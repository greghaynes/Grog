from sqlalchemy import MetaData
from sqlalchemy.orm import create_session, scoped_session

from werkzeug.local import Local, LocalManager
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

import json

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

def render_json(data):
	return Response(json.dumps(data), mimetype='application/json')

