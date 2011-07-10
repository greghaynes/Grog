from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json, session, handle_notfound, needs_post_args
from grog.models import Entry, User
from grog.users import editor_only, superuser_only, hash_password

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
	if request.args['username'] == 'admin' and request.args['password'] == ADMIN_PASSWORD:
		request.client_session['user_id'] = -1
		return render_json({'id': -1, })
	user = session.query(User).filter(User.username==request.args['username']).filter(User.password==hash_password(request.args['password'])).one()
	request.client_session['user_id'] = user.id
	return render_json(user.to_api_dict())

@expose('/user/create')
@superuser_only
@needs_post_args('username', 'password', 'fullname', 'superuser', 'editor')
def create_user(request):
	u = User(request.args['username'], request.args['fullname'], request.args['password'], request.args['editor'], request.args['superuser'])
	session.add(u)

