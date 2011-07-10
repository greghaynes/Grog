from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json, session, handle_notfound
from grog.models import Entry, User
from grog.users import admin_only

@expose('/entries/latest/', defaults={'count': 5})
@expose('/entries/latest/<int:count>')
def latest_entries(request, count):
	return render_json([entry.to_api_dict() for entry in session.query(Entry).order_by(Entry.created)[:count]])

@handle_notfound
@expose('/user/profile/<int:user_id>')
def user_profile(request, user_id):
		return render_json(session.query(User).filter_by(id=user_id).one().to_api_dict())

@expose('/entries/create')
def create_entry(request):
	pass

