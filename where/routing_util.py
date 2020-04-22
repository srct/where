from flask import url_for, make_response, abort, g, jsonify
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

from where.model import Point, Category, Field, Session


def init_routing_util(app):
    ResourceNamespace.app = app


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


class ResourceNamespace:
    """
    A simple way to create endpoints based off a certain resource. Does nothing more than wrap
    around the app.route functionality in a handy way.
    """

    def __init__(self, name):
        self.name = name

    def route(self, path, **kwargs):
        def decorator(func):
            self.app.route(f'/{self.name}{path}', **kwargs)(func)

        return decorator

    def creator(self, func):
        self.route('/', methods=['POST'])(func)

    def getter(self, func):
        self.route('/<int:id>', methods=['GET'])(func)

    def deleter(self, func):
        self.route('/<int:id>', methods=['DELETE'])(func)

    def editor(self, func):
        self.route('/<int:id>', methods=['PUT'])(func)


def create_resource(schema: CategorySchema, data: dict, get_function: str):
    """
    Create the resource specified by the given model class and initialized with the data
    dict, returning an appropriate JSON response.

    :param schema: The class of the model for this resource
    :param data: The initial data for this resource stored as a dictionary
    :param get_function: The name of the view function (as a string) that gets a single
                           instance of this resource. This is used for the response Location header.
    :return: a Flask Response object
    """
    resource = schema.Meta.model(**data)
    g.db_session.add(resource)
    g.db_session.commit()

    response = make_response(schema.dump(resource, many=False), 201)
    response.headers['Location'] = url_for(get_function, id=resource.id)
    return response


def get_resource(schema: BaseSchema, id: int):
    """
    Get a single resource of the specified model class by its ID.

    :param schema: The class of the model for this resource
    :param id: The id of this resource
    :return: a Flask Response object
    """
    resource = g.db_session.query(schema.Meta.model).get(id)
    if resource is None:
        abort(404)

    resp = (schema.dump(resource, many=False), 200)
    return make_response(resp)


def edit_resource(schema: BaseSchema, id: int, data: dict):
    """
    Modify the resource of the specified model class and id with the data from
    data. Does not perform data validation.

    :param schema: The class of the model for this resource
    :param id: The id of this resource
    :param data: The new data for this resource stored as a dictionary

    Returns: a Flask Response object
    """
    resource = g.db_session.query(schema.Meta.model).get(id)
    for attr in data:
        setattr(resource, attr, data[attr])
    g.db_session.commit()

    return make_response(schema.dump(resource), 200)


def delete_resource(schema: BaseSchema, id: int):
    """
    Delete the resource of the specified model class and id and return the
    appropriate response.

    :param schema: The class of the model for this resource
    :param id: The id of this resource
    :return: a Flask Response object
    """
    resource = g.db_session.query(schema.Meta.model).get(id)
    g.db_session.delete(resource)
    g.db_session.commit()

    return make_response('', 204)


def search_resource(schema: BaseSchema, data: dict):
    """
    Search the database for a list of instances of the specified model class
    that have the attributes given in data and return the appropriate JSON
    response. Does not perform validation on search parameters.

    :param schema: The class of the model for this resource
    :param data: A dictionary containing search parameters

    :return: a Flask Response object
    """
    query = g.db_session.query(schema.Meta.model).filter_by(**data)
    if query.first() is None:
        abort(404)

    resp = (jsonify(schema.dump(query.all(), many=True)), 200)
    return make_response(resp)
