import os

# SECURE_COOKIE_SECRET is a key used for secure client side only cookies
SECURE_COOKIE_SECRET = os.urandom(20)

# Password for admin user
ADMIN_PASSWORD = os.urandom(6)

# Set to false to not print admin password on startup
PRINT_ADMIN_PASSWORD = True

DB_URI = 'sqlite:////tmp/grog.db'

