from flask import Flask, redirect, g, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from model import AccessLevel
from routing_util import init_routing_util, ResourceNamespace, get_resource, CategorySchema, create_resource, edit_resource, search_resource, PointSchema, delete_resource
from where import auth
# from where.auth import authenticated
from where.error_handlers import register_error_handlers
from where.model import Session

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'potato'  # TODO set this from some kind of config file / environment variable
auth.init(app)
register_error_handlers(app)
init_routing_util(app)


@app.route('/auth')
def authenticate():
    return jsonify(auth_url=auth.get_auth_url())


@app.route('/validate-auth')
@use_args({'ticket': fields.Str(required=True)})
def validate_auth(args):
    pass


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
    import where.test_data as t
    t.create_test_data()
    return redirect('/')


category = ResourceNamespace('category')


@category.getter
def get_category(id: int):
    return get_resource(CategorySchema(), id)


# @authenticated(AccessLevel.ADMIN)
@category.creator
@use_args(CategorySchema())
def create_category(args):
    return create_resource(CategorySchema(), args, 'get_category')


# @authenticated(AccessLevel.ADMIN)
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


# @authenticated(AccessLevel.ADMIN)
@point.creator
@use_args(PointSchema)
def create_point(args):
    return create_resource(PointSchema(), args, 'get_point')


@point.getter
def get_point(id):
    return get_resource(PointSchema(), id)


# @authenticated(AccessLevel.ADMIN)
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
