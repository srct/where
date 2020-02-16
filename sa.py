from sqlalchemy import String, ARRAY, Table, ForeignKey, Enum, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, validates
from sqlalchemy.schema import Column

from .field_types import FieldType


# TODO declarative_base
class Base(object):
    # id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)


# This table maintains the field <-> ObjectType links.
type_links = Table('type_links', Base.metadata,  # ???
                   Column('type_id', Integer, ForeignKey('objecttype.id')),
                   Column('field_id', Integer, ForeignKey('field.id')))


class Point(Base):
    """
    TODO docstring
    """
    __tablename__ = 'point'
    name = Column(String, nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    attributes = Column(JSONB, nullable=False)

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

    slug = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)

    fields = relationship("Field")


class Field(Base):
    """
    Represent a field that can be on an ObjectType schema
    """
    __tablename__ = 'field'

    name = Column(String, nullable=False)
    type = Column(Enum(FieldType), nullable=False)
    unit = Column(String)

    # Relationship
    category_id = Column(Integer, ForeignKey('category.id'))

    def validate_data(self, data):
        """
        Verify that data is the correct type for this Field.
        """
        if type(data) is not dict:
            raise ValueError('Input "{}" for field {} is not of type dict'.format(data, self.name))
        print(type(data))
        print(self.type)
        raise ValueError('Invalid input "{}" for field {}'.format(data, self.name))
