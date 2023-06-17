#!/usr/bin/env python3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/messages/messages', methods=['GET'])
def messages_messages_get():
    print('/messages/messages GET')
    
    return jsonify({'error':'Not Implemented'}), 501

@app.route('/messages/messages/<id>', methods=['GET'])
def messages_messages_id_get(id):
    print('/messages/messages/<id> GET', id)

    return jsonify({'error':'Not Implemented'}), 501

@app.route('/messages/messages', methods=['POST'])
def messages_messages_post():
    content = request.json
    print('/messages/messages POST', content)
    
    return jsonify({'error':'Not Implemented'}), 501


if __name__ == '__main__':
    app.run(host='0.0.0.0')