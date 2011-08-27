from werkzeug.routing import Map, Rule

url_map = Map([
	Rule('/entries/latest', endpoint='latest_entries', defaults={'count': 5, 'offset': 0}),
	Rule('/entries/latest/<int:count>', endpoint='latest_entries', defaults={'offset': 0}),
	Rule('/entries/latest/<int:offset>/<int:count>', endpoint='latest_entries'), 
	Rule('/entry/<int:entry_id>', endpoint='single_entry'),
	Rule('/entry/delete/<int:entry_id>', endpoint='delete_entry'),
	Rule('/entry/create', endpoint='create_entry'),
	Rule('/user/profile/<int:user_id>', endpoint='user_profile'),
	Rule('/user/login', endpoint='user_login'),
	Rule('/user/logout', endpoint='user_logout'),
	Rule('/user/create', endpoint='create_user'),
	Rule('/user/delete/<int:user_id>', endpoint='delete_user'),
	Rule('/user/whoami', endpoint='whoami'),
])

