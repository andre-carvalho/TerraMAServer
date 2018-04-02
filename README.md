# TerraMAServer
A simple API to receive data from a Ionic app.
I'am using this technology: https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example

## Test

After run the server, use the command line to test:
```
curl http://127.0.0.1:5000/locations -d '{"description":"teste","lat":-23.121,"lng":-45.231,"datetime":"2018-04-02","photo":"aps897d8907an98ansd98nuasd"}' POST -v -H "Content-Type: application/json"
```

# Docker file to deploy

This docker is prepared to run a Flesk server used in this project. No has PostgreSQL database service. You need your our SGDB service.

### Prerequisites

Your environment to run this docker is the Docker Engine and a PostgreSQL service.

- [Docker](https://docs.docker.com/install/)
- [PostgreSQL](https://www.postgresql.org/)

### Installing

#### Build your image

Run these commands to build your image:

```sh
git clone https://github.com/andre-carvalho/TerraMAServer.git

docker build -t vita3server .
```

#### Run the container

Just run the image and your service is starting. Note that command use the set env parameters to send the database connection information for vita3server service.

* --env HOST=&lt;your ip or hostname&gt;
* --env PORT=&lt;port&gt;
* --env DBUSER=&lt;username&gt;
* --env DBPASS=&lt;secret&gt;
* --env DBNAME=&lt;database name&gt;

```sh
docker run --env HOST=IP --env PORT=5432 --env DBNAME=terramaapp --env DBUSER=postgres --env DBPASS=postgres -d vita3server
```

You may run with less parameters, like this:

```sh
docker run --env HOST=IP --env DBNAME=dbname --env DBPASS=postgres -d vita3server
```

Or run docker accessing the terminal and set your connection informations.

To procced that, you may run the docker:

```sh
docker run -it vita3server sh
```
And just run these commands to create the storage_module/config/db.cfg file setting your values:
```sh
echo "[postgresql]" > storage_module/config/db.cfg
echo "host=localhost" >> storage_module/config/db.cfg
echo "port=5432" >> storage_module/config/db.cfg
echo "database=bitcointoyou" >> storage_module/config/db.cfg
echo "user=postgres" >> storage_module/config/db.cfg
echo "password=postgres" >> storage_module/config/db.cfg
```
