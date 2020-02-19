from flask import Flask, redirect, jsonify, abort, request, url_for, Response, make_response
from werkzeug.datastructures import Headers

from where.model.field_types import FieldType
from where.model.sa import Category, Point, Field, with_session

app = Flask(__name__)


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
    # session = Session()
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
    result = session.query(Category).filter_by(id=id).first()
    if result:
        return jsonify(result.as_json())
    else:
        abort(404)


@app.route('/point/<id>')
@with_session
def get_point(session, id):
    result = session.query(Point).filter_by(id=id).first()
    if result:
        return jsonify(result.as_json())
    else:
        abort(404)


@app.route('/add-point', methods=['POST'])
@with_session
def add_point(session):
    allowed_params = {'name', 'lat', 'lon', 'attributes', 'category_id', 'parent_id'}
    data = request.get_json()
    data = {key:val for key, val in data.items() if key in allowed_params}
    
    # TODO: For some reason point.category is NULL when we do validation, even though the category ID is present
    #       this is causing an exception whenever a non-null attributes object is passed
    point = Point(category_id=data.pop('category_id'))
    for key, val in data.items():
        setattr(point, key, val)

    session.add(point)
    session.commit()

    response = make_response(jsonify(point.as_json()), 201)
    response.headers['Location'] = url_for('get_point', id=point.id)
    return response


@app.route('/point', methods=['GET'])
@with_session
def search_points(session):
    q = session.query(Point)
    
    if 'category_id' in request.args:
        q = q.filter(Point.category_id == request.args.get('category_id'))

    if 'parent_id' in request.args:
        q = q.filter(Point.parent_id == request.args.get('parent_id'))

    return jsonify(list(map(lambda p: p.as_json(), q.limit(100).all())))


if __name__ == '__main__':
    app.run()