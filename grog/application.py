from sqlalchemy import create_engine
from werkzeug.wrappers import Request
from werkzeug.wsgi import ClosingIterator
from werkzeug.exceptions import HTTPException

from grog.utils import session, metadata, local, local_manager, url_map
from grog import views

class Grog(object):
	def __init__(self, db_uri):
		local.application = self
		self.database_engine = create_engine(db_uri, convert_unicode=True)
	def init_database(self):
		metadata.create_all(self.database_engine)
	def __call__(self, environ, start_response):
		local.application = self
		request = Request(environ)
		local.url_adapter = adapter = url_map.bind_to_environ(environ)
		try:
			endpoint, values = adapter.match()
			handler = getattr(views, endpoint)
			response = handler(request, **values)
		except HTTPException, e:
			response = e
		return ClosingIterator(response(environ, start_response),
						   [session.remove, local_manager.cleanup])

