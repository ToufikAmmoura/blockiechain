# registering our second node
curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://127.0.0.1:5001"]
}' "http://localhost:5000/nodes/register"

# mining three blocks on our second node

curl -X GET http://localhost:5001/mine
curl -X GET http://localhost:5001/mine
curl -X GET http://localhost:5001/mine

# resolving the conflict between the nodes

curl -X GET http://localhost:5000/nodes/resolve

curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://127.0.0.1:5000"]
}' "http://localhost:5001/nodes/register"