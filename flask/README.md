# Iroha Flask REST Api

Documentation is Incomplete!

The goal is to build an rest server api that communicates with an Iroha Blockchain Daemon.

Whilst there are no restrictions in using your own database for your apps, kindly note Iroha utilizes PostGres so it can be used for your apps storage.

For this example app Iroha gets used to store user credentials which are retrieved by the server for loggin in etc.

requires python 3.7 + devtools

REST API Written In Flask with Simple GUI.

Create venv

activate

install requirements:

pip install requirments.txt

python app.py

the server can be reached via HTTP request to the respective end points
an example website with user dashboard and account/asset management features is also available, making it easier for admins.

for using iroha directly in your python app you can import iroha_server.py file to your app and call functions from there.

#features
##most are ToDo still

create users
create assets
transfer assets
create domain
view, set and grant access to account details (Iroha uses KV store)
assign users to custom domains(Private Sub Chains)
setup tool, script in python
    generates genesis block based on Cli parameters
    commandline key pair generation for admin, nodes and users
    docker checker
    starts run bash script & downloads all files
    starts build of daemon and CLi
    starts daemon with genesis block config
start network script

#custom features for Plenteum Asset Ledger

connect to Plenteum Domain
create asset manager profile
upload file to IPFS and link to asset
domain asset explorer