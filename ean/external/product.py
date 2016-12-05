import os

import requests

outpan_key = os.environ.get("OUTPAN_KEY")


def request_product(gtin):
    product_name = request_product_opendatasoft(gtin)
    if product_name is None:
        product_name = request_product_outpan(gtin)

    if product_name is None:
        return None

    return {
        "ean": gtin,
        "name": product_name,
        "type": 1  # Is always undefined
        # TODO: Add Product Type recognition from recipe API
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
        print(product['name'])
        if 'name' in product:
            return product['name']
    else:
        return None
