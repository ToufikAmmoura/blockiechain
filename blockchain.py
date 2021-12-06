import hashlib
import json
from time import time

class Block(object):
    def __init__(self, index, hash, previous_hash, timestamp, proof):
        self.index = index
        self.hash = hash
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.proof = proof

class Blockchain(object):
    def __init__(self):
        self.chain = []

        # create the genesis block
        genesis_hash = "0000607e58623c07e2634999e38638e13b76af5b450cd7a295bc60179e6db208"
        genesis = Block(0, genesis_hash, "", "inthebeninging", 33)
        self.chain.append(genesis)

    def generate_new_block(self):
        last_block = self.last_block
        index = last_block.index + 1
        previous_hash = last_block.hash
        timestamp = time()

        block = self.proof_of_work(index, previous_hash, timestamp)
        return block


    def proof_of_work(self, index, previous_hash, timestamp):
        proof = 0
        while True:
            hash = self.calc_hash(index, previous_hash, timestamp, proof)  
            if self.valid_hash(hash):
                block = Block(
                    index=index,
                    hash=hash,
                    previous_hash=previous_hash,
                    timestamp=timestamp,
                    proof=proof
                )
                return block
            proof += 1
    
    @staticmethod
    def calc_hash(index, previous_hash, timestamp, proof):
        string = str(index) + previous_hash + str(timestamp) + str(proof)
        encoded = string.encode()
        hash = hashlib.sha256(encoded).hexdigest()
        return hash

    @staticmethod
    def valid_hash(hash):
        return hash[:4] == "0000"
    
    @property
    def last_block(self):
        return self.chain[-1]