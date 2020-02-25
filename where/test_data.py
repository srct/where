from where.model import Session, Point, Category, Field
from where.model.field_types import FieldType

from flask import g

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
