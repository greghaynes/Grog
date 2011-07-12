from tests.settings import BASE_URL
from grog.settings import ADMIN_PASSWORD

from urllib2 import build_opener, HTTPCookieProcessor, install_opener, urlopen
from urllib import urlencode
import json
import unittest

class ClientTester(unittest.TestCase):
	def setUp(self):
		self.opener = build_opener(HTTPCookieProcessor())
		install_opener(self.opener)

	def post_req(self, api_path, data):
		return self.opener.open(BASE_URL+api_path, urlencode(data))

	def get_req(self, api_path):
		return self.opener.open(BASE_URL+api_path)

	def admin_login(self):
		self.assertEqual(json.loads(self.post_req('user/login', {'username': 'admin', 'password': ADMIN_PASSWORD}).read()), {'id': -1})

