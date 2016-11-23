from flask import json

from ean.FoodshipTest import FoodshipTest


class TestUserName(FoodshipTest):
    token = "TEST"
    name = "testname"

    def test_put(self):
        rv = self.app.put("/v1/user/name", data=dict(
            token=self.token,
        ))

        self.assertEqual(rv.status_code, 400, "Name is missing, should get HTTP 400: Invalid Arguments")

        rv = self.app.put("/v1/user/name", data=dict(
            token=self.token,
            name=self.name
        ))

        self.assertEqual(rv.status_code, 200, "PUT with valid ID and name should return HTTP 200")

    def test_get(self):
        rv = self.app.put("/v1/user/name", data=dict(
            token=self.token,
            name=self.name
        ))

        self.assertEqual(rv.status_code, 200, "PUT with valid ID and name should return HTTP 200")

        rv = self.app.get("/v1/user/name", data=dict(
            token=self.token
        ))
        self.assertEqual(rv.status_code, 200, "GET username should return valid username")
        self.assertEqual(json.loads(rv.data.decode("utf-8"))['name'], self.name, "GET should return correct Username")



