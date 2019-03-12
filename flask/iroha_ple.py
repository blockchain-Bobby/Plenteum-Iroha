import binascii
from iroha import IrohaCrypto as ic
from iroha import Iroha, IrohaGrpc
import sys

iroha = Iroha('admin@test')
#populate from login form. iroha = Iroha('user@domain')
net = IrohaGrpc()
admin_private_key = open('./configs/admin@test.priv').read()
#user_private_key = open('./configs/user@test.priv').read() or from form.

def send_transaction_and_print_status(transaction):
    global net
    hex_hash = binascii.hexlify(ic.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)

def create_domain():
    return

def add_peer_node():
    return

def generate_kp():
    global iroha
    pk = ic.private_key()
    user_private_key = pk
    user_public_key = ic.derive_public_key(user_private_key)
    return user_private_key, user_private_key

def create_users(user_name,domain):
    global iroha
    user_private_key, user_public_key = generate_kp()
    init_cmds = [
        iroha.command('CreateAccount', account_name=user_name, domain_id=domain,
                      public_key=user_public_key)
    ]
    init_tx = iroha.transaction(init_cmds)
    ic.sign_transaction(init_tx, admin_private_key)
    send_transaction_and_print_status(init_tx)
    return user_private_key, user_public_key
    
def create_new_asset(username,asset,domain,precision):
    global iroha
    user_tx = iroha.transaction(
        [iroha.command('CreateAsset', asset_name=asset,
            domain_id=domain, precision=precision)],
        creator_account=username
    )
    ic.sign_transaction(user_tx, admin_private_key)
    send_transaction_and_print_status(user_tx)

def transfer_asset(owner,recepient,asset_id,description,domain,qty):
    global iroha
    user_tx = iroha.transaction(
        iroha.command('TransferAsset', src_account_id=owner, dest_account_id=recepient,
                      asset_id=asset_id, description=description, amount=qty))
    ic.sign_transaction(user_tx, admin_private_key)
    send_transaction_and_print_status(user_tx)

def get_blocks():
    """
    Subscribe to blocks stream from the network
    :return:
    """
    query = iroha.blocks_query()
    ic.sign_query(query, admin_private_key)
    for block in net.send_blocks_stream_query(query):
        print('The next block arrived:', block)

def add_account_detaill():
    return