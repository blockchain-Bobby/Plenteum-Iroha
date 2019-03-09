import binascii
from iroha import IrohaCrypto as ic
from iroha import Iroha, IrohaGrpc
import sys

iroha = Iroha('admin@test')
net = IrohaGrpc()
admin_private_key = open('./configs/admin@test.priv').read()

def send_transaction_and_print_status(transaction):
    global net
    hex_hash = binascii.hexlify(ic.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)

def create_users(user_name,domain):
    global iroha
    pk = ic.private_key()
    user_private_key = pk
    user_public_key = ic.derive_public_key(user_private_key)
    init_cmds = [
        iroha.command('CreateAccount', account_name=user_name, domain_id=domain,
                      public_key=user_public_key)
    ]
    init_tx = iroha.transaction(init_cmds)
    ic.sign_transaction(init_tx, admin_private_key)
    send_transaction_and_print_status(init_tx)
    return user_private_key, user_public_key
    
def create_new_asset(username,asset,domain,precision,qty):
    global iroha
    user_tx = iroha.transaction(
        [iroha.command('CreateAsset', asset_name=asset,
            domain_id=domain, precision=precision, amount='1')],
        creator_account=username
    )
    ic.sign_transaction(user_tx, admin_private_key)
    send_transaction_and_print_status(user_tx)