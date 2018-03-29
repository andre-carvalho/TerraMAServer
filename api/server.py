from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('description', required=True, help="description cannot be blank!")
parser.add_argument('lat', required=True, help="lat cannot be blank!")
parser.add_argument('lng', required=True, help="lng cannot be blank!")
parser.add_argument('datetime', required=True, help="datetime cannot be blank!")
parser.add_argument('photo', required=True, help="photo cannot be blank!")

class Locations(Resource):
    def post(self):
        args = parser.parse_args()
        path = '/home/andre/Projects/TerraMAServerAPI/api/request_api.txt'
        aFile = open(path,'w')
        aFile.write(args['description'])
        aFile.write(args['lat'])
        aFile.write(args['lng'])
        aFile.write(args['datetime'])
        aFile.write(args['photo'])
        aFile.close()
        return {'status':'completed'}, 200


api.add_resource(Locations, '/locations') # Route_1


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)