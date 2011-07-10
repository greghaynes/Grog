from grog.models import User
from grog.canned_responses import InsufficientPermissions

def is_admin(user_id):
	return False

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

