from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from .model import Point, Category, Field

class PointSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Point
        include_fk = True
        include_relationships = False
        load_instance = False


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_relationships = False
        load_instance = False


class FieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Field
        include_relationships = False
        load_instance = False
