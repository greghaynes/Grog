from sqlalchemy import MetaData
from sqlalchemy.orm import create_session, scoped_session
from sqlalchemy.orm.exc import NoResultFound

from werkzeug.local import Local, LocalManager
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

from grog.canned_responses import NotFound, InvalidRequest

import json
import logging

local = Local()
local_manager = LocalManager([local])
application = local('application')

metadata = MetaData()
session = scoped_session(lambda: create_session(application.database_engine,
                         autocommit=False, autoflush=False),
                         local_manager.get_ident)

url_map = Map()
def expose(rule, **kw):
	def decorate(f):
		kw['endpoint'] = f.__name__
		url_map.add(Rule(rule, **kw))
		return f
	return decorate

class handle_notfound(object):
	def __init__(self, f):
		self.f = f
		self.__name__ = f.__name__
	def __call__(self, *args, **kwargs):
		try:
			return self.f(*args, **kwargs)
		except NoResultFound:
			return NotFound

class needs_post_args(object):
	def __init__(self, *args):
		self.args = args
	def __call__(self, f):
		self.f = f
		def decorate(request, *args, **kwargs):
			if request.method != 'POST':
				logging.debug('Required POST, got %s' % request.method)
				return InvalidRequest
			for arg in self.args:
				if not arg in request.form:
					return InvalidRequest
			return f(request, *args, **kwargs)
		decorate.__name__ = f.__name__
		return decorate

def render_json(data):
	return Response(json.dumps(data), mimetype='application/json')

