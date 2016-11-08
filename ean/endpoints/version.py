class APIInfo():
    @staticmethod
    def get():
        return {'api': {'version': 1, 'health': 'good'},
                'android': {'version': 0}
                }
