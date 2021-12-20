import hashlib
from time import time
from transaction import Transaction, TxIn, TxOut

class Block(object):
    def __init__(self, index, hash, previous_hash, timestamp, proof, data):
        self.index = index
        self.hash = hash
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.proof = proof
        self.data = data
    
    def __repr__(self) -> str:
        return str(self.__dict__)

class Blockchain(object):
    def __repr__(self):
        return str(self.__dict__)

    def __init__(self):
        self.chain = []

        # create the genesis transaction
        genesis_in = TxIn(txout_id="", txout_index=0, signature="")
        address = "3059301306072a8648ce3d020106082a8648ce3d0301070342000447e45d57be90ac1ad97c5232f7922ade8e63f9931666f1fab5f1bcaac0bdc4b83bf68c72534eb33b68865b5e5465c7ba46094961b578513aed09ed22ab8c03f3"
        genesis_out = TxOut(address=address, amount=50)
        genesis_transaction = Transaction(txins=[genesis_in], txouts=[genesis_out])

        # create the genesis block
        genesis_hash = "0000607e58623c07e2634999e38638e13b76af5b450cd7a295bc60179e6db208"
        genesis = Block(index=0, hash=genesis_hash, previous_hash="", timestamp="inthebeninging", proof=33, data=[genesis_transaction])
        self.chain.append(genesis)

    def generate_new_block(self, data):
        last_block = self.last_block
        index = last_block.index + 1
        previous_hash = last_block.hash
        timestamp = time()

        block = self.proof_of_work(index, previous_hash, timestamp, data)
        return block

    def proof_of_work(self, index, previous_hash, timestamp, data):
        proof = 0
        while True:
            hash = self.calc_hash(index, previous_hash, timestamp, proof, data)  
            if self.valid_hash(hash):
                block = Block(
                    index=index,
                    hash=hash,
                    previous_hash=previous_hash,
                    timestamp=timestamp,
                    proof=proof,
                    data=data
                )
                return block
            proof += 1

    def valid_block(self, block,  previous_block):
        if previous_block.index + 1 != block.index:
            return False
        elif previous_block.hash != block.previous_hash:
            return False
        else:
            recalculate_hash = self.calc_hash(block.index, block.previous_hash, block.timestamp, block.proof, block.data) 
            if recalculate_hash != block.hash:
                return False

    def replace_chain(self, new_chain):
        if self.valid_chain(new_chain) and len(new_chain) > len(self.chain):
            self.chain = new_chain
        else:
            print("received blockchain invalid")
    
    @staticmethod
    def valid_chain(self, chain):
        for i in range(1, len(chain)):
            prev_block = chain[i-1]
            block = chain[i]
            if not self.valid_block(block, prev_block):
                return False
            
        return True

    @staticmethod
    def calc_hash(index, previous_hash, timestamp, proof, data):
        string = str(index) + previous_hash + str(timestamp) + str(proof) + str(data)
        encoded = string.encode()
        hash = hashlib.sha256(encoded).hexdigest()
        return hash

    @staticmethod
    def valid_hash(hash):
        return hash[:4] == "0000"
    
    @property
    def last_block(self):
        return self.chain[-1]