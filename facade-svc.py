#!/usr/bin/env python3
from flask import Flask, request, jsonify
import uuid, requests, json, atexit
from ast import literal_eval
import hazelcast
from consul_facade import consul_get_value, consul_service_register, consul_service_deregister, consul_get_service
from service_utils import get_host_port

LOGGING_SVC = 'logging-svc'
MESSAGES_SVC = 'messages-svc'

HAZLECAST_CLIENT = hazelcast.HazelcastClient()
HAZLECAST_QUEUE = HAZLECAST_CLIENT.get_queue(consul_get_value("QUEUE_MESSAGES")) 

app = Flask(__name__)

@app.route('/api/messages', methods=['GET'])
def api_messages_get():
    print('/api/messages GET')

    logging = requests.get(get_logging_url() + '/logging/messages')
    messages = requests.get(get_messages_url() + '/messages/messages')

    return create_response(logging, messages)

@app.route('/api/messages/<id>', methods=['GET'])
def api_messages_id_get(id):
    print('/api/messages/<id> GET', id)

    logging = requests.get(get_logging_url() + '/logging/messages/'+id)
    messages = requests.get(get_messages_url() + '/messages/messages/'+id)

    return create_response(logging, messages)

@app.route('/api/messages', methods=['POST'])
def api_messages_post():
    content = request.json
    print('/api/messages POST', content)    
    
    content['uuid'] = str(uuid.uuid4())
    logging = requests.post(get_logging_url() + '/logging/messages', json=content)

    messages = requests.Response()
    if HAZLECAST_QUEUE.offer(content).result():
        print("Produced {}".format(content))
        messages.status_code = 200
        messages._content = json.dumps({'uuid':content['uuid']}).encode()
    else:
        print("Failed to produce {}".format(content))
        messages.status_code = 500
        messages._content = json.dumps({'error':'Not produced'}).encode()
    
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
    url = consul_get_service(LOGGING_SVC)
    print('Selected', url)
    return url

def get_messages_url():
    url = consul_get_service(MESSAGES_SVC)
    print('Selected', url)
    return url

def on_exit():
    print('on exit')
    consul_service_deregister(app.name, port)
    HAZLECAST_CLIENT.shutdown()

if __name__ == '__main__':
    atexit.register(on_exit)

    host, port = get_host_port()
    consul_service_register(app.name, host, port)

    app.run(host=host, port=port)