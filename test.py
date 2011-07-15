from tests.user import CreateUser
from tests.entry import CreateEntry

import unittest

if __name__ == '__main__':
	suitegens = (CreateUser, CreateEntry)
	for gen in suitegens:
		suite = unittest.TestLoader().loadTestsFromTestCase(gen)
		unittest.TextTestRunner(verbosity=2).run(suite)

