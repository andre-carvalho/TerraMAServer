import os, base64
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from storage_module.locations_dao import LocationsDao
from base64_module.base64_utils import B64Utils

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

class Locations(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        id_photo = json_data['datetime']

        try:
            db = LocationsDao()
            id_photo = db.storeLocation(json_data)
        except Exception as error:
            print(error)
            return 500

        curpath = os.path.abspath(os.curdir)
        b64 = B64Utils(curpath, json_data['photo'])
        b64.writeToBinary(id_photo)
        
        return {'status':'completed'}, 201


api.add_resource(Locations, '/locations') # Route_1


if __name__ == '__main__':
     # app.run(host='0.0.0.0', port=5000)
     app.run(debug=True)