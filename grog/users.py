from sqlalchemy.orm.exc import NoResultFound

from grog.models import User, ConfigOption
from grog.canned_responses import InsufficientPermissions
from grog.utils import session
from grog.settings import PASSWORD_HASH_FUNC

import os
import logging
from base64 import b64encode

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

class superuser_only(object):
	def __init__(self, f):
		self.f = f
		self.__name__ = f.__name__
	def __call__(self, request, *args, **kwargs):
		# handle admin
		try:
			is_admin = int(request.client_session['user_id']) == -1
		except KeyError:
			pass
		if is_admin:
			return self.f(request, *args, **kwargs)

		# check db
		try:
			user = session.query(User).filter(User.id==request.client_session['user_id']).one()
			if not user.superuser:
				return InsufficientPermissions
		except KeyError:
			return InsufficientPermissions
		except NoResultFound:
			logging.debug('Invalid user ID (%d) supplied in valid cookie' % request.client_session['user_id'])
		return self.f(request, *args, **kwargs)

def password_salt():
	try:
		salt = session.query(ConfigOption.value).filter(ConfigOption.key=='password_salt').one().value
	except NoResultFound:
		salt = b64encode(os.urandom(16))
		co = ConfigOption('password_salt', salt)
		session.add(co)
	return salt

hash_password = lambda password: PASSWORD_HASH_FUNC(password_salt() + password)

