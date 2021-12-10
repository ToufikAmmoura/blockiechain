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

    def validateTransaction(self, allUnspentTxOuts):
        # check de signatures van alle txIns
        # check of het geld ook daadwerkelijk aanwezig is
        pass

class UnspentTxOut(object):
    def __init__(self, txOutId, txOutIndex, address, amount):
        self.txOutId = txOutId
        self.txOutIndex = txOutIndex
        self.address = address
        self.amount = amount

class TxIn(object):
    def __init__(self, txOutId, txOutIndex, signature):
        self.txOutId = txOutId
        self.txOutIndex = txOutIndex
        self.signature = signature

class TxOut(object):
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount