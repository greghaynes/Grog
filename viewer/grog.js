var grog = {
	entries : {},

	get_latest_entries: function(handler, offset, count) {
		offset = typeof(offset) != 'undefined' ? offset: 0;
		count = typeof(count) != 'undefined' ? count: 0;

		if(count == 0) {
			if(offset == 0)
				$.getJSON('/entries/latest', function(data) {
					$.each(data, function(ndx, entry) { grog.entries[entry.id] = entry; });
					handler(data);
					});
			else
				$.getJSON('/entries/latest/'+offset, handler);
		} else
			$.getJSON('/entries/latest/'+offset+'/'+count, handler);
	},

	get_entry: function(entry_id, handler) {
		if(entry_id in grog.entries)
			handler(grog.entries[entry_id]);
		else
			$.getJSON('/entry/'+entry_id, handler);
	}
};


