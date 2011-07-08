from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Unicode, UnicodeText, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(Unicode)
	fullname = Column(Unicode)
	password = Column(Unicode)

	entries = relationship("Entry", backref="users")

	def __init__(self, name, fullname, password):
		self.name = name
		self.fullname = fullname
		self.password = password

	def __repr__(self):
		return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

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
	                          secondary_association=entry_category_association,
	                          backref="Entries")

	comments = relationship("Comment", backref="entries")

	def __init__(self, title, content, author, created, last_updated):
		self.title = title
		self.content = content
		self.author = author
		self.created = created
		self.last_updated = last_updated

	def __repr__(self):
		return "<Entry('%s', '%s', '%s', '%s')>" % (self.title, self.content, self.author, self.created, self.last_updated)

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

