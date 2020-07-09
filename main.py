import json
import os
import uuid

from bottle import request, response, run, HTTPResponse
from bottle import post, get, put, delete
from dotenv import load_dotenv

# configuration --------------
load_dotenv()

# ENVIRONMENT=development
environment = os.getenv("ENVIRONMENT")

_contacts = [
    {'Id': str(uuid.uuid4()), 'FirstName': "Albert", 'LastName': "Einstein", 'PhoneNumber': "2222-1111"},
    {'Id': str(uuid.uuid4()), 'FirstName': "Mary", 'LastName': "Curie", 'PhoneNumber': "1111-1111"}
]


@post('/contacts')
def create_contact():
    """Creates a contact"""
    try:
        try:
            contact = request.json
        except:
            raise ValueError
        if contact is None:
            raise ValueError

        id = str(uuid.uuid4())
        contact['Id'] = id

        _contacts.append(contact)

        response.status = 201
        # todo: verify
        # response.set_header("Location", f"{request.path}/{id}")
        response.set_header("Location", f"/{id}")
    except ValueError:
        # todo: use abort?
        response.status = 400


@get('/contacts')
def get_all_contacts():
    """Gets all contacts"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(_contacts)


@get('/contacts/<id>')
def get_contact(id):
    """Gets a specific contact"""
    _, contact = find_contact(id)
    if not contact:
        raise HTTPResponse(status=404)

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(contact)


@put('/contacts/<id>')
def update_contact(id):
    """Updates a contact"""
    i, _ = find_contact(id)
    if i == -1:
        raise HTTPResponse(status=404)

    try:
        try:
            contact = request.json
        except:
            raise ValueError
        if contact is None:
            raise ValueError

        _contacts[i] = contact
        response.status = 204
    except ValueError:
        response.status = 400


@delete('/contacts/<id>')
def delete_contact(id):
    """Deletes a contact"""
    i, contact = find_contact(id)
    if not contact:
        raise HTTPResponse(status=404)

    del _contacts[i]
    response.status = 204


def find_contact(id):
    for i in range(len(_contacts)):
        if _contacts[i]['Id'] == id:
            return i, _contacts[i]
    return -1, None


if __name__ == '__main__':
    debug = environment == 'development'
    run(host='0.0.0.0', port=8010, debug=debug, reloader=debug)

