from app import create_app
import unittest


class FoodshipTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
