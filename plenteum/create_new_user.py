import binascii
from iroha import IrohaCrypto as ic
from iroha import Iroha, IrohaGrpc
import sys

iroha = Iroha('admin@test')
net = IrohaGrpc()

admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'

alice_private_keys = [
    'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba1',
    'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506caba2'
]
alice_public_keys = [ic.derive_public_key(x) for x in alice_private_keys]

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
    init_cmds = [
        iroha.command('CreateAccount', account_name='alice', domain_id='casino',
                      public_key=alice_public_keys[0])
    ]
    init_tx = iroha.transaction(init_cmds)
    ic.sign_transaction(init_tx, admin_private_key)
    send_transaction_and_print_status(init_tx)