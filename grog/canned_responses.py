from werkzeug.wrappers import Response

import json

def error_json(**kwargs):
	kwargs['status'] = 'error'
	return Response(json.dumps(kwargs))

InsufficientPermissions = error_json(type='Insufficient Permissions')
NotFound = error_json(type='Not Found')
InvalidRequest = error_json(type='Invalid Request')
DuplicateError = error_json(type='Duplicate')

