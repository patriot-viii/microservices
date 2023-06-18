# [FB-z21mp] Volodymyr Duduladenko
Results of practical work in the discipline "Distributed Systems Design"
## Task 1
### Run services
```
flask --app facade-svc.py run --port=8080
flask --app logging-svc.py run --port=9090
flask --app messages-cvc.py run --port=10010
```
### Send requests
```
curl -H 'Content-Type: application/json' -d '{"msg":"hello world"}' http://0.0.0.0:8080/api/messages
curl -H 'Content-Type: application/json' -d '{"msg":"goodbye monolith"}' http://0.0.0.0:8080/api/messages
curl http://0.0.0.0:8080/api/messages
curl http://0.0.0.0:8080/api/messages/
```
## Task 2
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