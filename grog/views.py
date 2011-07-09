from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json

@expose('/entries/latest/', defaults={'count': 5})
@expose('/entries/latest/<int:count>')
def latestEntries(request, count):
	return render_json(['hello', 'hello again'])

