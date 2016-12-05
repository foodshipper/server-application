import os

import requests

from ean.database import db
from ean.external.recipe import classify_product

outpan_key = os.environ.get("OUTPAN_KEY")


def request_product(gtin):
    type_id = 1  # Undefined Category
    product_name = request_product_opendatasoft(gtin)
    if product_name is None:
        product_name = request_product_outpan(gtin)

    if product_name is None:
        return None

    classified = classify_product(product_name)

    if classified is not None:
        product_type, product_name = classified

        if product_type is not None and 'name' in product_type:
            with db:
                with db.cursor() as cursor:
                    print(product_type)
                    cursor.execute(
                        "SELECT id FROM product_types WHERE name LIKE %s OR product_types.image=%s",
                        ['%' + product_type['name'] + '%', product_type['image']])

                    product_type_db = cursor.fetchone()
                    if product_type_db is not None:
                        type_id = product_type_db[0]
                    else:
                        cursor.execute("INSERT INTO product_types (name, image) VALUES (%s, %s) RETURNING id",
                                       [product_type['name'], product_type['image']])
                        type_id = cursor.fetchone()[0]

    return {
        "ean": gtin,
        "name": product_name,
        "type": type_id  # Is always undefined
    }


def request_product_opendatasoft(gtin):
    req = requests.get(
        'http://pod.opendatasoft.com/api/records/1.0/search/?dataset=pod_gtin&rows=1&refine.gtin_cd={}'.format(
            gtin))
    if req.status_code == requests.codes.ok:
        product = req.json()
        if product['nhits'] == 0:
            return None
        if 'gtin_nm' not in product['records'][0]['fields']:
            return None

        return product['records'][0]['fields']['gtin_nm']
    else:
        return None


def request_product_outpan(gtin):
    req = requests.get(
        'https://api.outpan.com/v2/products/{}?apikey={}'.format(
            gtin, outpan_key))
    if req.status_code == requests.codes.ok:
        product = req.json()
        if 'name' in product:
            return product['name']
    else:
        return None
