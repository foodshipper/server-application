from ean.database import db


class Product(db.Model):
    ean = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))

    def __init__(self, ean, name, type):
        self.ean = ean
        self.name = name
        self.type = type

    def __repr__(self):
        return '<Product {} {}>'.format(self.ean, self.name)
