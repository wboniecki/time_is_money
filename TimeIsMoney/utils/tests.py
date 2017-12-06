from django.test import TestCase
from .utils import Utils

# Create your tests here.

class UtilsTest(TestCase):
    def unifyPriceTest(self):
        utils = Utils()

        self.assertEqual(utils.unifyPrice("12339999"), 1233.9999)

