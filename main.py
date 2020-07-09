import json
import os
import uuid

import bottle
from bottle import request, response, run, HTTPResponse
from bottle import post, get, put, delete
from dotenv import load_dotenv
from pony.orm import *

# configuration --------------
load_dotenv()

# DB_LOCATION=contacts.db
# ENVIRONMENT=development
environment = os.getenv("ENVIRONMENT")
db_location = os.getenv("DB_LOCATION")

# database --------------
if environment != 'production':
    set_sql_debug(True)

db = Database()


class Contact(db.Entity):
    id = PrimaryKey(str)
    firstName = Required(str)
    lastName = Required(str)
    phoneNumber = Required(str)


db.bind(provider='sqlite', filename=db_location, create_db=True)
db.generate_mapping(create_tables=True)


# api --------------
@bottle.post('/contacts')
@db_session
def create_contact():
    """Creates a contact"""
    try:
        try:
            contact_payload = request.json
        except:
            raise ValueError
        if contact_payload is None:
            raise ValueError

        id = str(uuid.uuid4())

        Contact(id=id, firstName=contact_payload['firstName'], lastName=contact_payload['lastName'],
                phoneNumber=contact_payload['phoneNumber'])

        response.status = 201
        # todo: verify
        # response.set_header("Location", f"{request.path}/{id}")
        response.set_header("Location", f"/{id}")
    except ValueError:
        # todo: use abort?
        response.status = 400


@bottle.get('/contacts')
@db_session
def get_all_contacts():
    """Gets all contacts"""
    contacts_payload = []

    contacts = select(c for c in Contact)
    for c in contacts:
        contacts_payload.append(c.to_dict())

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(contacts_payload)


@bottle.get('/contacts/<id>')
@db_session
def get_contact(id):
    """Gets a specific contact"""
    try:
        contact = Contact[id]
    except ObjectNotFound:
        raise HTTPResponse(status=404)

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(contact.to_dict())


@bottle.put('/contacts/<id>')
@db_session
def update_contact(id):
    """Updates a contact"""
    try:
        contact = Contact[id]
    except ObjectNotFound:
        raise HTTPResponse(status=404)

    try:
        try:
            contact_payload = request.json
        except:
            raise ValueError
        if contact is None:
            raise ValueError

        contact.firstName = contact_payload['firstName']
        contact.lastName = contact_payload['lastName']
        contact.phoneNumber = contact_payload['phoneNumber']

        response.status = 204
    except ValueError:
        response.status = 400


@bottle.delete('/contacts/<id>')
@db_session
def delete_contact(id):
    """Deletes a contact"""
    try:
        contact = Contact[id]
    except ObjectNotFound:
        raise HTTPResponse(status=404)

    contact.delete()

    response.status = 204


if __name__ == '__main__':
    debug = environment == 'development'
    run(host='0.0.0.0', port=8010, debug=debug, reloader=debug)
