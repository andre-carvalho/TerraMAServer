
## virtualenv

### Configuration file

nano ~/.virtualenv/virtualenv.ini

```sh

# create virtual env inside a pwd path
virtualenv env

# use one python version
virtualenv --python=/usr/bin/python3 env

# to activate the virtual env
source env/bin/activate

# to leave
deactivate

```

## To run using gunicorn use:

Pay atention, do not use the eventlet worker class "-k eventlet". It's break the connection before the response was sent to client.

```sh
# use only on localhost
gunicorn -w 1 -b 127.0.0.1:5000 wsgi:app

# use on entire network
gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app

# this will start in port: 8000
gunicorn -w 1 wsgi:app
```


Or use the no-sendfile to fix this behaviour.

```sh
gunicorn -k eventlet --no-sendfile -w 1 -b 0.0.0.0:5000 wsgi:app
```