from contextlib import contextmanager

from sqlalchemy import String, ForeignKey, Enum, Integer, Float, JSON
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship, validates
from sqlalchemy.schema import Column

from .field_types import FieldType
from .meta import Session


@contextmanager
def session_context():
    session = Session()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()

# Decorator for convenience when building endpoints
def with_session(func):
    def wrapper(*args, **kwargs):
        with session_context() as session:
            func(session, *args, **kwargs)

    # Flask identifies endpoint handlers based on their name
    wrapper.__name__ = func.__name__
    return wrapper


@as_declarative()
class Base(object):
    pass


class Point(Base):
    """
    Represents actual instances of any and all points on the map.
    """
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    attributes = Column(JSON, nullable=False)

    # Relationships
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category')
    parent_id = Column(Integer, ForeignKey('point.id'), nullable=True)
    parent = relationship('Point', remote_side=[id])
    children = relationship('Point')

    @validates('attributes')
    def validate_data(self, _, data):
        if data is None:
            return
        fields = self.category.fields
        for key in data:
            # Find Field object that corresponds to this key
            for field in fields:
                if field.slug == key:
                    break
            else:
                raise ValueError(f'extra data "{key}" must be a registered field')
            field.validate_data(data[key])
        return data

    def as_json(self, children=True):
        if children:
            children = [child.as_json(children=False) for child in self.children]
        return {
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "category": self.category.id,
            "attributes": self.attributes,
            "children": children
        }


class Category(Base):
    """
    Represent a schema for a single category of objects (e.g. water fountain or bathroom)
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    icon = Column(String, nullable=True)

    fields = relationship("Field")

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "attributes": {attr.slug: attr.as_json() for attr in self.fields}
        }


class Field(Base):
    """
    Represents a single field in the Category schema.
    """
    __tablename__ = 'field'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(FieldType), nullable=False)

    # Relationship
    category_id = Column(Integer, ForeignKey('category.id'))

    def validate_data(self, data):
        """
        Verify that data is the correct type for this Field.
        """
        self.type.validate(data)

    def as_json(self):
        return {
            "slug": self.slug,
            "name": self.name,
            "type": self.type.name
        }
