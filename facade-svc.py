#!/usr/bin/env python3
from zoneinfo import available_timezones
from flask import Flask, request, jsonify, make_response
import uuid, requests
from ast import literal_eval
import random

LOGGING_URL = 'http://localhost'
MESSAGES_URL = 'http://localhost:10010'

app = Flask(__name__)

@app.route('/api/messages', methods=['GET'])
def api_messages_get():
    print('/api/messages GET')

    logging = requests.get(get_logging_url() + '/logging/messages')
    messages = requests.get(MESSAGES_URL + '/messages/messages')

    return create_response(logging, messages)

@app.route('/api/messages/<id>', methods=['GET'])
def api_messages_id_get(id):
    print('/api/messages/<id> GET', id)

    logging = requests.get(get_logging_url() + '/logging/messages/'+id)
    messages = requests.get(MESSAGES_URL + '/messages/messages/'+id)

    return create_response(logging, messages)

@app.route('/api/messages', methods=['POST'])
def api_messages_post():
    content = request.json
    print('/api/messages POST', content)    
    
    content['uuid'] = str(uuid.uuid4())
    logging = requests.post(get_logging_url() + '/logging/messages', json=content)
    messages = requests.post(MESSAGES_URL + '/messages/messages', json=content)
    
    #return jsonify(uuid=content['uuid'])
    return create_response(logging, messages)

def create_response(logging, messages):
    resp = {
        'logging':{
            'code':logging.status_code,
            'content':literal_eval(logging.text)
        },
        'messages':{
            'code':messages.status_code,
            'content':literal_eval(messages.text)
        },
    }
    return jsonify(resp)

def get_logging_url():
    available_ports = ['9090', '9091', '9092']
    url = ''
    while True:
        try:
            url = LOGGING_URL + ':' + random.choice(available_ports)
            r = requests.options(url)
            print(url, '- selected')
            break
        except Exception as ex:
            print(url, '- failed to establish a new connection')

    return url


if __name__ == '__main__':
    app.run(host='0.0.0.0')