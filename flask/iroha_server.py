import binascii
from iroha import IrohaCrypto as ic
from iroha import Iroha, IrohaGrpc
from iroha.primitive_pb2 import can_set_my_account_detail
import sys
import json
import os

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

def create_users(user_name,domain,ple_id,pwd_hash):
    global iroha
    """
    register new user, grant permission to admin and set password & plenteum address
    """
    user_private_key, user_public_key = generate_kp()
    init_cmds = [
        iroha.command('CreateAccount', account_name=user_name, domain_id=domain,
                      public_key=user_public_key)
    ]
    init_tx = iroha.transaction(init_cmds)
    ic.sign_transaction(init_tx, admin_private_key)
    send_transaction_and_print_status(init_tx)
    account_id = user_name + '@' + domain
    grant_permission = iroha.transaction([
        iroha.command('GrantPermission', account_id='admin@test', permission=can_set_my_account_detail)
    ], creator_account=account_id)
    ic.sign_transaction(grant_permission, user_private_key)
    send_transaction_and_print_status(grant_permission)
    account_details = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id, key='password', value=pwd_hash),
        iroha.command('SetAccountDetail',
                      account_id=account_id, key='ple_id', value=ple_id)], creator_account='admin@test')
    ic.sign_transaction(account_details, admin_private_key)
    send_transaction_and_print_status(account_details)
    user_pvt_file = './configs/' + account_id +'.priv'
    user_pub_file = './configs/' + account_id +'.pub'
    user_private_key_file = open(user_pvt_file).write(admin_private_key)
    user_publcic_key_file = open(user_pvt_file).write(admin_private_key)
    return user_private_key, user_public_key
    

def create_domain_asset_manager(domain,ple_id):
    global iroha
    """
    register new domain asset manager and set password & plenteum address
    """
    user_private_key, user_public_key = generate_kp()
    init_cmds = [
        iroha.command('CreateAccount', account_name="asset_manager", domain_id=domain,
                      public_key=user_public_key)
    ]
    init_tx = iroha.transaction(init_cmds)
    ic.sign_transaction(init_tx, admin_private_key)
    send_transaction_and_print_status(init_tx)
    account_id = 'asset_manager@' + domain
    grant_permission = iroha.transaction([
        iroha.command('GrantPermission', account_id='admin@test', permission=can_set_my_account_detail)
    ], creator_account=account_id)
    ic.sign_transaction(grant_permission, user_private_key)
    send_transaction_and_print_status(grant_permission)
    account_details = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id, key='ple_id', value=ple_id)], creator_account='admin@test')
    ic.sign_transaction(account_details, admin_private_key)
    send_transaction_and_print_status(account_details)
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

def add_asset_to_user(account_id, asset_id, qty):
    global iroha
    """
    Add asset supply and assign to 'creator'
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id=asset_id, amount=qty)
    ])
    ic.sign_transaction(tx, admin_private_key)
    send_transaction_and_print_status(tx)

def create_and_issue_new_asset(asset,domain,precision,qty,account_id,description):
    global iroha
    user_tx = iroha.transaction(
        [iroha.command('CreateAsset', asset_name=asset,
            domain_id=domain, precision=precision)]    )
    ic.sign_transaction(user_tx, admin_private_key)
    send_transaction_and_print_status(user_tx)
    asset_id = asset + '#' + domain
    add_asset_to_admin(asset_id=asset_id,qty=qty)
    transfer_asset('admin@test',account_id,asset_id,description,domain,qty)

def join_plenteum_asset_ledger():
    """
    Creates Plenteum Domain 'domain' and asset 'coin#domain' with precision 2 and joins global network
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
    user_tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id=owner, dest_account_id=recepient,
                      asset_id=asset_id, description=description, amount=qty)])
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
    Get asset info
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

def get_domain_assets():
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
    user = json.loads(str(data.detail))
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return user

def get_user_password(account_id):
    global iroha
    """
    Get all the kv-storage entries for user@domain
    """
    query = iroha.query('GetAccountDetail', account_id=account_id)
    ic.sign_query(query, admin_private_key)
    response = net.send_query(query)
    data = response.account_detail_response
    user = json.loads(str(data.detail))
    pwd_hash = user['admin@test']['password']
    return pwd_hash