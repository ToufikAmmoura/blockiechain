import hashlib
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

class Transaction(object):

    def __init__(self, txIns, txOuts):
        self.txIns = txIns
        self.txOuts = txOuts
        self.id = self.calc_txid()

    def calc_txid(self):
        txins_content = "".join([x.txOutId + str(x.txOutIndex) for x in self.txIns])
        txouts_content = "".join([x.address + str(x.amount) for x in self.txOuts])
        content = txins_content + txouts_content
        encoded = content.encode()
        hash = hashlib.sha256(encoded).hexdigest() # misschien hier SHA256 gebruiken ipv hashlib
        return hash

    def validate_transaction(self, allUnspentTxOuts):
        # check de signatures van alle txIns
        # check of het geld ook daadwerkelijk aanwezig is
        pass

    def __repr__(self):
        return str(self.__dict__)
        

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
    
    def __repr__(self):
        return str(self.__dict__)

class TxOut(object):
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def __repr__(self):
        return str(self.__dict__)
        