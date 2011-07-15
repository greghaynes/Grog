from tests.user import CreateUser
from tests.entry import CreateEntry

import unittest

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(CreateUser)
	unittest.TextTestRunner(verbosity=2).run(suite)

