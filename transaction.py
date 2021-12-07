class Transaction(object):
    def __init__(self, id, txIns, txOuts):
        self.txIns = txIns
        self.txOuts = txOuts
        self.calcTxId()

    def calcTxId(self):
        # hash de txIns en de txOuts -> dat is de txId
        self.txId = ""
        pass    

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