from flask_restful import Resource


class APIInfo(Resource):
    @staticmethod
    def get():
        return {'api': {'version': 1, 'health': 'online'},
                'android': {'version': 0}
                }
