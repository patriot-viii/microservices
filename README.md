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