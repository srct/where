from contextlib import contextmanager

from sqlalchemy import String, ForeignKey, Enum, Integer, Float, JSON
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship, validates, Session
from sqlalchemy.schema import Column

from .field_types import FieldType


@contextmanager
def session_context() -> Session:
    session = Session()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


class Point(Base):
    """
    TODO docstring
    """
    __tablename__ = 'point'
    name = Column(String, nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    attributes = Column(JSON, nullable=False)

    # Relationships
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category')
    parent_id = Column(Integer, ForeignKey('point.id'), nullable=True)
    parent = relationship('Point')

    @validates('attributes')
    def validate_data(self, _, data):
        # TODO validate
        if data is None:
            return
        fields = self.category.fields
        for key in data:
            # Find Field object that corresponds to this key
            for field in fields:
                if field.name == key:
                    break
            else:
                raise ValueError('extra data must be a registered field')
            field.validate_data(data[key])
        return data


class Category(Base):
    """
    Represent a schema for a single category of objects (e.g. water fountain)
    """
    __tablename__ = 'category'

    name = Column(String, nullable=False, unique=True)
    icon = Column(String, nullable=True)

    fields = relationship("Field")


class Field(Base):
    """
    Represent a field that can be on an ObjectType schema
    """
    __tablename__ = 'field'

    name = Column(String, nullable=False)
    type = Column(Enum(FieldType), nullable=False)

    # Relationship
    category_id = Column(Integer, ForeignKey('category.id'))

    def validate_data(self, data):
        """
        Verify that data is the correct type for this Field.
        """
        self.type.validate(data)
