import os
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

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
        print('wallet already exists')
        return
    else:
        f = open(filename, 'wb')
        privkey, _ = make_keypair()
        f.write(privkey.export_key(format='DER'))
        f.close()

def get_key_from_wallet(name):
    filename = name + '.der'
    try:
        f = open(filename, 'rb')
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
            left_over = current_amount - amount
            return (included_utxos, left_over)

    print("Cannot create transaction from the available unpent transaction outputs")
    return None, None # hier misschien beter over nadenken

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

def create_txouts(receiver, my_address, amount, left_over_amount):
    import transaction
    txout = transaction.TxOut(receiver, amount)
    if left_over_amount == 0:
        return [txout]
    else:
        left_over_txout = transaction.TxOut(my_address, left_over_amount)
        return [txout, left_over_txout]

def filter_tx_pool_txs(unspent_txouts, transaction_pool):
    unused_utxos = []
    used = []
    for transaction in transaction_pool:
        for txin in transaction.txins:
            tup = (txin.txout_id, txin.txout_index)
            used.append(tup)
    
    for utxo in unspent_txouts:
        tup = (utxo.txout_id, utxo.txout_index)
        if tup not in used:
            unused_utxos.append(utxo)
    
    return unused_utxos

def create_transaction(receiver, amount, priv_key, unspent_txouts, tx_pool):
    import transaction
    address = get_hex_from_key(priv_key.public_key())
    my_unspent_txouts = find_unspent_txouts(address, unspent_txouts)
    my_unspent_txouts = filter_tx_pool_txs(my_unspent_txouts, tx_pool)

    included_utxouts, left_over = find_txouts_for_amount(amount, my_unspent_txouts)
    unsigned_txins = []
    for utxo in included_utxouts:
        txin = transaction.TxIn(utxo.txout_id, utxo.txout_index, "")
        unsigned_txins.append(txin)
    
    txouts = create_txouts(receiver, address, amount, left_over)
    transaction = transaction.Transaction(unsigned_txins, txouts)

    for txin in transaction.txins:
        txin.sign(transaction.id, priv_key, unspent_txouts)
    
    return transaction