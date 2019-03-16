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
    return user_private_key, user_public_key

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

def add_asset_to_admin(asset_id, qty):
    global iroha
    """
    Add asset supply and assign to 'admin@test'
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id=asset_id, amount=qty)
    ])
    ic.sign_transaction(tx, admin_private_key)
    send_transaction_and_print_status(tx)

def create_new_asset(asset,domain,precision,qty):
    global iroha
    user_tx = iroha.transaction(
        [iroha.command('CreateAsset', asset_name=asset,
            domain_id=domain, precision=precision)]    )
    ic.sign_transaction(user_tx, admin_private_key)
    send_transaction_and_print_status(user_tx)
    asset_id = asset + '#' + domain
    add_asset_to_admin(asset_id=asset_id,qty=qty)

def add_asset_to_user():
    """
    Add 1000.00 units of 'coin#domain' to 'admin@test'
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id='coin#domain', amount='1000.00')
    ])
    ic.sign_transaction(tx, admin_private_key)
    send_transaction_and_print_status(tx)

def create_ple_doman_and_asset():
    """
    Creates domain 'domain' and asset 'coin#domain' with precision 2
    """
    commands = [
        iroha.command('CreateDomain', domain_id='domain', default_role='user'),
        iroha.command('CreateAsset', asset_name='coin',
                      domain_id='domain', precision=2)
    ]
    tx = ic.sign_transaction(
        iroha.transaction(commands), admin_private_key)
    send_transaction_and_print_status(tx)

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

def set_account_detail(account_id,key,value):
    """
    Set age to user@domain by admin@test
    """
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id, key=key, value=value)
    ])
    ic.sign_transaction(tx, admin_private_key)
    send_transaction_and_print_status(tx)

def get_asset_info(asset_id):
    """
    Get asset info for coin#domain
    :return:
    """
    query = iroha.query('GetAssetInfo', asset_id=asset_id)
    ic.sign_query(query, admin_private_key)
    response = net.send_query(query)
    data = response.asset_response.asset
    print('Asset id = {}, precision = {}'.format(data.asset_id, data.precision))

def get_account_assets():
    """
    List all the assets of user@domain
    """
    query = iroha.query('GetAccountAssets', account_id='admin@test')
    ic.sign_query(query, admin_private_key)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    for asset in data:
        print('Asset id = {}, balance = {}'.format(
            asset.asset_id, asset.balance))
    return data

def get_user_details(account_id):
    """
    Get all the kv-storage entries for user@domain
    """
    query = iroha.query('GetAccountDetail', account_id=account_id)
    ic.sign_query(query, admin_private_key)

    response = net.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data