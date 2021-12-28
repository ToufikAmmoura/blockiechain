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