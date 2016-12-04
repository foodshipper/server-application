from ean.app import create_app
from ean.database import install_testdata
import unittest


class FoodshipTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        install_testdata()
