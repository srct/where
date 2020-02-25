from flask import request
from urllib import parse
import requests
import xml.etree.ElementTree as et


# XML cas namespace. Read: https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
XML_NS = {'cas': 'http://www.yale.edu/tp/cas'}


def find_auth_token():
	if request.method == 'GET':
		return request.args.get('ticket')
	else:
		return None


def format_service_name():
	return parse.quote(request.base_url)


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
