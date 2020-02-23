from flask import Flask, redirect, jsonify, abort, request, url_for, make_response

from where.model import with_session, Point, Category, Field
from where.model.field_types import FieldType

from where.validation import PointSchema, CategorySchema, FieldSchema

app = Flask(__name__)


# Endpoints:


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
@with_session
def test_data(session):
    session.query(Point).delete()
    session.query(Field).delete()
    session.query(Category).delete()
    # Water Fountain, the class.
    wf = Category()
    wf.name = "Water Fountain"
    wf.icon = "https://karel.pw/water.png"
    session.add(wf)
    session.commit()
    # Building
    bd = Category()
    bd.name = "Building"
    bd.icon = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/basket-building-news-photo-1572015168.jpg?resize=980:*"
    session.add(bd)
    session.commit()
    # Radius (Really the simplest metric we can have for building size)
    rd = Field()
    rd.name = "Radius"
    rd.slug = "radius"
    rd.type = FieldType.FLOAT
    rd.category_id = bd.id
    session.add(rd)
    session.commit()

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
    session.add(cd)
    session.add(fl)
    session.commit()

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
    session.add(jc)

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

    session.add(fn)
    session.commit()
    return redirect('/')


@app.route('/category/<id>')
@with_session
def get_category(session, id):
    return get_resource(session, Category, id)


@app.route('/category/<id>/children')
@with_session
def get_category_children(session, id):
    data = dict(request.args)
    data['parent_id'] = id
    return search_resource(session, Point, data)


@app.route('/point', methods=['GET'])
@with_session
def search_point(session):
    return search_resource(session, Point, dict(request.args))


@app.route('/point', methods=['POST'])
def create_point(session):
    data = request.get_json()
    data['category'] = session.query(Category).get(data.pop('category_id'))

    return create_resource(session, Point, data, 'get_point')
   

@app.route('/point/<id>', methods=['GET'])
@with_session
def get_point(session, id):
    return get_resource(session, Point, id)


@app.route('/point/<id>', methods=['DELETE'])
@with_session
def del_point(session, id):
    return delete_resource(session, Point, id)


@app.route('/point/<id>', methods=['PUT'])
@with_session
def edit_point(session, id):
    return edit_resource(session, Point, id, request.get_json())


@app.route('/point/<id>/children', methods=['GET'])
@with_session
def get_point_children(session, id):
    data = dict(request.args)
    data['parent_id'] = id
    return search_resource(session, Point, data)


# Helper functions:
# TODO: Add helper functions for data validation


def create_resource(session, model_cls, data, get_function):
    '''
    Create the resource specified by the given model class and initialized with the data
    dict, returning an appropriate JSON response. 

    :param session: The sqlalchemy session
    :param model_cls: The class of the model for this resource
    :param data: The initial data for this resource stored as a dictionary
    :param get_function: The name of the view function (as a string) that gets a single instance of this resource. This is used for the response Location header.
    :return: a Flask Response object
    '''
    resource = model_cls(**data)
    session.add(resource)
    session.commit()

    response = make_response(jsonify(resource.as_json()), 201)
    response.headers['Location'] = url_for(get_function, id=resource.id)
    return response


def get_resource(session, model_cls, id):
    '''
    Get a single resource of the specified model class by its ID.
    
    :param session: The sqlalchemy session
    :param model_cls: The class of the model for this resource
    :param id: The id of this resource
    :return: a Flask Response object
    '''
    resource = session.query(model_cls).get(id)
    return make_response(jsonify(resource.as_json()), 200)


def edit_resource(session, model_cls, id, data):
    '''
    Modify the resource of the specified model class and id with the data from
    data. Does not perform data validation.

    :param session: The sqlalchemy session
    :param model_cls: The class of the model for this resource
    :param id: The id of this resource
    :param data: The new data for this resource stored as a dictionary
    :return: a Flask Response object
    '''
    resource = session.query(model_cls).get(id)
    for attr in data:
        setattr(resource, attr, data[attr])
    session.commit()

    return make_response(jsonify(resource.as_json()), 200)


def delete_resource(session, model_cls, id):
    '''
    Delete the resource of the specified model class and id and return the 
    appropriate response.

    :param session: The sqlalchemy session
    :param model_cls: The class of the model for this resource
    :param id: The id of this resource
    :return: a Flask Response object
    '''
    resource = session.query(model_cls).get(id)
    session.delete(resource)
    session.commit()

    return make_response('', 204)


def search_resource(session, model_cls, data):
    '''
    Search the database for a list of instances of the specified model class
    that have the attributes given in data and return the appropriate JSON
    response. Does not perform validation on search parameters.

    :param session: The sqlalchemy session
    :param model_cls: The class of the model for this resource
    :param data: A dictionary containing search parameters
    :return: a Flask Response object
    '''
    query = session.query(model_cls).filter_by(**data)
    results = list(map(lambda m: m.as_json(), query.limit(100).all()))

    response = make_response(jsonify(results), 200)
    return response


if __name__ == '__main__':
    app.run()
