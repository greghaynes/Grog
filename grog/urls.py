from werkzeug.routing import Map, Rule

url_map = Map([
	# Entry
	Rule('/entries/latest', endpoint='latest_entries', defaults={'count': 5, 'offset': 0}),
	Rule('/entries/latest/<int:count>', endpoint='latest_entries', defaults={'offset': 0}),
	Rule('/entries/latest/<int:offset>/<int:count>', endpoint='latest_entries'), 
	Rule('/entry/<int:entry_id>', endpoint='single_entry'),
	Rule('/entry/<int:entry_id>/comment/create', endpoint='comment_create'),

	# Entry Admin
	Rule('/entry/delete/<int:entry_id>', endpoint='delete_entry'),
	Rule('/entry/create', endpoint='create_entry'),

	# User viewing
	Rule('/user/profile/<int:user_id>', endpoint='user_profile'),
	Rule('/user/login', endpoint='user_login'),
	Rule('/user/whoami', endpoint='whoami'),

	# User Actions
	Rule('/user/logout', endpoint='user_logout'),

	# User admin
	Rule('/users/list', endpoint='users_list', defaults={'count': 5, 'offset': 0}),
	Rule('/users/list/<int:count>', endpoint='users_list', defaults={'offset': 0}),
	Rule('/users/list/<int:offset>/<int:count>', endpoint='users_list'),
	Rule('/user/create', endpoint='create_user'),
	Rule('/user/delete/<int:user_id>', endpoint='delete_user'),
])

