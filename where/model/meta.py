from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3')  # TODO configurable

Session = sessionmaker(bind=engine)
