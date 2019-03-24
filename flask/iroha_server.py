import binascii
from iroha import IrohaCrypto as ic
from iroha import Iroha, IrohaGrpc
from iroha.primitive_pb2 import can_set_my_account_detail
import sys
import json
import os
import pandas as pd
import ipfsapi

ipfs_api = ipfsapi.connect('127.0.0.1', 5001)

def add_to_ipfs(ipfs_file):
    res = ipfs_api.add(ipfs_file)
    return res

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

def create_domain(domain):

    commands = [
        iroha.command('CreateDomain', domain_id=domain, default_role='user'),
    ]
    tx = ic.sign_transaction(
        iroha.transaction(commands), admin_private_key)
    send_transaction_and_print_status(tx)
    return

def add_peer_node():
    return

def generate_kp():
    global iroha
    pk = ic.private_key()
    user_private_key = pk
    user_public_key = ic.derive_public_key(user_private_key)
    return user_private_key, user_public_key

def create_users(user_name,domain,pwd_hash):
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
                      account_id=account_id, key='password', value=pwd_hash),])
    ic.sign_transaction(account_details, admin_private_key)
    send_transaction_and_print_status(account_details)
    user_pvt_file = './configs/' + account_id +'.priv'
    user_pub_file = './configs/' + account_id +'.pub'
    user_private_key_file = open(user_pvt_file,'wb+').write(user_public_key)
    user_public_key_file = open(user_pub_file,'wb+').write(user_private_key)
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
    transfer_asset_from_admin('admin@test',account_id,asset_id,description,domain,qty)

def transfer_asset(owner,recepient,asset_id,description,qty):
    user_iroha = Iroha(owner)
    net = IrohaGrpc()
    user_pvt_file = './configs/' + owner +'.priv'
    user_private_key = open(user_pvt_file).read()
    user_tx = user_iroha.transaction([
        user_iroha.command('TransferAsset', src_account_id=owner, dest_account_id=recepient,
                      asset_id=asset_id, description=description, amount=qty)])
    ic.sign_transaction(user_tx, user_private_key)
    send_transaction_and_print_status(user_tx)

def transfer_asset_from_admin(owner,recepient,asset_id,description,qty):
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

def get_account_assets(account_id):
    """
    List all the assets of user@domain
    """
    query = iroha.query('GetAccountAssets', account_id=account_id)
    ic.sign_query(query, admin_private_key)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    all_assets = []
    for asset in data:
        assets = dict()
        print('Asset id = {}, balance = {}'.format(
            asset.asset_id, asset.balance))
        assets[u'asset_id'] = asset.asset_id
        assets[u'balance'] = asset.balance
        all_assets.append(assets)
    df = pd.DataFrame.from_dict(all_assets)  
    return df
    
def get_domain_assets():
    """
    List all the assets of user@domain
    """
    query = iroha.query('GetAccountAssets', account_id='admin@test')
    ic.sign_query(query, admin_private_key)
    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    all_assets = []
    for asset in data:
        assets = dict()
        print('Asset id = {}, balance = {}'.format(
            asset.asset_id, asset.balance))
        assets[u'asset_id'] = asset.asset_id
        all_assets.append(assets)
    df = pd.DataFrame.from_dict(all_assets)  
    return df
    
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

def create_dummy_users(total):
    global iroha
    """
    test to create 100 dummy user accounts
    """
    i = 0
    while i < total:
        i += 1
        user_name = 'user' + str(i)
        domain = 'test'
        user_private_key, user_public_key = generate_kp()
        init_cmds = [
            iroha.command('CreateAccount', account_name=user_name, domain_id=domain,
                        public_key=user_public_key)
        ]
        init_tx = iroha.transaction(init_cmds)
        ic.sign_transaction(init_tx, admin_private_key)
        send_transaction_and_print_status(init_tx)
        account_id = user_name + '@' + domain
        user_pvt_file = './configs/' + account_id +'.priv'
        user_pub_file = './configs/' + account_id +'.pub'
        user_private_key_file = open(user_pvt_file,'wb+').write(user_public_key)    
        user_public_key_file = open(user_pub_file,'wb+').write(user_private_key)
    print("All users have been created")

def alice_creates_exchange_batch():
    alice_tx = iroha.transaction(
        [iroha.command(
            'TransferAsset', src_account_id='alice@test', dest_account_id='bob@test', asset_id='bitcoin#test',
            amount='1'
        )],
        creator_account='alice@test',
        quorum=2
    )
    bob_tx = iroha.transaction(
        [iroha.command(
            'TransferAsset', src_account_id='bob@test', dest_account_id='alice@test', asset_id='dogecoin#test',
            amount='2'
        )],
        creator_account='bob@test'
        # we intentionally omit here bob's quorum, since alice is the originator of the exchange and in general case
        # alice does not know bob's quorum.
        # bob knowing own quorum in case of accept should sign the tx using all the number of missing keys at once
    )
    iroha.batch(alice_tx, bob_tx, atomic=True)
    # sign transactions only after batch meta creation
    ic.sign_transaction(alice_tx, *alice_private_keys)
    send_batch_and_print_status(alice_tx, bob_tx)

def bob_accepts_exchange_request():
    global net
    q = ic.sign_query(
        Iroha('bob@test').query('GetPendingTransactions'),
        bob_private_keys[0]
    )
    pending_transactions = net.send_query(q)
    for tx in pending_transactions.transactions_response.transactions:
        if tx.payload.reduced_payload.creator_account_id == 'alice@test':
            # we need do this temporarily, otherwise accept will not reach MST engine
            del tx.signatures[:]
        else:
            ic.sign_transaction(tx, *bob_private_keys)
    send_batch_and_print_status(
        *pending_transactions.transactions_response.transactions)

def check_no_pending_txs(account_id):
    user_pvt_file = './configs/' + account_id +'.priv'
    user_private_key_file = open(user_pvt_file).read()        
    print(' ~~~ Checking pending txs:')
    print(
        net.send_query(
            ic.sign_query(
                iroha.query('GetPendingTransactions',
                            creator_account=account_id),
                user_private_key_file
            )
        )
    )
    print(' ~~~')

def bob_declines_exchange_request():
    print("""
    
    IT IS EXPECTED HERE THAT THE BATCH WILL FAIL STATEFUL VALIDATION
    
    """)
    global net
    q = ic.sign_query(
        Iroha('bob@test').query('GetPendingTransactions'),
        bob_private_keys[0]
    )
    pending_transactions = net.send_query(q)
    for tx in pending_transactions.transactions_response.transactions:
        if tx.payload.reduced_payload.creator_account_id == 'alice@test':
            # we need do this temporarily, otherwise accept will not reach MST engine
            del tx.signatures[:]
        else:
            # intentionally alice keys were used to fail bob's txs
            ic.sign_transaction(tx, *alice_private_keys)
            # zeroes as private keys are also acceptable
    send_batch_and_print_status(
        *pending_transactions.transactions_response.transactions)