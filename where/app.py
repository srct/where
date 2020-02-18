from flask import Flask, redirect, jsonify, abort

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
    # an actual instance!
    fn = Point()
    fn.name = None
    fn.lat = 38.829791
    fn.lon = -77.307043
    # fn.category_id = wf.id
    fn.category = wf
    fn.parent_id = None
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

@app.route('/point', methods=['POST'])
@with_session
def query_point():
    pass
        

if __name__ == '__main__':
    app.run()
