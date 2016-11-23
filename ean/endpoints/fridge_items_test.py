from flask import json

from FoodshipTest import FoodshipTest


class ProductTest(FoodshipTest):
    user_id = "TEST_TEST_TEST"

    def testGetItems(self):
        rv = self.app.get("/v1/items", data=dict(
            user_id=self.user_id
        ))
        self.assertEqual(rv.status_code, 200, "Item Overview should return a 200 Response")

        rv = self.app.get("/v1/items")
        self.assertEqual(rv.status_code, 400, "Item Overview should return a 400 Response without user_id")

    def testPutItem(self):
        rv = self.app.put("/v1/items/4000406071242", data=dict(
            user_id=self.user_id
        ))
        answer = json.loads(rv.data.decode("utf-8"))
        self.assertIn(rv.status_code, [200, 201], "PUT Item should return 201 Created or 200 Updated")
        self.assertIn("name", answer, "PUT Response should contain item name")
        self.assertIn("type", answer, "PUT Response should contain item type")

    def testDeleteItem(self):
        self.app.put("/v1/items/4000406071242", data=dict(
            user_id=self.user_id
        ))
        rv = self.app.delete("/v1/items/4000406071242", data=dict(
            user_id=self.user_id
        ))
        self.assertIn(rv.status_code, [200, 202, 204], "DELETE Response Code should be 20(0|2|4)")

        rv = self.app.delete("/v1/items/4000406071242", data=dict(
            user_id=self.user_id
        ))
        self.assertIn(rv.status_code, [404], "DELETE Response Code should be 404 if now item exists")

        rv = self.app.get("/v1/items", data=dict(
            user_id=self.user_id
        ))
        answer = rv.data.decode("utf-8")
        self.assertNotIn("4000406071242", answer, "Item Overview should not contain EAN that was deleted")
