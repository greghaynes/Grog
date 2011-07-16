from tests.utils import ClientTester

from grog.models import Entry

import json

class CreateEntry(ClientTester):
	def req_create_entry(self, title, content, author_id):
		return self.post_req('entry/create', {'title': title, 'content': content}).read()

	def test_single_entry(self):
		self.admin_login()

		# Create temp user
		resp = json.loads(self.post_req('user/create', {'username': 'test', 'fullname': 'Test User', 'password': 'test1234', 'superuser': False, 'editor': True}).read())
		# login as temp user
		resp = json.loads(self.post_req('user/login', {'username': 'test', 'password': 'test1234'}).read())
		tmp_id = resp['id']

		# Create Entry
		resp = self.req_create_entry('A test entry', 'This is a test entry. It is not very long. For that I am sorry.', tmp_id)
		self.assertFalse('status' in resp)

		# TODO
		# Check latest entries

		# TODO
		# Check specific entry by id

		self.admin_login()

		# Delete temp user
		resp = json.loads(self.get_req('user/delete/%d'%tmp_id).read())

