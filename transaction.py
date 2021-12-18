import hashlib
from wallet import *
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

    def validate_transaction(self, pubkey, allUnspentTxOuts):
        # check of id nog goed is
        if not self.id == self.calc_txid():
            return False
        
        # check de signatures van alle txIns
        for txin in self.txIns:
            if not verify_signature(pubkey, self.id, txin.signature):
                return False

        # check of de input gelijk is aan de output
        for txin in self.txIns:
            tup = (txin.txOutId, txin.txOutIndex)
            for utxout in allUnspentTxOuts:
                pass
        
        return True

    def __repr__(self):
        return str(self.__dict__)
        

class UnspentTxOut(object):
    def __init__(self, txOutId, txOutIndex, address, amount):
        self.txOutId = txOutId
        self.txOutIndex = txOutIndex
        self.address = address
        self.amount = amount
    
    def __repr__(self):
        return str(self.__dict__)

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
        
def update_unspent_txouts(block_transactions, unspent_txouts):
    new = []
    for transaction in block_transactions:
        for index, txout in enumerate(transaction.txOuts):
            utxout = UnspentTxOut(
                transaction.id,
                index,
                txout.address,
                txout.amount
            )
            new.append(utxout)

    used = []
    for transaction in block_transactions:
        for txin in transaction.txIns:
            id = txin.txOutId
            index = txin.txOutIndex
            used.append((id, index))

    for utxout in unspent_txouts:
        id = utxout.txOutId
        index = utxout.txOutIndex
        tup = (id, index)
        if tup in used:
            unspent_txouts.remove(tup)
            used.remove(tup)

    return unspent_txouts + new