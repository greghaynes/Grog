var grog = {
	getLatestEntries: function(handler, offset, count) {
		offset = typeof(offset) != 'undefined' ? offset: 0;
		count = typeof(count) != 'undefined' ? count: 0;

		if(count == 0) {
			if(offset == 0)
				$.getJSON('/entries/latest', handler);
			else
				$.getJSON('/entries/latest/'+offset, handler);
		} else
			$.getJSON('/entries/latest/'+offset+'/'+count, handler);
	},

	getEntry: function(entry_id, handler) {
		$.getJSON('/entry/'+entry_id, handler);
	}
};

