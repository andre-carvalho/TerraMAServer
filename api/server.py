import os, base64
from flask import Flask, request, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from storage_module.locations_dao import LocationsDao
from base64_module.base64_utils import B64Utils

SERVER_IP='192.168.1.11'
IMG_PATH='/uploadImages'

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

class Locations(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        try:
            db = LocationsDao()
            id_photo = db.storeLocation(json_data)
            url_picture = "http://{0}/locations/{1}".format(SERVER_IP, id_photo)
            db.updateLocation(id_photo, url_picture)
        except Exception as error:
            print(error)
            return 500

        curpath = os.path.abspath(os.curdir) + IMG_PATH
        b64 = B64Utils(curpath, json_data['photo'])
        b64.writeToBinary(id_photo)
        
        return {'status':'completed'}, 201

class LocationsList(Resource):
     def get(self, location_id):
        
        curpath = os.path.abspath(os.curdir) + IMG_PATH
        b64 = B64Utils(curpath)
        try:
            imageio,attach,mime = b64.readFromBinary(location_id)
        except Exception as error:
            return 404
        return send_file(imageio, attachment_filename=attach, mimetype=mime)


api.add_resource(Locations, '/locations') # Route_1
api.add_resource(LocationsList, '/locations/<location_id>')


if __name__ == '__main__':
     # app.run(host='0.0.0.0', port=5000)
     app.run(host=SERVER_IP, port=5000)
     # app.run(debug=True)