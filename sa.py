import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import String, DateTime, Numeric, ARRAY, Table, ForeignKey, Enum, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, validates
from sqlalchemy.orm.session import Session as BaseSession

from .field_types import FieldType


# TODO declarative_base
class Base(object):
    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))

class Session(SessionManager):
    engine = sqlalchemy.create_engine(config['sqlalchemy.url'])



# This table maintains the field <-> ObjectType links.
type_links = Table('type_links', Base.metadata,
        Column('type_id', UUID, ForeignKey('objecttype.id')),
        Column('field_id' UUID, ForeignKey('field.id')))



class MapObject(Base):
    __tablename__ = 'mapobject' #TODO fix for py3/new sa
    name = Column(String, nullable=False)
    type_id = Column(UUID, ForeignKey('objecttype.id')) # TODO fix foreignkeyconstraint
    type = relationship('ObjectType')
    lat = Column(Numeric(precision=10, scale=15, asdecimal=False), nullable=False)#TODO this doesn't work
    lon = Column(Numeric(precision=10, scale=15, asdecimal=False), nullable=False) 
    data = Column(JSONB)

    @validates('data')
    def validate_data(self, _, data):
        if data is None:
            return
        fields = type.fields
        for key in data:
            for field in fields:
                if field.name == key:
                    break
            else:
                raise ValueError('extra data must be a registered field')
            field.validate_data(data[key])
        return data

class ObjectType(Base):
    """
    Represent a schema
    """
    __tablename__ = 'objecttype' #TODO py3

    name = Column(String, nullable=False, unique=True)
    fields = relationship('Field', secondary=type_links, backref='types')


class Field(Base):
    """
    Represent a field that can be on an ObjectType schema
    """
    __tablename__ = 'field' # TODO this don't work in py3?

    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(FieldType), nullable=False)
    unit = Column(String)
    values = Column(ARRAY(String)) # enum values - TODO change to comma-separated list if sqlite don't support?
    # types: List[ObjectType]

    def validate_data(self, data):
        """
        Verify that data is the correct type for this Field.
        """
        if self.type is FieldType.BOOLEAN and isinstance(data, bool):
            return
        if self.type is FieldType.FLOAT and isinstance(data, float) or isinstance(data, int):
            return
        if self.type is FieldType.INTEGER and isinstance(data, int):
            return
        if self.type is FieldType.STRING and isinstance(data, str):
            return
        if self.type is FieldType.ENUM and isinstance(data, str):
            if data in self.values:
                return
        print(type(data))
        print(self.type)
        raise ValueError('Invalid input "{}" for field {}'.format(data, self.name))
