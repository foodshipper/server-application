from flask import json

from ean.FoodshipTest import FoodshipTest


class ProductTest(FoodshipTest):
    def testGetProduct(self):
        # Get unknown product
        rv = self.app.get("/v1/product/123")
        self.assertEqual(rv.status_code, 404, "Product with EAN 123 should not be found")
        self.assertGreater(len(rv.data), 10, "JSON encoded Error Message should be longer then 10 characters")

        # Get known product
        rv = self.app.get("/v1/product/4000406071242")
        self.assertEqual(rv.status_code, 200, "Product with EAN 4000406071242 should be found")
        answer = json.loads(rv.data.decode("utf-8"))

        self.assertIn("Mehl", answer['name'], "Product Response should return the correct name")

    def testPutProduct(self):
        exist_rq = self.app.get("/v1/product/321")

        type_rq = self.app.get("/v1/types")
        product_types = json.loads(type_rq.data.decode("utf-8"))

        rv = self.app.put("/v1/product/321", data=dict(
            name="TestCase Product",
            type=product_types[0]['id']
        ))

        if exist_rq.status_code == 404:
            self.assertEqual(rv.status_code, 201, "PUT Operation should create new entry")
        else:
            self.assertEqual(rv.status_code, 200, "PUT Operation should override existing entry")

        rv = self.app.put("/v1/product/321", data=dict(
            name="Product that should fail",
            type="gibberish"
        ))
        self.assertNotIn("gibberish", product_types, "Product Types should not contain gibberish")
        self.assertEqual(rv.status_code, 400, "PUT Operation should fail with unknown product type")


    def testProductTypes(self):
        rv = self.app.get("/v1/types")
        self.assertEqual(rv.status_code, 200, "Types Overview shout return 200")
        self.assertGreater(len(json.loads(rv.data.decode("utf-8"))), 0, "There should be at least 1 product type")
