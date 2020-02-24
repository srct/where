from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from .model import Point, Category, Field, Session

class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        include_relationships = True
        sqla_session = Session


class PointSchema(BaseSchema):
    children = fields.Nested('PointSchema', exclude=('children',), many=True)

    class Meta(BaseSchema.Meta):
        model = Point


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category


class FieldSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Field

