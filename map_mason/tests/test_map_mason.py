import unittest

import map_mason


class Map_masonTestCase(unittest.TestCase):

    def setUp(self):
        self.app = map_mason.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to MapMason', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
