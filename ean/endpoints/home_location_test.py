from ean.FoodshipTest import FoodshipTest


class HomeLocationTest(FoodshipTest):
    user_id = "TEST"

    def test_put(self):
        rv = self.app.put("/v1/home-location", data=dict(
            user_id=self.user_id,
            lon=0,
            lat=0
        ))
        self.assertIn(rv.status_code, [200, 201], "Home Location should Create or Update Resource!")

