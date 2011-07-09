from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json, session
from grog.models import Entry

from collections import deque

@expose('/entries/latest/', defaults={'count': 5})
@expose('/entries/latest/<int:count>')
def latestEntries(request, count):
	return render_json([entry.to_api_dict() for entry in session.query(Entry).order_by(Entry.created)[:count]])

