from flask import Flask, redirect, jsonify, abort, request, url_for, make_response, g
from webargs.flaskparser import use_args
from webargs import fields

from where.model import Session, Point, Category, Field
from where.model.field_types import FieldType

from where.validation import PointSchema, CategorySchema, FieldSchema

app = Flask(__name__)


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


@app.route('/')
def index():
    return """
<head>
</head>
<body>
    <h1>W H E R E</h1>
    <p>This is the WHERE project.</p>
    <a href='/test_data'>Click here to nuke the database and make it all be test data.</a>
</body>
    """


@app.route('/test_data')
def test_data():
    g.db_session.query(Point).delete()
    g.db_session.query(Field).delete()
    g.db_session.query(Category).delete()
    # Water Fountain, the class.
    wf = Category()
    wf.name = "Water Fountain"
    wf.icon = "https://karel.pw/water.png"
    g.db_session.add(wf)
    g.db_session.commit()
    # Building
    bd = Category()
    bd.name = "Building"
    bd.icon = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/basket-building-news-photo-1572015168.jpg?resize=980:*"
    g.db_session.add(bd)
    g.db_session.commit()
    # Radius (Really the simplest metric we can have for building size)
    rd = Field()
    rd.name = "Radius"
    rd.slug = "radius"
    rd.type = FieldType.FLOAT
    rd.category_id = bd.id
    g.db_session.add(rd)
    g.db_session.commit()

    # coldness
    cd = Field()
    cd.name = "Coldness"
    cd.slug = "coldness"
    cd.type = FieldType.RATING
    cd.category_id = wf.id
    # filler
    fl = Field()
    fl.slug = "bottle_filler"
    fl.name = "Has Bottle Filler"
    fl.type = FieldType.BOOLEAN
    fl.category_id = wf.id
    g.db_session.add(cd)
    g.db_session.add(fl)
    g.db_session.commit()

    # The johnson center
    jc = Point()
    jc.category = bd
    jc.name = "Johnson Center"
    jc.lat = 38
    jc.lon = -77
    jc.parent = None
    jc.attributes = {
        "radius": {
            "value": 2.0
        }
    }
    g.db_session.add(jc)

    # A water fountain inside the JC
    fn = Point()
    fn.name = None
    fn.lat = 38.829791
    fn.lon = -77.307043
    # fn.category_id = wf.id
    fn.category = wf
    fn.parent = jc
    fn.attributes = {
        "coldness": {
            "num_reviews": 32,
            "average_rating": 0.5
        },
        "bottle_filler": {
            "value": True
        }
    }

    g.db_session.add(fn)
    g.db_session.commit()
    return redirect('/')


@app.route('/category/<int:id>')
def get_category(id):
    return get_resource(Category, id)


@app.route('/category/<int:id>/children')
def get_category_children(data, id):
    data = dict(request.args)
    data['parent_id'] = id
    return search_resource(Point, data)


@app.route('/point', methods=['GET'])
@use_args({'parent_id': fields.Int(), 'category_id': fields.Int(required=True)})
def search_point(args):
    return search_resource(Point, args)


@app.route('/point', methods=['POST'])
@use_args(PointSchema)
def create_point(args):
    args['category'] = g.db_session.query(Category).get(args.pop('category_id'))
    return create_resource(Point, args, 'get_point')
   

@app.route('/point/<int:id>', methods=['GET'])
def get_point(id):
    return get_resource(Point, id)


@app.route('/point/<int:id>', methods=['DELETE'])
def del_point(id):
    return delete_resource(Point, id)


@app.route('/point/<int:id>', methods=['PUT'])
def edit_point(id):
    return edit_resource(Point, id, request.get_json())


@app.route('/point/<int:id>/children', methods=['GET'])
def get_point_children(id):
    data = dict(request.args)
    data['parent_id'] = id
    return search_resource(Point, data)


# Helper functions:


def create_resource(model_cls, data, get_function):
    '''
    Create the resource specified by the given model class and initialized with the data
    dict, returning an appropriate JSON response. 

    :param model_cls: The class of the model for this resource
    :param data: The initial data for this resource stored as a dictionary
    :param get_function: The name of the view function (as a string) that gets a single instance of this resource. This is used for the response Location header.
    :return: a Flask Response object
    '''
    resource = model_cls(**data)
    g.db_session.add(resource)
    g.db_session.commit()

    response = make_response(jsonify(resource.as_json()), 201)
    response.headers['Location'] = url_for(get_function, id=resource.id)
    return response


def get_resource(model_cls, id):
    '''
    Get a single resource of the specified model class by its ID.
    
    :param model_cls: The class of the model for this resource
    :param id: The id of this resource
    :return: a Flask Response object
    '''
    resource = g.db_session.query(model_cls).get(id)
    resp = (None, 404) if resource is None else \
        (resource.as_json(), 200)
    return make_response(jsonify(resp[0]), resp[1])


def edit_resource(model_cls, id, data):
    '''
    Modify the resource of the specified model class and id with the data from
    data. Does not perform data validation.

    :param model_cls: The class of the model for this resource
    :param id: The id of this resource
    :param data: The new data for this resource stored as a dictionary
    :return: a Flask Response object
    '''
    resource = g.db_session.query(model_cls).get(id)
    for attr in data:
        setattr(resource, attr, data[attr])
    g.db_session.commit()

    return make_response(jsonify(resource.as_json()), 200)


def delete_resource(model_cls, id):
    '''
    Delete the resource of the specified model class and id and return the 
    appropriate response.

    :param model_cls: The class of the model for this resource
    :param id: The id of this resource
    :return: a Flask Response object
    '''
    resource = g.db_session.query(model_cls).get(id)
    g.db_session.delete(resource)
    g.db_session.commit()

    return make_response('', 204)


def search_resource(model_cls, data):
    '''
    Search the database for a list of instances of the specified model class
    that have the attributes given in data and return the appropriate JSON
    response. Does not perform validation on search parameters.

    :param model_cls: The class of the model for this resource
    :param data: A dictionary containing search parameters
    :return: a Flask Response object
    '''
    query = g.db_session.query(model_cls).filter_by(**data)
    resp = (None, 404) if query.first() is None else \
        (list(map(lambda m: m.as_json(), query.limit(100).all())), 200)

    return make_response(jsonify(resp[0]), resp[1])


if __name__ == '__main__':
    app.run()
