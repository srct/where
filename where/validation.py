from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from .model import Point, Category, Field, Session

class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        include_relationships = True
        sqla_session = Session


class PointSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Point


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category


class FieldSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Field

