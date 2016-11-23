import unittest

from app import create_app


class FoodshipTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
