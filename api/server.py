import os
import json
from flask import Flask, request, send_from_directory
from flask_restful import abort, Api, Resource
from werkzeug.utils import secure_filename
from flask_cors import CORS
from storage_module.locations_dao import LocationsDao
from logs_module.log_writer import logWriter
from authorization.api_client import APIClient

UPLOAD_FOLDER = '/uploadImages'
LOG_PATH='/logs'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

SERVER_IP='0.0.0.0'
SERVER_DOMAIN=os.getenv('SERVER_DOMAIN', '127.0.0.1:5000')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(__file__) + UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


class PhotoInput(Resource):
    
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def post(self):
        # check if Authorization header is present and if it is valid
        request.headers.get('Authorization')
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
                 # call the Authentication API
                #oAuth = APIClient(SERVER_DOMAIN)
                oAuth = APIClient("192.168.1.121:5000")
                auth=oAuth.tokenValidation(auth_token)
                if auth is None:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Unauthorized'
                    }
                    return responseObject, 401
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return responseObject, 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Missing token.'
            }
            return responseObject, 401
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            # No file part
            error_msg = 'Error in PhotoUpload class when trying test the file part from request. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'parse error'}, 500
        file = request.files['file']

        user_id = "uncategorized"
        filename = ""
        if 'json_data' in request.form:
            json_data = request.form['json_data']
            # parse JSON:
            aJson = json.loads(json_data)
            user_id = str(aJson["userid"])
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or user_id == '':
            error_msg = 'Error in PhotoUpload class when trying read the filename. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'parse error'}, 500
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.isdir(app.config['UPLOAD_FOLDER'] + '/' +user_id):
                os.mkdir(app.config['UPLOAD_FOLDER'] + '/' +user_id)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+ '/' +user_id, filename))

        # trying store data into database
        try:
            db = LocationsDao()
            entry_id = db.storeLocation(aJson)
            url_picture = "http://{0}/locations/{1}/{2}".format(SERVER_DOMAIN, user_id, filename)
            db.updateLocation(entry_id, url_picture)
        except Exception as error:
            error_msg = 'Error in PhotoUpload class when trying store posted data. Return HTTP:500'
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'database error'}, 500
        # everything is ok
        return {'status':'completed'}, 201
        

class PhotoOutput(Resource):
    def get(self, user_id, filename):
        dir=os.path.join(app.config['UPLOAD_FOLDER'], user_id)
        # trying read picture from disk and send to client
        try:
            if os.path.isfile(dir+'/'+filename):
                return send_from_directory(dir, filename, as_attachment=False)
            else:
                abort(404)
        except Exception as error:
            error_msg = 'Error in PhotoUpload class when trying read the filename. Return HTTP:500'
            error_msg = error_msg+'\n'+str(error)
            logWriter(os.path.abspath(os.curdir) + LOG_PATH).write(error_msg)
            return {'status': 'file not found'}, 404

# receive the JSON data together pictures
api.add_resource(PhotoInput, '/occurrences')
api.add_resource(PhotoOutput, '/occurrences/<user_id>/<filename>')


if __name__ == '__main__':
     app.run(host=SERVER_IP, port=5000)