from sqlalchemy import Column, Table, Integer, Unicode, UnicodeText, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from grog.utils import metadata

from datetime import datetime

Base = declarative_base(metadata=metadata)

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(Unicode, unique=True)
	fullname = Column(Unicode)
	password = Column(Unicode)
	superuser = Column(Boolean)
	editor = Column(Boolean)
	active = Column(Boolean)

	entries = relationship("Entry", backref="users")

	def __init__(self, username, fullname, password, editor=True, superuser=False, active=True):
		self.username = username
		self.fullname = fullname
		self.password = password
		self.editor = editor
		self.superuser = superuser
		self.active = active

	def __repr__(self):
		return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

	def to_api_dict(self):
		return {
			'id': self.id,
			'username': self.username,
			'fullname': self.fullname,
			'superuser': self.superuser,
			'active': self.active,
			'editor': self.editor }

entry_category_association = Table('entry_category', Base.metadata,
	Column('entry_id', Integer, ForeignKey('entries.id')),
	Column('category_id', Integer, ForeignKey('categories.id'))
)

class Entry(Base):
	__tablename__ = 'entries'

	id = Column(Integer, primary_key=True)
	title = Column(Unicode)
	content = Column(UnicodeText)
	author = Column(Integer, ForeignKey('users.id'))
	created = Column(DateTime)
	last_updated = Column(DateTime)

	categories = relationship("Category",
	                          secondary=entry_category_association,
	                          backref="Entries")

	comments = relationship("Comment", backref="entries")

	def __init__(self, title, content, author, created=None, last_updated=None):
		self.title = title
		self.content = content
		self.author = author
		self.created = created or datetime.utcnow()
		self.last_updated = last_updated or datetime.utcnow()

	def __repr__(self):
		return "<Entry('%s', '%s', '%s', '%s')>" % (self.title, self.content, self.author, self.created, self.last_updated)

	def to_api_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'content': self.content,
			'author': self.author,
			'created': self.created.isoformat(),
			'last_updated': self.last_updated.isoformat() }

class Comment(Base):
	__tablename__ = 'comments'

	id = Column(Integer, primary_key=True)
	entry = Column(Integer, ForeignKey('entries.id'))
	title = Column(Unicode)
	author_fullname = Column(Unicode)
	author_email = Column(Unicode)
	author_website = Column(Unicode)
	created = Column(DateTime)
	content = Column(UnicodeText)

	def __init__(self, title, author_fullname, author_email, author_website, created, content):
		this.title = title
		this.author_fullname = author_fullname
		this.author_email = author_email
		this.author_website = author_website
		this.created = created
		this.content = content

	def __repr__(self):
		return "<Comment('%s', '%s', '%s', '%s', '%s', '%s')>" % (this.title, this.author_fullname, this.author_email, this.author_website, this.created, this.content)

	def to_api_dict(self):
		return {
			'id': self.id,
			'entry_id': self.entry,
			'title': self.title,
			'author_fullname': self.author_fullname,
			'author_email': self.author_email,
			'self.author_website': self.author_website,
			'created': self.created.isoformat() }

class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	name = Column(Unicode)
	description = Column(Unicode)

	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return "<Category('%s', '%s')>" % (self.name, self.description)

class ConfigOption(Base):
	__tablename__ = 'config_options'

	id = Column(Integer, primary_key=True)
	key = Column(Unicode)
	value = Column(Unicode)

	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __repr__(self):
		return "<ConfigOption('%s', '%s')>" % (self.key, self.value)

