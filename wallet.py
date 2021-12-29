from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import os

def make_keypair():
    privkey = ECC.generate(curve='P-256')
    pubkey = privkey.public_key()
    return privkey, pubkey 

def get_key_from_hex(hex):
    return ECC.import_key(bytes.fromhex(hex))

def get_hex_from_key(key):
    binary = key.public_key().export_key(format='DER')
    return binary.hex()

def init_wallet(name):
    filename = name + '.der'
    if os.path.exists(filename):
        return
    else:
        f = open(filename, 'wt')
        privkey, _ = make_keypair()
        f.write(privkey.export_key(format='DER'))
        f.close()

def get_key_from_wallet(name):
    filename = name + '.der'
    try:
        f = open(filename, 'rt')
        key = ECC.import_key(f.read())
        return key
    except FileNotFoundError:
        print('Wallet does not exist')
        return None

def get_balance(address, unspent_txouts):
    amount = 0
    for utxo in unspent_txouts:
        if utxo.address == address:
            amount += utxo.amount
    return amount

def find_unspent_txouts(address, unspent_txouts):
    utxos = []
    for utxo in unspent_txouts:
        if utxo.address == address:
            utxos.append(utxo)
    return utxos

def find_txouts_for_amount(amount, unspent_txouts):
    current_amount = 0
    included_utxos = []
    for utxo in unspent_txouts:
        current_amount += utxo.amount
        included_utxos.append(utxo)
        if current_amount >= amount:
            leftover = current_amount - amount
            return (included_utxos, leftover)

    print("Cannot create transaction from the available unpent transaction outputs")
    return None # hier misschien beter over nadenken

def delete_wallet(name):
    filename = name + '.der'
    if os.path.exists(filename):
        os.remove(filename)

def sign_data(priv_key, data):
    signer = DSS.new(priv_key, 'fips-186-3')
    h = SHA256.new(data)
    signature = signer.sign(h)
    return signature

def verify_signature(pub_key, data, signature):
    h = SHA256.new(data)
    verifier = DSS.new(pub_key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        return True
    except ValueError:
        print("wrong signature")
        return False