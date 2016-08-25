import uuid
import unittest
from app.api.shopify import Shopify
from app.api.models import Discount

class TestShopify(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.shopify = Shopify()

    def test_add_discount(self):
        random_code = str(uuid.uuid4())
        discount = Discount(discount_type='fixed_amount', code=random_code, value=10)
        r = self.shopify.add_discount(discount)
        self.assertEqual(r.status_code, 201)