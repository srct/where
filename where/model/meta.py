from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///db.sqlite3')  # TODO configurable

# Session is scoped to the current thread (which, in Flask, is the current request)
Session = scoped_session(sessionmaker(bind=engine))