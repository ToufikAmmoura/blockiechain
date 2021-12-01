# blockiechain

basicly a copied tutorial where I'm adding my own additions and implementations

## things to try

 - adding private keys so transactions can only be done by the owner
 - reward the miner for its mining

## possible commands

### mine a block
```
curl -X GET http://localhost:5000/mine
```

### perform transaction
```
curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "someone-other-address",
 "amount": 5
}' "http://localhost:5000/transactions/new"
```

### request blockchain

```
curl -X GET http://localhost:5000/chain
```

### register node

```
curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://127.0.0.1:5001"]
}' "http://localhost:5000/nodes/register"
```

### resolve conflict

```
curl -X GET http://localhost:5000/nodes/resolve
```