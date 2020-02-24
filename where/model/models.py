from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship, validates

from . import FieldType

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

    def __init__(self, **kwargs):
        # Need to load category first or else attribute validation will fail
        if 'category' in kwargs:
            self.category = kwargs.pop('category')
        
        super(Point, self).__init__(**kwargs)


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


class Category(Base):
    """
    Represent a schema for a single category of objects (e.g. water fountain or bathroom)
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    icon = Column(String, nullable=True)

    fields = relationship("Field")


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
