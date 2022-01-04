from transaction import *

class TransactionPool:
    def __init__(self, transaction_pool):
        self.transaction_pool = transaction_pool

    def add_to_transaction_pool(self, transaction, unspent_txouts):
        if not transaction.validate_transaction(unspent_txouts):
            print('trying to add invalid tx to pool')
            return
        
        if not self.is_valid_for_transaction_pool(transaction):
            print('trying to add invalid tx to pool')
            return

        self.transaction_pool.append(transaction)

    def is_valid_for_transaction_pool(self, transaction):
        used_txins = []
        for pool_transaction in self.transaction_pool:
            for txin in pool_transaction.txins:
                tup = (txin.txout_id, txin.txout_index)
                used_txins.append(tup)

        for txin in transaction.txins:
            tup = (txin.txout_id, txin.txout_index)
            if tup in used_txins:
                return False
        
        return True

    def update_transaction_pool(self, unspent_txouts):
        for transaction in self.transaction_pool:
            for txin in transaction.txins:
                if not has_txin(txin, unspent_txouts):
                    self.transaction_pool.remove(transaction)
                    break

    def get_txins(self):
        txins = []
        for transaction in self.transaction_pool:
            for txin in transaction.txins:
                txins.append(txin)
        return txins


def has_txin(txin, unspent_txouts):
    for utxo in unspent_txouts:
        if utxo.txout_id == txin.txout_id and utxo.txout_index == txin.txout_index:
            return True
    
    return False