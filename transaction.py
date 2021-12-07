import hashlib

class Transaction(object):
    def __init__(self, txIns, txOuts):
        self.txIns = txIns
        self.txOuts = txOuts
        self.id = self.calcTxId()

    def calcTxId(self):
        txins_content = "".join([x.txOutId + str(x.txOutIndex) for x in self.txIns])
        txouts_content = "".join([x.address + str(x.amount) for x in self.txOuts])
        content = txins_content + txouts_content
        encoded = content.encode()
        hash = hashlib.sha256(encoded).hexdigest()
        return hash    

class TxIn(object):
    def __init__(self, txOutId, txOutIndex):
        self.txOutId = txOutId
        self.txOutIndex = txOutIndex
        # voor nu is de signature even niet nodig
        # self.signature = signature

class TxOut(object):
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount