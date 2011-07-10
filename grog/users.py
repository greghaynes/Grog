from sqlalchemy.orm.exc import NoResultFound

from grog.models import User, ConfigOption
from grog.canned_responses import InsufficientPermissions
from grog.utils import session
from grog.settings import PASSWORD_HASH_FUNC

import os

def is_admin(user_id):
	return False

class editor_only(object):
	def __init__(self, f):
		self.f = f
		self.__name__ = f.__name__
	def __call__(self, request, *args, **kwargs):
		try:
			user = session.query(User).filter(User.id==request.client_session['user_id']).one()
			if not user.editor:
				return InsufficientPermissions
		except (KeyError, NoResultFound):
			return InsufficientPermissions
		request.user = user
		return self.f(request, *args, **kwargs)

class admin_only(object):
	def __init__(self, f):
		self.f = f
		self.__name__ = f.__name__
	def __call__(self, request, *args, **kwargs):
		try:
			if not is_admin(request.client_session['user_id']):
				return InsufficientPermissions
		except KeyError:
			return InsufficientPermissions
		return self.f(request, *args, **kwargs)

def password_salt():
	try:
		salt = session.query(ConfigOption.value).filter(ConfigOption.name=='password_salt').one().value
	except NoResultFound:
		salt = os.urandom(16)
		co = ConfigOption('password_salt', salt)
		session.add(co)
	return salt

hash_password = lambda password: PASSWORD_HASH_FUNC(password_salt() + password)

