import xml.etree.ElementTree as et
from functools import wraps
from urllib import parse

import requests
from flask import request, g, make_response, url_for
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity

from where.model import User, AccessLevel

# XML cas namespace. Read: https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
XML_NS = {'cas': 'http://www.yale.edu/tp/cas'}
jwt = None


def init(app):
    global jwt
    jwt = JWTManager(app)


def authenticated(level=AccessLevel.USER, pass_user=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = g.db_session.query(User).get(get_jwt_identity())

            if user is None:
                return make_response(None, 404)

            if level > user.access_level:
                return make_response(None, 500)

            if pass_user:
                return func(user, *args, **kwargs)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def format_service_name():
    return parse.quote('https://' + request.host + url_for('validate_auth'))


def get_auth_url():
    # This is the link to the GMU CAS
    return f'https://login.gmu.edu/?service={format_service_name()}'


def validate_auth_token(token):
    response = requests.get(f'https://login.gmu.edu/serviceValidate?service={format_service_name()}&ticket={token}')
    root = et.fromstring(response.text)

    success_block = root.find('cas:authenticationSuccess', XML_NS)

    if success_block:
        return True, success_block.find('cas:user', XML_NS).text
    else:
        return False, None
