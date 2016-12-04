from flask import json

from ean.FoodshipTest import FoodshipTest


class GroupTest(FoodshipTest):
    token = "albertplatz"

    def testGetGroup(self):
        rv = self.app.get("/v1/dinner/3", data=dict(
            token=self.token
        ))
        self.assertEqual(rv.status_code, 200, "Dinner should be accessible")
        answer = json.loads(rv.data.decode("utf-8"))
        self.assertEqual(answer['invited'], 4, "Invitation Number should be valid")
        self.assertEqual(answer['accepted'], 2, "Accepted Number should be valid")
        self.assertEqual(answer['day'], "2016-12-04", "Day should be valid")

        rv = self.app.get("/v1/dinner/404", data=dict(
            token=self.token
        ))
        self.assertEqual(rv.status_code, 404, "Dinner does not exist and should return 404")

        rv = self.app.get("/v1/dinner/4", data=dict(
            token=self.token
        ))
        self.assertEqual(rv.status_code, 403, "Dinner is not accessible for user, should return 300")
