import binascii
from iroha import IrohaCrypto as ic
from iroha import Iroha, IrohaGrpc
import sys

def connect_to_iroha():
        iroha = Iroha('admin@test')
        net = IrohaGrpc()

        admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'


def send_transaction_and_print_status(transaction):
    global net
    hex_hash = binascii.hexlify(ic.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)

def create_users():
    global iroha
    user_private_key =  'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba1'
    user_public_key = ic.derive_public_key(user_private_key)

    init_cmds = [
        iroha.command('CreateAccount', account_name='alice', domain_id='casino',
                      public_key=user_public_key)
    ]
    init_tx = iroha.transaction(init_cmds)
    ic.sign_transaction(init_tx, admin_private_key)
    send_transaction_and_print_status(init_tx)