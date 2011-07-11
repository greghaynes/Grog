from tests.settings import BASE_URL
from grog.settings import ADMIN_PASSWORD

from urllib2 import urlopen
from urllib import urlencode
import json

def post_req(api_path, data):
	return urlopen(BASE_URL+api_path, urlencode(data))

def admin_login():
	resp = post_req('user/login', {'username': 'admin', 'password': ADMIN_PASSWORD})
	resp_data = json.loads(resp.read())
	try:
		if resp_data['status'] == 'Error':
			print 'Invalid login as admin, got: %s' % resp
			return False
	except KeyError:
		pass
	return True

