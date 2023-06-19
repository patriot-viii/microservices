#!/usr/bin/env python3
import consul
import random

master = consul.Consul()

def consul_register_kv():
    master.kv.put('MAP_LOGGING', 'messages-map')
    master.kv.put('MAP_MESSAGES', 'queue-map')
    master.kv.put('QUEUE_MESSAGES', 'messages-queue')    

def consul_get_value(key):
    index, data = master.kv.get(key)
    return data['Value'].decode()

def consul_service_register(name, address, port):
    service_id = get_service_id(name, port)
    return master.agent.service.register(name, service_id=service_id, address=address, port=port)

def consul_service_deregister(name, port):
    service_id = get_service_id(name, port)
    return master.agent.service.deregister(service_id)

def get_service_id(name, port):
    return f'{name}-{port}'

def consul_get_service(svc_name):
    services = []
    for id, svc in master.agent.services().items():
        if svc['Service'] == svc_name:
            services.append(svc)
    selected_svc = random.choice(services)
    return f"http://{selected_svc['Address']}:{selected_svc['Port']}"