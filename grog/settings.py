import os
import hashlib
import logging

# SECURE_COOKIE_SECRET is a key used for secure client side only cookies
SECURE_COOKIE_SECRET = os.urandom(20)

# Password for admin user
ADMIN_PASSWORD = 'grogadmin'

# URI for database
DB_URI = 'sqlite:////tmp/grog.db'

# Hash function used for password storage
PASSWORD_HASH_FUNC = lambda passwd: hashlib.sha256(passwd).hexdigest()

logging.basicConfig(level='DEBUG')

