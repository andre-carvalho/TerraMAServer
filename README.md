# TerraMAServer
A simple API to receive data from a Ionic app.
I'am using this technology: https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example

## Test

After run the server, use the command line to test:
```
curl http://127.0.0.1:5000/locations -d "description=teste&lat=-23.121&lng=-45.231&datetime=2018-03-29&photo=aps897d8907an98ansd98nuasd" POST -v -H "Content-Type: application/x-www-form-urlencoded"
```
