# [FB-z21mp] Volodymyr Duduladenko
Results of practical work in the discipline "Distributed Systems Design"
## Task 1
### Run services
```
flask --app facade-svc.py run --port=8080
flask --app logging-svc.py run --port=9090
flask --app messages-svc.py run --port=10010
```
### Send requests
```
curl -H 'Content-Type: application/json' -d '{"msg":"hello world"}' http://0.0.0.0:8080/api/messages
curl -H 'Content-Type: application/json' -d '{"msg":"goodbye monolith"}' http://0.0.0.0:8080/api/messages
curl http://0.0.0.0:8080/api/messages
curl http://0.0.0.0:8080/api/messages/
```
## Task 2
### Useful links
[Hazelcast > Distributed Data Structures > Map](https://docs.hazelcast.com/hazelcast/latest/data-structures/map)

[Hazelcast > Distributed Data Structures > Queue](https://docs.hazelcast.com/hazelcast/latest/data-structures/queue)

[Hazelcast Python Client > map.py](https://github.com/hazelcast/hazelcast-python-client/blob/9c4cc92208d94dfc20708564a8b3613b7c3aee39/hazelcast/proxy/map.py)

[Hazelcast Python Client > queue.py](https://github.com/hazelcast/hazelcast-python-client/blob/9c4cc92208d94dfc20708564a8b3613b7c3aee39/hazelcast/proxy/queue.py)

### Install hazelcast
```
wget -qO - https://repository.hazelcast.com/api/gpg/key/public | gpg --dearmor | sudo tee /usr/share/keyrings/hazelcast-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/hazelcast-archive-keyring.gpg] https://repository.hazelcast.com/debian stable main" | sudo tee -a /etc/apt/sources.list
sudo apt update && sudo apt install hazelcast=5.3.1
sudo apt update && sudo apt install hazelcast-management-center=5.3.0
```
### Configure hazelcast
```
sudo vim /usr/lib/hazelcast/config/hazelcast.xml
```
### Run hazelcast
```
hz -v
hz start
hz start
hz start

hz-mc -V
hz-mc start
```
## Task 3
### Run hazelcast
```
hz start
hz start
hz start
hz-mc start
```
### Run services
```
python3 -m flask --app facade-svc.py run --port=1337
python3 -m flask --app messages-svc.py run --port=10010
python3 -m flask --app logging-svc.py run --port=9090
python3 -m flask --app logging-svc.py run --port=9091
python3 -m flask --app logging-svc.py run --port=9092
```
### Send POST requests
```
for i in `seq 1 10`; \
do curl -H 'Content-Type: application/json' -d '{"msg":"msg-'$i'"}' \
http://0.0.0.0:1337/api/messages; \
done
```
### Send GET request
```
curl http://0.0.0.0:1337/api/messages
```
## Task 4
### Run services
```
python3 -m flask --app facade-svc.py run --port=1337
python3 -m flask --app messages-svc.py run --port=10010
python3 -m flask --app messages-svc.py run --port=10011
python3 -m flask --app logging-svc.py run --port=9090
python3 -m flask --app logging-svc.py run --port=9091
python3 -m flask --app logging-svc.py run --port=9092
```
### Send POST requests
```
for i in `seq 1 10`; \
do curl -H 'Content-Type: application/json' -d '{"msg":"msg-'$i'"}' \
http://0.0.0.0:1337/api/messages; \
done
```
### Send GET request
```
curl http://0.0.0.0:1337/api/messages
```
## Task 5
### Useful links
[Start the Consul Agent in Dev Mode](https://mpolinowski.github.io/docs/DevOps/Hashicorp/2020-08-17--installing-consul-ubuntu/2020-08-17/#start-the-consul-agent-in-dev-mode)

[Python client for Consul.io](https://python-consul.readthedocs.io/en/latest/)

### Install Consul
```
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install consul
```
### Consul commands
```
consul --version
consul agent -dev
pip3 install python-consul
```
### Run services
```
python3 facade-svc.py --host=127.0.0.1 --port=1337
python3 messages-svc.py --host=127.0.0.1 --port=10010
python3 messages-svc.py --host=127.0.0.1 --port=10011
python3 logging-svc.py --host=127.0.0.1 --port=9090
python3 logging-svc.py --host=127.0.0.1 --port=9091
python3 logging-svc.py --host=127.0.0.1 --port=9092
```
### Send POST requests
```
for i in `seq 1 10`; \
do curl -H 'Content-Type: application/json' -d '{"msg":"msg-'$i'"}' \
http://0.0.0.0:1337/api/messages; \
done
```
### Send GET request
```
curl http://0.0.0.0:1337/api/messages
```