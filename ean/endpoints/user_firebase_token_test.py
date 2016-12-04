from flask import json

from ean.FoodshipTest import FoodshipTest


class TestUserFirebaseToken(FoodshipTest):
    token = "TEST"
    firebase_token = "823n4v25829m30b"

    def test_put(self):
        rv = self.app.put("/v1/user/firebase-token", data=dict(
            token=self.token,
        ))

        self.assertEqual(rv.status_code, 400, "Firebase Token is missing, should get HTTP 400: Invalid Arguments")

        rv = self.app.put("/v1/user/firebase-token", data=dict(
            token=self.token,
            firebase_token=self.firebase_token
        ))

        self.assertEqual(rv.status_code, 200, "PUT with valid ID and Firebase token should return HTTP 200")