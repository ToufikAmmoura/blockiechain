import hashlib
import json
from time import time

class Block(object):
    def __init__(self, index, previous_hash, timestamp, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.proof = proof

        self.hash = self.calc_hash()

    def calc_hash(self):
        string = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.proof)
        encoded = string.encode()
        hash = hashlib.sha256(encoded).hexdigest()
        return hash

        # self.transactions = [] # TODO voor nu laat ik dit weg maar als ik aan transactions ga werken voeg ik het toe

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()

        # create the genesis block
        self.new_block(previous_hash=1, proof=100)

    # # TODO verwijder
    # def register_node(self, address):
    #     """
    #     Add a new node to the list of nodes
    #     address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
    #     """

    #     parsed_url = urlparse(address)
    #     self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        chain: <list> A blockchain
        return: <bool> True if valid, False if not
        """

        last_block = chain[0]   # beginning with the genesis block
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    # TODO als het goed is moet dit ook weg want dit moet via HTTP of P2P geregeld worden
    # def resolve_conflicts(self):
    #     """
    #     This is our Consensus Algorithm, it resolves conflicts
    #     by replacing our chain with the longest one in the network.
    #     return: <bool> True if our chain was replaced, False if not
    #     """

    #     neighbours = self.nodes
    #     new_chain = None

    #     # We're only looking for chains longer than ours
    #     max_length = len(self.chain)

    #     # Grab and verify the chains from all the nodes in our network
    #     for node in neighbours:
    #         response = requests.get(f'http://{node}/chain')

    #         if response.status_code == 200:
    #             length = response.json()['length']
    #             chain = response.json()['chain']

    #             # Check if the length is longer and the chain is valid
    #             if length > max_length and self.valid_chain(chain):
    #                 max_length = length
    #                 new_chain = chain

    #     # Replace our chain if we discovered a new, valid chain longer than ours
    #     if new_chain:
    #         self.chain = new_chain
    #         return True

    #     return False

    # TODO dit hier is een chille manier om docstrings te doen
    def new_block(self, proof, previous_hash):
        """ Create a new Block in the Blockchain
        
        args:
            proof (int): the proof given by the Proof of Work algorithm
            previous_hash (str): hash of previous Block
        returns: 
        dict: New Block
        """

        index = len(self.chain)+1
        timestamp = time()
        prev_hash = previous_hash or self.hash(self.chain[-1])
        block = Block(
            index=index,
            timestamp=timestamp,
            previous_hash=prev_hash,
            proof=proof
        )

        # Reset the current list of transactions
        # self.current_transactions = []
               
        self.chain.append(block)
        return block

    # TODO dit moet waarschijnlijk anders gaan uiteindelijk
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction tot go into the next mined Block
        sender: <str> Address of the Sender
        recipient: <str> Address of the Recipient
        amount: <int> Amount
        return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    # TODO moet nog nadenken of deze functie dus nodig is
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        block: <dict> Block
        return: <str>
        """

        # We must make sure that the Dict is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def proof_of_work(self, last_block):
        """
        Simple proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains 4 leading zeroes 
         - p is the previous proof, and p' is the new proof
        last_proof: <dict> last Block
        return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1
        
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof: does hash(last_proof, proof, last_hash) contain 4 leading zeroes?
        return: <bool>
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def main():
    print(3)

main()