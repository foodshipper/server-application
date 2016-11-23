from ean.FoodshipTest import FoodshipTest


class HomeLocationTest(FoodshipTest):
    token = "TEST"

    def test_put(self):
        rv = self.app.put("/v1/user/home-location", data=dict(
            token=self.token,
            lon=0,
            lat=0
        ))
        self.assertIn(rv.status_code, [200, 201], "Home Location should Create or Update Resource!")

