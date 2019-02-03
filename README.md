# TerraMAServer
A simple API to receive data from an Ionic app.
I'am using this technology: https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example

# Docker file to deploy

This docker is prepared to run a Flesk server used in this project. No has PostgreSQL database service. You need your our SGDB service.

### Prerequisites

Your environment to run this docker is the Docker Engine and a PostgreSQL service.

- [Docker](https://docs.docker.com/install/)
- [PostgreSQL](https://www.postgresql.org/)

### Installing

#### Database

Prepare your database using the db.sql script from here: https://raw.githubusercontent.com/andre-carvalho/TerraMAServer/master/api/storage_module/config/db.sql

#### Build your image

You may change the image version before building using the tag_version appended in image name. \
The command line template is: *docker build -t <image_name>:<tag_version> .*

Run these commands to build your image:

```sh
git clone https://github.com/andre-carvalho/TerraMAServer.git

docker build -t attempo-server:v1 -f env/Dockerfile .
```

#### Run the container

Just run the image and your service is starting. Note that command use the set env parameters to send the database connection information for API service.

* --env HOST=&lt;your ip or hostname&gt;
* --env PORT=&lt;port&gt;
* --env DBUSER=&lt;username&gt;
* --env DBPASS=&lt;secret&gt;
* --env DBNAME=&lt;database name&gt;

Note: The SERVER_DOMAIN is used to compose the data stored into the database table "Locations" into picture column. This column is used to tell for the TerraMA client the URL for one picture. The default value is "127.0.0.1:5000" and is will be valid only a local test.

* --env SERVER_DOMAIN=&lt;server_domain&gt;

```sh
docker run -p 5000:5000 -v /tmp/attempo_docker_files:/server/api/uploadImages \
--env HOST=IP --env PORT=5432 --env DBNAME=terramaapp --env DBUSER=postgres \
--env DBPASS=postgres -d attempo-server:v1
```

You may run with less parameters, like this:

```sh
docker run -p 5000:5000 -v /tmp/attempo_docker_files:/server/api/uploadImages \
--env HOST=IP --env DBNAME=dbname --env DBPASS=postgres -d attempo-server:v1
```

Or run docker accessing the terminal and set your connection informations.

To procced that, you may run the docker:

```sh
docker run -it attempo-server:v1 sh
```
And just run these commands to create the storage_module/config/db.cfg file setting your values:
```sh
echo "[database]" > storage_module/config/db.cfg
echo "host=localhost" >> storage_module/config/db.cfg
echo "port=5432" >> storage_module/config/db.cfg
echo "database=terramaapp" >> storage_module/config/db.cfg
echo "user=postgres" >> storage_module/config/db.cfg
echo "password=postgres" >> storage_module/config/db.cfg
```

You may use the docker compose to that task:

```sh
docker compose up
```

### Test

After run the server, use the command line to test:
```
curl http://127.0.0.1:5000/locations -d '{"description":"teste","lat":-23.121,"lng":-45.231,"datetime":"2018-04-02","photo":"aps897d8907an98ansd98nuasd"}' -v -H "Content-Type: application/json"
```
or use a Browser.