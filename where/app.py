from flask import Flask, redirect, request, url_for, make_response, g, jsonify, abort
from webargs import fields
from webargs.flaskparser import use_args

from where.model import Session, Point, Category, Field
from where.model.field_types import FieldType
from where.routing_util import *

from where.error_handlers import register_error_handlers
from where.test_data import create_test_data

app = Flask(__name__)
register_error_handlers(app)
init_routing_util(app)


@app.route('/')
def index():
    return """
<head>
</head>
<body>
    <h1>W H E R E</h1>
    <p>This is the WHERE project.</p>
    <a href='/test-data'>Click here to nuke the database and make it all be test data.</a>
</body>
    """


@app.route('/test-data')
def test_data():
    create_test_data()
    return redirect('/')


category = ResourceNamespace('category')


@category.getter
def get_category(id: int):
    return get_resource(CategorySchema(), id)


@category.creator
@use_args(CategorySchema())
def create_category(args):
    return create_resource(CategorySchema(), args, 'get_category')


@category.editor
@use_args(CategorySchema(exclude=('id',), partial=('name',)))
def edit_category(args, id: int):
    return edit_resource(CategorySchema(), id, args)


@category.route('/<int:id>/points')
@use_args(PointSchema(only=('parent',)))
def get_category_points(args: dict, id: int):
    args['category_id'] = id
    return search_resource(PointSchema(), args)


point = ResourceNamespace('point')


@point.route('/', methods=['GET'])
@use_args(PointSchema(only=('parent', 'category',), partial=('category',)))
def search_point(args):
    return search_resource(PointSchema(), args)


@point.creator
@use_args(PointSchema)
def create_point(args):
    return create_resource(PointSchema(), args, 'get_point')


@point.getter
def get_point(id):
    return get_resource(PointSchema(), id)


@point.deleter
def del_point(id):
    return delete_resource(PointSchema(), id)


@point.editor
@use_args(PointSchema(exclude=('id',), partial=('lat', 'lon', 'attributes', 'category')))
def edit_point(args, id):
    return edit_resource(PointSchema(), id, args)


@point.route('/<int:id>/children', methods=['GET'])
@use_args(PointSchema(only=('category',), partial=('category',)))
def get_point_children(args, id: int):
    args['parent_id'] = id
    return search_resource(PointSchema(), args)


# Database session cleanup:

@app.before_request
def create_local_db_session():
    g.db_session = Session()


@app.after_request
def destroy_local_db_session(resp):
    try:
        g.db_session.commit()
    except BaseException:
        g.db_session.rollback()
        raise
    finally:
        Session.remove()
        return resp


if __name__ == '__main__':
    app.run()
