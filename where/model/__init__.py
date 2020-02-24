from contextlib import contextmanager

from .meta import Session
from .field_types import FieldType
from .models import Base, Point, Category, Field


@contextmanager
def session_context():
    session = Session()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


def with_session(func):
    """
    Decorator for convenience when building endpoints.  The first argument to the
    decorated function will be a safe-to-use, autocommitting Session instance.
    :param func: the view function to wrap
    :return: the wrapped function
    """

    def wrapper(*args, **kwargs):
        with session_context() as session:
            return func(session, *args, **kwargs)

    # Flask identifies endpoint handlers based on their name
    wrapper.__name__ = func.__name__
    return wrapper
