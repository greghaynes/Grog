from tests.settings import BASE_URL

from grog.models import User
from grog.settings import ADMIN_PASSWORD

from urllib2 import build_opener, HTTPCookieProcessor, install_opener, urlopen
from urllib import urlencode
import unittest
import json

class CreateUser(unittest.TestCase):
	def setUp(self):
		self.opener = build_opener(HTTPCookieProcessor())
		install_opener(self.opener)

	def post_req(self, api_path, data):
		return self.opener.open(BASE_URL+api_path, urlencode(data))

	def get_req(self, api_path):
		return self.opener.open(BASE_URL+api_path)

	def test_create_delete(self):
		# login as admin
		self.assertEqual(json.loads(self.post_req('user/login', {'username': 'admin', 'password': ADMIN_PASSWORD}).read()), {'id': -1})

		# Create user
		u = User('test', 'Test User', 'test1234', False, False)
		resp = json.loads(self.post_req('user/create', {'username': 'test', 'fullname': 'Test User', 'password': 'test1234', 'superuser': False, 'editor': False}).read())
		u.id = resp['id']
		self.assertFalse('status' in resp)

		# Check user profile
		resp = json.loads(self.get_req('user/profile/%d'%u.id).read())
		self.assertFalse('status' in resp)

		# Delete user
		resp = json.loads(self.get_req('user/delete/%d'%u.id).read())
		self.assertFalse('status' in resp)

