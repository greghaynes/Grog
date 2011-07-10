from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json, session, handle_notfound, needs_post_args
from grog.models import Entry, User
from grog.users import editor_only, hash_password

@expose('/entries/latest/', defaults={'count': 5})
@expose('/entries/latest/<int:count>')
def latest_entries(request, count):
	return render_json([entry.to_api_dict() for entry in session.query(Entry).order_by(Entry.created).limit(count)])

@expose('/entries/create')
@editor_only
@needs_post_args('title', 'content')
def create_entry(request):
	e = Entry(request['title'], request['content'], request.user.id)
	session.add(e)

@expose('/user/profile/<int:user_id>')
@handle_notfound
def user_profile(request, user_id):
	return render_json(session.query(User).filter(User.id==user_id).one().to_api_dict())

@expose('/user/login')
@handle_notfound
@needs_post_args('username', 'password')
def user_login(request):
	request.client_session['user_id'] = session.query(User.id).filter(User.username==request.args['username']).filter(User.password==hash_password(request.args['password'])).one().id

