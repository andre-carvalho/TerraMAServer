import json
import requests

class APIClient:
    #constructor
    def __init__(self, URI):
        self.url="http://{0}/{1}".format(URI,"isAuthorized")
    
    def tokenValidation(self, token):
        headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)}

        response = requests.get(self.url, headers=headers)

        if response.status_code == 200:
            jsonResponse = json.loads(response.content.decode('utf-8'))
            if jsonResponse['status']=='fail':
                return None
            return jsonResponse
        else:
            return None