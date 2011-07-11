from tests.utils import post_req, admin_login

from grog.models import User

import unittest

class CreateUser(unittest.TestCase):
	def setUp(self):
		admin_login()

	def test_create_delete(self):
		u = User('test', 'Test User', 'test1234', False, False)
		self.assertEqual(post_req('user/create', u.to_api_dict()).read(), u.to_api_dict())

