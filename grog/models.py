from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Unicode, UnicodeText, ForeignKey
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

class Entry(Base):
	__tablename__ = 'entries'

	id = Column(Integer, primary_key=True)
	title = Column(Unicode)
	content = Column(UnicodeText)
	author = Column(Integer, ForeignKey('users.id'))

