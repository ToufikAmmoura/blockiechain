from Crypto.Hash import SHA256
from time import time

class Block:
    def __init__(self, index, hash, previous_hash, timestamp, proof, data):
        self.index = index
        self.hash = hash
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.proof = proof
        self.data = data
    
    def __repr__(self) -> str:
        return str(self.__dict__)

class Blockchain:
    def __repr__(self):
        return str(self.__dict__)

    def __init__(self, genesis_block):
        self.chain = []
        self.chain.append(genesis_block)

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
        hash = SHA256.new(encoded).hexdigest()
        return hash

    @staticmethod
    def valid_hash(hash):
        return hash[:4] == "0000"
    
    @property
    def last_block(self):
        return self.chain[-1]