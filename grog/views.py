from sqlalchemy.orm.exc import NoResultFound

from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from grog.utils import expose, render_json, session, handle_notfound, needs_post_args
from grog.models import Entry, User, Comment
from grog.users import editor_only, superuser_only, user_only, hash_password
from grog.settings import ADMIN_PASSWORD
from grog.canned_responses import DuplicateError

import logging
import datetime

def latest_entries(request, count, offset):
	return render_json([entry.to_api_dict() for entry in session.query(Entry).order_by(Entry.created).offset(offset).limit(count)])

@handle_notfound
def single_entry(request, entry_id):
	entry_dict = session.query(Entry).filter(Entry.id==entry_id).one().to_api_dict()
	entry_dict['comments'] = [comment.to_api_dict() for comment in session.query(Comment).filter(Comment.entry==entry_id).order_by(Comment.created)]
	return render_json(entry_dict)

@handle_notfound
@needs_post_args('title', 'content', 'author_fullname', 'author_email', 'author_website')
def comment_create(request):
	c = Comment(request.form['title'], request.form['author_fullname'], request.form['author_email'], request.form['author_website'], datetime.datetime.now().isoformat(), request.form['content'])
	session.add(c)
	session.commit()
	return render_json(c.to_api_dict())

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
	if user_id == -1:
		user = User('admin', 'Administrator User', '', False, True, True)
		user.id = -1
		return render_json(user.to_api_dict())
	return render_json(session.query(User).filter(User.id==user_id).one().to_api_dict())

@handle_notfound
@needs_post_args('username', 'password')
def user_login(request):
	if request.form['username'] == 'admin' and request.form['password'] == ADMIN_PASSWORD:
		request.client_session['user_id'] = -1
		return user_profile(request, -1)
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
		u = session.query(User).filter(User.username==request.form['username']).one()
		logging.debug("Not creating user %s, username already in use." % request.form['username'])
		return DuplicateError
	except NoResultFound:
		pass
	u = User(request.form['username'], request.form['fullname'], hash_password(request.form['password']), request.form['editor']=='true', request.form['superuser']=='true')
	# handle query errors and return a valid response
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
	return user_profile(request, request.client_session['user_id'])

@superuser_only
def users_list(request, count, offset):
	user_q = session.query(User).order_by(User.username).offset(offset).limit(count)
	users_list = [u.to_api_dict() for u in user_q]
	print users_list
	return render_json(users_list)

