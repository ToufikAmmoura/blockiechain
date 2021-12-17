from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

def make_keypair():
    privkey = ECC.generate(curve='P-256')
    pubkey = privkey.public_key()
    return privkey, pubkey 

def make_hex_key(key):
    binary = key.public_key().export_key(format='DER')
    return binary.hex()

def sign_something(priv_key, something):
    signer = DSS.new(priv_key, 'fips-186-3')
    h = SHA256.new(something)
    signature = signer.sign(h)
    return signature

def verify_signature(pub_key, something, signature):
    h = SHA256.new(something)
    verifier = DSS.new(pub_key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        print ("The message is authentic.")
    except ValueError:
        print ("The message is not authentic.")
