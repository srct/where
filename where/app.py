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
    print(PointSchema().Meta.model)
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


@app.route('/category/<int:id>')
def get_category(id):
    return get_resource(CategorySchema(), id)


@app.route('/category/<int:id>/children')
def get_category_children(data, id):
    data = dict(request.args)
    data['parent_id'] = id
    return search_resource(PointSchema(), data)


@app.route('/point', methods=['GET'])
@use_args({'parent_id': fields.Int(), 'category_id': fields.Int(required=True)})
def search_point(args):
    return search_resource(PointSchema(), args)


@app.route('/point', methods=['POST'])
@use_args(PointSchema)
def create_point(args):
    return create_resource(PointSchema(), args, 'get_point')
   

@app.route('/point/<int:id>', methods=['GET'])
def get_point(id):
    return get_resource(PointSchema(), id)


@app.route('/point/<int:id>', methods=['DELETE'])
def del_point(id):
    return delete_resource(PointSchema(), id)


#TODO: Validate this
@app.route('/point/<int:id>', methods=['PUT'])
def edit_point(id):
    return edit_resource(PointSchema(), id, request.get_json())


@app.route('/point/<int:id>/children', methods=['GET'])
def get_point_children(id):
    data = dict(request.args)
    data['parent_id'] = id
    return search_resource(PointSchema(), data)


# Helper functions:


def create_resource(schema, data, get_function):
    '''
    Create the resource specified by the given model class and initialized with the data
    dict, returning an appropriate JSON response. 

    Parameters:
    schema       (object): The class of the model for this resource
    data         (dict)  : The initial data for this resource stored as a dictionary
    get_function (string): The name of the view function (as a string) that gets a single 
                           instance of this resource. This is used for the response Location header.
    
    Returns: a Flask Response object
    '''
    resource = schema.Meta.model(**data)
    g.db_session.add(resource)
    g.db_session.commit()

    response = make_response(schema.dump(resource, many=False), 201)
    response.headers['Location'] = url_for(get_function, id=resource.id)
    return response


def get_resource(schema, id):
    '''
    Get a single resource of the specified model class by its ID.
    
    Parameters:
    schema  (object): The class of the model for this resource
    id      (int)   : The id of this resource
    
    Returns: a Flask Response object
    '''
    resource = g.db_session.query(schema.Meta.model).get(id)
    resp = (None, 404) if resource is None else \
        (schema.dump(resource, many=False), 200)
    return make_response(resp)


def edit_resource(schema, id, data):
    '''
    Modify the resource of the specified model class and id with the data from
    data. Does not perform data validation.

    Parameters:
    schema  (object): The class of the model for this resource
    id      (int)   : The id of this resource
    data    (dict)  : The new data for this resource stored as a dictionary
    
    Returns: a Flask Response object
    '''
    resource = g.db_session.query(schema.Meta.model).get(id)
    for attr in data:
        setattr(resource, attr, data[attr])
    g.db_session.commit()

    return make_response(schema.dump(resource), 200)


def delete_resource(schema, id):
    '''
    Delete the resource of the specified model class and id and return the 
    appropriate response.

    Parameters:
    schema  (object): The class of the model for this resource
    id      (int)   : The id of this resource
    
    Returns: a Flask Response object
    '''
    resource = g.db_session.query(schema.Meta.model).get(id)
    g.db_session.delete(resource)
    g.db_session.commit()

    return make_response('', 204)


def search_resource(schema, data):
    '''
    Search the database for a list of instances of the specified model class
    that have the attributes given in data and return the appropriate JSON
    response. Does not perform validation on search parameters.

    Parameters:
    schema  (object): The class of the model for this resource
    data    (dict)  : A dictionary containing search parameters
    
    Returns:
    a Flask Response object
    '''

    # TODO: returns 404 when accessing children - i think it should just return an empty array
    query = g.db_session.query(schema.Meta.model).filter_by(**data)
    resp = (None, 404) if query.first() is None else \
        (schema.dump(query.all(), many=True), 200)

    return make_response(resp)


if __name__ == '__main__':
    app.run()
