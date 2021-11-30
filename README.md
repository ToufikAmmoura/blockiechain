## blockiechain

voor nu is het min of meer gekopieerd van een tutorial maar zal er langzaam m'n eigen implementaties aan toevoegen


### mine a block
`curl -X GET http://localhost:5000/mine`

### perform transaction
```
curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "someone-other-address",
 "amount": 5
}' "http://localhost:5000/transactions/new"
```

### request blockchain

`curl -X GET http://localhost:5000/chain`
