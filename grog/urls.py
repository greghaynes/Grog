from werkzeug.routing import Map, Rule

url_map = Map([
	Rule('/entry/latest', endpoint='latest_entries', defaults={'count': 5}),
	Rule('/entries/latest/<int:count>', endpoint='latest_entries'),
	Rule('/entry/<int:entry_id>', endpoint='single_entry'),
])

