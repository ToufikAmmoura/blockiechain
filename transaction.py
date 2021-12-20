import hashlib
from wallet import *
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

COINBASE_AMOUNT = 50

class Transaction(object):

    def __init__(self, txins, txouts):
        self.txins = txins
        self.txouts = txouts
        self.id = self.calc_txid()

    def calc_txid(self):
        txins_content = "".join([x.txout_id + str(x.txout_index) for x in self.txins])
        txouts_content = "".join([x.address + str(x.amount) for x in self.txouts])
        content = txins_content + txouts_content
        encoded = content.encode()
        hash = hashlib.sha256(encoded).hexdigest() # misschien hier SHA256 gebruiken ipv hashlib
        return hash

    def validate_transaction(self, pubkey, allUnspentTxOuts):
        # ID must be right
        if not self.id == self.calc_txid():
            return False
        
        # verify the txin signatures
        for txin in self.txins:
            if not verify_signature(pubkey, self.id, txin.signature):
                return False

        # validating if input is equal to output
        input = 0
        output = 0
        
        # calculating input
        for txin in self.txins:
            id, index = txin.txout_id, txin.txout_index
            for utxout in allUnspentTxOuts:
                if id == utxout.txout_id and index == utxout.txout_index:
                    input += utxout.amount
        
        # calculating output
        for txout in self.txouts:
            output += txout.amount

        return input == output

    def validate_coinbase_transaction(self, block_index):
        # ID must be right
        if not self.id == self.calc_txid():
            return False

        # must contain only one txin and one txout
        if len(self.txins) != 1 or len(self.txouts) != 1:
            return False
        
        # txout_index must be the blockindex
        if self.txins[0].txout_index != block_index:
            return False

        # coinbase amount must be valid
        return self.txouts[0].amount == COINBASE_AMOUNT

    def __repr__(self):
        return str(self.__dict__)
        

class UnspentTxOut(object):
    def __init__(self, txout_id, txout_index, address, amount):
        self.txout_id = txout_id
        self.txout_index = txout_index
        self.address = address
        self.amount = amount
    
    def __repr__(self):
        return str(self.__dict__)

class TxIn(object):
    def __init__(self, txout_id, txout_index, signature):
        self.txout_id = txout_id
        self.txout_index = txout_index
        self.signature = signature
    
    def validate_txin(transaction, unspent_txouts):
        pass

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
        for index, txout in enumerate(transaction.txouts):
            utxout = UnspentTxOut(
                transaction.id,
                index,
                txout.address,
                txout.amount
            )
            new.append(utxout)

    used = []
    for transaction in block_transactions:
        for txin in transaction.txins:
            id = txin.txout_id
            index = txin.txout_index
            used.append((id, index))

    for utxout in unspent_txouts:
        id = utxout.txout_id
        index = utxout.txout_index
        tup = (id, index)
        if tup in used:
            unspent_txouts.remove(tup)
            used.remove(tup)

    return unspent_txouts + new

def validate_block_transactions(transactions, unspent_txouts, block_index):
    # coinbase transaction must be valid
    coinbase_tx = transactions[0]
    if not coinbase_tx.validate_coinbase_transaction(block_index):
        return False

    # there are no duplicate txins
    txins = []
    for transaction in transactions:
        for txin in transaction.txins:
            tup = (txin.txout_id, txin.txout_index)
            txins.append(tup)
    
    duplicates = len(txins) != len(set(txins))
    if duplicates:
        return False

    # validate the normal transactions
    for transaction in transactions[:1]:
        if not transaction.validate_transaction(unspent_txouts):
            return False
    
    return True


def get_coinbase_transaction(address, block_index):
    coinbase_in = TxIn(txout_id='', txout_index=block_index, signature='')
    coinbase_out = TxOut(address=address, amount=COINBASE_AMOUNT)
    coinbase_tx = Transaction([coinbase_in], [coinbase_out])
    return coinbase_tx