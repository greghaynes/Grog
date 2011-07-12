from tests.utils import ClientTester

from grog.models import Entry

import json

def CreateEntry(ClientTester):
	def req_create_entry(self, title, content, author_id):
		return self.post_req('entry/create', {'title': title, 'content': content})

	def test_create_entry(self):
		self.admin_login()

		# Create temp user
		resp = json.loads(self.post_req('user/create', {'username': 'test', 'fullname': 'Test User', 'password': 'test1234', 'superuser': superuser, 'editor': editor}).read())
		# login as temp user
		resp = json.loads(self.post_req('user/login', {'username': 'test', 'password': 'test1234'}))

		self.admin_login()

		# Delete temp user
		resp = json.loads(self.get_req('user/delete/%d'%u.id).read())

