var grogadmin = {
	is_logged_in: false,

	check_login: function(success, error) {
		$.getJSON('/user/whoami', function(data) {
			if('id' in data)
				grogadmin.is_logged_in = true;
			else
				grogadmin.is_logged_in = false;
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
					grogadmin.is_logged_in = true;
				success(data);
				},
			error: error,
			dataType: 'json'});
	},

	logout: function(success) {
		$.getJSON('/user/logout', function(data) {
			if('id' in data)
				grogadmin.is_logged_in = false;
			success(data);
		});
	},
};

