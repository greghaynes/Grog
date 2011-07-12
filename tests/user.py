from tests.settings import BASE_URL
from tests.utils import ClientTester

from grog.models import User
from grog.settings import ADMIN_PASSWORD

from urllib2 import build_opener, HTTPCookieProcessor, install_opener, urlopen
from urllib import urlencode
import json

class CreateUser(ClientTester):
	def run_createuser_test(self, superuser, editor):
		self.admin_login()

		# Create user
		u = User('test', 'Test User', 'test1234', superuser, editor)
		resp = json.loads(self.post_req('user/create', {'username': 'test', 'fullname': 'Test User', 'password': 'test1234', 'superuser': superuser, 'editor': editor}).read())
		self.assertFalse('status' in resp)
		u.id = resp['id']

		# Check user profile
		resp = json.loads(self.get_req('user/profile/%d'%u.id).read())
		self.assertFalse('status' in resp)
		self.assertEqual(resp['superuser'], superuser)
		self.assertEqual(resp['editor'], editor)

		# Delete user
		resp = json.loads(self.get_req('user/delete/%d'%u.id).read())
		self.assertFalse('status' in resp)

	def test_create_noperms(self):
		self.run_createuser_test(False, False)

	def test_create_editor(self):
		self.run_createuser_test(False, True)

	def test_create_superuser(self):
		self.run_createuser_test(True, False)

	def test_create_superuser_editor(self):
		self.run_createuser_test(True, True)

