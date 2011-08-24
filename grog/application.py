from sqlalchemy import create_engine
from werkzeug.utils import cached_property
from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import ClosingIterator
from werkzeug.exceptions import HTTPException
from werkzeug.contrib.securecookie import SecureCookie

from grog.utils import session, metadata, local, local_manager
from grog.urls import url_map
from grog.settings import SECURE_COOKIE_SECRET, DB_URI
from grog import views
import grog.models


class Request(BaseRequest):
	@cached_property
	def client_session(self):
		data = self.cookies.get('session_data')
		if not data:
			return SecureCookie(secret_key=SECURE_COOKIE_SECRET)
		return SecureCookie.unserialize(data, SECURE_COOKIE_SECRET)

class Grog(object):
	def __init__(self, db_uri=DB_URI):
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

		if request.client_session.should_save:
			session_data = request.client_session.serialize()
			response.set_cookie('session_data', session_data,
			                    httponly=True)
		return ClosingIterator(response(environ, start_response),
						   [session.remove, local_manager.cleanup])

