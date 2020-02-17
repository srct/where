from flask import Flask
from sqlalchemy.orm import Session

from where.field_types import FieldType
from . import sa

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
def test_data():
    with sa.session_context() as session:
        session = Session()
        session.query(sa.Point).delete()
        session.query(sa.Field).delete()
        session.query(sa.Category).delete()
        # Water Fountain, the class.
        wf = sa.Category()
        wf.name = "Water Fountain"
        wf.icon = "https://karel.pw/water.png"
        session.add(wf)
        session.commit()
        # coldness
        cd = sa.Field()
        cd.name = "Coldness"
        cd.type = FieldType.RATING
        cd.category_id = wf.id



if __name__ == '__main__':
    app.run()
