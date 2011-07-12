from tests.settings import BASE_URL
from tests.utils import ClientTester

from grog.models import User
from grog.settings import ADMIN_PASSWORD

from urllib2 import build_opener, HTTPCookieProcessor, install_opener, urlopen
from urllib import urlencode
import json

class CreateUser(ClientTester):
	def test_superuser(self):
		self.admin_login()

		# Create user
		u = User('test', 'Test User', 'test1234', False, False)
		resp = json.loads(self.post_req('user/create', {'username': 'test', 'fullname': 'Test User', 'password': 'test1234', 'superuser': False, 'editor': False}).read())
		self.assertFalse('status' in resp)
		u.id = resp['id']

		# Check user profile
		resp = json.loads(self.get_req('user/profile/%d'%u.id).read())
		self.assertFalse('status' in resp)
		self.assertEqual(resp['superuser'], False)
		self.assertEqual(resp['editor'], False)

		# Delete user
		resp = json.loads(self.get_req('user/delete/%d'%u.id).read())
		self.assertFalse('status' in resp)

