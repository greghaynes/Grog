from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json, session, handle_notfound, needs_post_args
from grog.models import Entry, User
from grog.users import editor_only, superuser_only, hash_password
from grog.settings import ADMIN_PASSWORD

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
	return render_json(e.to_api_dict())

@expose('/user/profile/<int:user_id>')
@handle_notfound
def user_profile(request, user_id):
	return render_json(session.query(User).filter(User.id==user_id).one().to_api_dict())

@expose('/user/login')
@handle_notfound
@needs_post_args('username', 'password')
def user_login(request):
	if request.form['username'] == 'admin' and request.form['password'] == ADMIN_PASSWORD:
		request.client_session['user_id'] = -1
		return render_json({'id': -1, })
	user = session.query(User).filter(User.username==request.form['username']).filter(User.password==hash_password(request.form['password'])).one()
	request.client_session['user_id'] = user.id
	return render_json(user.to_api_dict())

@expose('/user/create')
@superuser_only
@needs_post_args('username', 'password', 'fullname', 'superuser', 'editor')
def create_user(request):
	u = User(request.form['username'], request.form['fullname'], request.form['password'], bool(request.form['editor']), bool(request.form['superuser']))
	session.add(u)
	session.commit()
	u = session.query(User).filter(User.username==request.form['username']).one()
	return render_json(u.to_api_dict())

@expose('/user/delete/<int:user_id>')
@superuser_only
@handle_notfound
def delete_user(request, user_id):
	session.query(User.id==user_id).delete()
	session.commit()
	return render_json({'id': user_id})

