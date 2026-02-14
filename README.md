# contacts-backend-python-bottle

**contacts-backend-python-bottle** is part of "contacts" project that is an initiative where we try to explore frontend and backend implementations in order to better understand it cutting-edge features. This repository presents a python rest API sample.

## status

This repository belongs to the Contacts reference initiative started in 2020.

Its purpose was to understand how different stacks shape design decisions around the same domain model.

As of 2026, this project is frozen.

The exploration phase has been completed.  
My current focus is depth, invariants, and system coherence rather than stack comparison.

This code remains as historical reference.

## stack
* python 3.10
* bottle
* sqlite
* pony

## features
* migrations
* small footprint

## get started (linux instructions only)

### option 1 - use latest docker image from dockerhub

execute the remote docker image
```
docker run -p 8010:8010 wastingnotime/contacts-backend-python-bottle
```

### option 2 - just build and use as docker image
build a local docker image
```
docker build --tag contacts-backend-python-bottle .
```

execute the local docker image
```
docker run -p 8010:8010 contacts-backend-python-bottle
```
### option 3 - execute from source code 
- first, install python 3.10+, if you don't have it on your computer:  [how to install python 3](https://docs.python.org/3/using/unix.html#on-linux)
- go to root of solution and execute the commands below

set environment for development
```
cp .env_example .env
```

activate venv
```
source venv/bin/activate
```

install deps
```
pip install -r requirements.txt
```

and then run the application
```
python3 main.py
```

## testing
create a new contact
```
curl --request POST \
  --url http://localhost:8010/contacts \
  --header 'Content-Type: application/json' \
  --data '{
	"firstName": "Albert",
	"lastName": "Einstein",
	"phoneNumber": "2222-1111"
  }'
```

retrieve existing contacts
```
curl --request GET \
  --url http://localhost:8010/contacts
```
more examples and details about requests on (link) *to be defined
