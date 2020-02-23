from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .model import Point, Category, Field

class PointSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Point
        include_relationships = True
        load_instance = True


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_relationships = True
        load_instance = True


class FieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Field
        include_relationships = True
        load_instance = True
        