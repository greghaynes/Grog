from sqlalchemy.orm.exc import NoResultFound

from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json, session, handle_notfound, needs_post_args
from grog.models import Entry, User, Comment
from grog.users import editor_only, superuser_only, user_only, hash_password
from grog.settings import ADMIN_PASSWORD
from grog.canned_responses import DuplicateError

def latest_entries(request, count):
	return render_json([entry.to_api_dict() for entry in session.query(Entry).order_by(Entry.created).limit(count)])

@handle_notfound
def single_entry(request, entry_id):
	entry_dict = session.query(Entry).filter(Entry.id==entry_id).one().to_api_dict()
	entry_dict['comments'] = [comment.to_api_dict() for comment in session.query(Comment).filter(Comment.entry==entry_id).order_by(Comment.created)]
	return render_json(entry_dict)

@editor_only
@handle_notfound
def delete_entry(request, entry_id):
	session.query(Entry).filter(Entry.id==entry_id).delete()
	session.commit()

@editor_only
@needs_post_args('title', 'content')
def create_entry(request):
	e = Entry(request.form['title'], request.form['content'], request.user.id)
	session.add(e)
	session.commit()
	return render_json(e.to_api_dict())

@handle_notfound
def user_profile(request, user_id):
	return render_json(session.query(User).filter(User.id==user_id).one().to_api_dict())

@handle_notfound
@needs_post_args('username', 'password')
def user_login(request):
	if request.form['username'] == 'admin' and request.form['password'] == ADMIN_PASSWORD:
		request.client_session['user_id'] = -1
		return render_json({'id': -1, })
	user = session.query(User).filter(User.username==request.form['username']).filter(User.password==hash_password(request.form['password'])).one()
	request.client_session['user_id'] = user.id
	return render_json(user.to_api_dict())

@user_only
def user_logout(request):
	user_id = request.client_session['user_id']
	del request.client_session['user_id']
	return render_json({'id': user_id})

@superuser_only
@needs_post_args('username', 'password', 'fullname', 'superuser', 'editor')
def create_user(request):
	try:
		u = session.query(User.username==request.form['username']).one()
		return DuplicateError
	except NoResultFound:
		pass
	u = User(request.form['username'], request.form['fullname'], hash_password(request.form['password']), request.form['editor'] == 'True', request.form['superuser'] == 'True')
	session.add(u)
	session.commit()
	u = session.query(User).filter(User.username==request.form['username']).one()
	return render_json(u.to_api_dict())

@superuser_only
@handle_notfound
def delete_user(request, user_id):
	session.query(User).filter(User.id==user_id).delete()
	session.commit()
	return render_json({'id': user_id})

@user_only
def whoami(request):
	return render_json({'id': request.client_session['user_id']})

