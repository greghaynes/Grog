var grogadmin = {
	is_logged_in: false,
	is_editor: false,
	is_superuser: false,

	reset_user: function() {
		grogadmin.is_logged_in = false;
		grogadmin.is_editor = false;
		grogadmin.is_superuser = false;
	},

	load_user: function(user) {
		grogadmin.is_logged_in = user.active;
		grogadmin.is_editor = user.editor;
		grogadmin.is_superuser = user.superuser;
	},

	check_login: function(success, error) {
		$.getJSON('/user/whoami', function(data) {
			if('id' in data)
				grogadmin.load_user(data);
			else
				grogadmin.reset_user();
			success(data);
		}, error);
	},

	login: function(username, password, success, error) {
		$.ajax({
			type: 'POST',
			url: '/user/login',
			data: {'username': username, 'password': password},
			success: function(data) {
				if('id' in data)
					grogadmin.load_user(data);
				success(data);
				},
			error: error,
			dataType: 'json'});
	},

	logout: function(success) {
		$.getJSON('/user/logout', function(data) {
			if('id' in data)
				grogadmin.reset_user();
			success(data);
		});
	},

	create_entry: function(title, content, success_handler, error_handler) {
		$.ajax({
			type: 'POST',
			url: '/entry/create',
			data: {'title': title, 'content': content},
			success: function(data) {
				if('id' in data)
					success_handler(data);
				else
					error_handler(data);
				},
			error: error_handler,
			dataType: 'json'
		});
	},

	users_list: function(success, error) {
		$.getJSON('/users/list', function(data) {
			if('type' in data)
				error(data);
			else
				success(data);
			},
			error);
	},
};

