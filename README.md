# This is a Proof of Concept utilizing Hyperledger Iroha & Plenteum

This is a proof of concept for applications to be built using Hyperledger Iroha as permissioned ledger and Plenteum for public validation & record keeping of transactions.

This code is not intended to be used or distributed for any production purposes until ready.

Private keys are not stored in a secure manner making it easier for development and should be removed from your production code.

The API for the project will be done using Python 3's Flask framework, allowing easily customizable REST end points. 

Intergration with Plenteum is done via REST API calls to Plenteum App Services.

IPFS is used for storage of content. Users can upload via the front end, do a REST POST request or have users upload content themselves and simply supply the IPFS location hash.

This example is the basic source code for the Plenteum Asset Service, which allows users to create, store and issue assets sercurely and optionally integrate it with their private Iroha chain / Asset Service, allowing users to have both the security and transparency of a public blockchain whilst private organizations can keep their transactions on a seperate permissioned chain and join public nodes.

# What is Hyperledger Iroha?

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/960/badge)](https://bestpractices.coreinfrastructure.org/projects/960)
[![Snap Status](https://build.snapcraft.io/badge/hyperledger/iroha.svg)](https://build.snapcraft.io/user/hyperledger/iroha)
[![Build Status](https://jenkins.soramitsu.co.jp/buildStatus/icon?job=iroha/iroha-hyperledger/master)](https://jenkins.soramitsu.co.jp/job/iroha/job/iroha-hyperledger/job/master/)
[![Throughput Graph](https://graphs.waffle.io/hyperledger/iroha/throughput.svg)](https://waffle.io/hyperledger/iroha/metrics/throughput)

Blockchain platform Hyperledger Iroha is designed for simple creation and management of assets. This is a distributed ledger of transactions.

Check [overview](http://iroha.readthedocs.io/en/latest/overview.html) page of our documentation.

<img height="300px" src="docs/image_assets/Iroha_3_sm.png"
 alt="Iroha logo" title="Iroha" align="right" />

Iroha has the following features:
1. Creation and management of custom complex assets, such as currencies or indivisible rights, serial numbers, patents, etc.
2. Management of user accounts
3. Taxonomy of accounts based on _domains_ — or _sub-ledgers_ in the system
4. The system of rights and verification of user permissions for the execution of transactions and queries in the system
5. Validation of business rules for transactions and queries in the system

Among the non-functional requirements can be noted a high degree of network fault tolerance _(Byzantine Fault Tolerant)_.

## Documentation

Our documentation is hosted at ReadTheDocs service here: [http://iroha.readthedocs.io](http://iroha.readthedocs.io).
We have documentation in several languages available and you are welcome to contribute on [POEditor website](https://poeditor.com/join/project/SFpZw7o33o)!

## API Documentation

https://iroha.readthedocs.io/en/latest/api/index.html

### How to explore Iroha really fast?

Check [getting started](http://iroha.readthedocs.io/en/latest/getting_started/) section in your version of localized docs to start exploring the system.

### How to build Iroha?

Use [build guide](http://iroha.readthedocs.io/en/latest/guides/build.html), which might be helpful if you want to modify the code and contribute.

### Is there SDK available?

Yes, in [Java](http://iroha.readthedocs.io/en/latest/guides/libraries/java.html), [Python](http://iroha.readthedocs.io/en/latest/guides/libraries/python.html), [Javascript](http://iroha.readthedocs.io/en/latest/guides/libraries/nodejs.html), builds for [Android](http://iroha.readthedocs.io/en/latest/guides/libraries/android.html), and [iOS](http://iroha.readthedocs.io/en/latest/guides/libraries/swift_ios.html).

### Are there any example applications?

[Android point app](https://github.com/hyperledger/iroha-android/tree/master/iroha-android-sample) and [JavaScript wallet](https://github.com/soramitsu/iroha-wallet-js).

### Use Case Examples from Qouted from Chapter 3 in Iroha Docs

We list a number of use cases and specific advantages that Hyperledger Iroha can introduce to these applications. We
hope that the applications and use cases will inspire developers and creators to further innovation with Hyperledger
Iroha.

3.1 Certificates in Education, Healthcare
Hyperledger Iroha incorporates into the system multiple certifying authorities such as universities, schools, and medical institutions. Flexible permission model used in Hyperledger Iroha allows building certifying identities, and grant
certificates. The storage of explicit and implicit information in users’ account allows building various reputation and
identity systems.

By using Hyperledger Iroha each education or medical certificate can be verified that it was issued by certain certifying
authorities. Immutability and clear validation rules provide transparency to health and education significantly reducing
the usage of fake certificates.

3.1.1 Example
Imagine a medical institution registered as a hospital domain in Hyperledger Iroha. This domain has certified and
registered workers each having some role, e.g. physician, therapist, nurse. Each patient of the hospital has
an account with full medical history. Each medical record, like blood test results, is securely and privately stored in the
account of the patient as JSON key/values. Rules in hospital domain are defined such that only certified medical
workers and the user can access the personal information. The medical data returned by a query is verified that it
comes from a trusted source.

Hospital is tied to a specific location, following legal rules of that location, like storing personal data of citizens
only in specific regions(privacy rules). A multi-domain approach in Hyperledger Iroha allows sharing information
across multiple countries not violating legal rules. For example, if the user makoto@hospital decides to share
personal case history with a medical institution in another country, the user can use grant command with permission
can_get_my_acc_detail.

Similar to a medical institution, a registered university in Hyperledger Iroha has permissions to push information to
the graduated students. A diploma or certificate is essentially Proof-of-Graduation with a signature of recognized
University. This approach helps to ease hiring process, with an employer making a query to Hyperledger Iroha to get
the acquired skills and competence of the potential employee.

3.2 Cross-Border Asset Transfers
Hyperledger Iroha provides fast and clear trade and settlement rules using multi-signature accounts and atomic exchange. Asset management is easy as in centralized systems while providing necessary security guarantees. By
simplifying the rules and commands required to create and transfer assets, we lower the barrier to entry, while at the
same time maintaining high-security guarantees.

3.2.1 Example

For example1
, a user might want to transfer the ownership of a car. User haruto has registered owner-asset relationship with a car of sora brand with parameters: {"id": "34322069732074686520616E73776572",
"color": "red", "size": "small"}. This ownership is fixed in an underlying database of the system
with copies at each validating peer. To perform the transfer operation user haruto creates an offer, i.e. a multisignature transaction with two commands: transfer to user haru the car identifier and transfer some amount
of usd tokens from haru to haruto. Upon receiving the offer haru accepts it by signing the multi-signature
transaction, in this case, transaction atomically commits to the system.
Hypeledger Iroha has no built-in token, but it supports different assets from various creators. This approach allows
building a decentralized exchange market. For example, the system can have central banks from different countries to
issue assets.

3.3 Financial Applications

Hyperleger Iroha can be very useful in the auditing process. Each information is validated by business rules and is
constantly maintained by distinct network participants. Access control rules along with some encryption maintain
desired level of privacy. Access control rules can be defined at different levels: user-level, domain-level or systemlevel. At the user-level privacy rules for a specific individual are defined. If access rules are determined at domain or
system level, they are affecting all users in the domain. In Hyperledger Iroha we provide convenient role-based access
control rules, where each role has specific permissions.
Transactions can be traced with a local database. Using Iroha-API auditor can query and perform analytics on the data,
execute specific audit software. Hyperledger Iroha supports different scenarios for deploying analytics software: on
a local computer, or execute code on specific middleware. This approach allows analyzing Big Data application with
Hadoop, Apache, and others. Hypeledger Iroha serves as a guarantor of data integrity and privacy (due to the query
permissions restriction).

3.3.1 Example
For example, auditing can be helpful in financial applications. An auditor account has a role of the auditor with
permissions to access the information of users in the domain without bothering the user. To reduce the probability of
account hijacking and prevent the auditor from sending malicious queries, the auditor is typically defined as a multisignature account, meaning that auditor can make queries only having signatures from multiple separate identities.
The auditor can make queries not only to fetch account data and balance but also all transactions of a user, e.g. all
1 Currently not implemented

To efficiently analyze data of million users each Iroha node can work
in tandem with analytics software.
Multi-signature transactions are a powerful tool of Hyperledger Iroha that can disrupt tax system. Each transaction
in a certain domain can be as a multi-signature transaction, where one signature comes from the user (for example
asset transfer) and the second signature comes from special taxing nodes. Taxing nodes will have special validation
rules written using Iroha-API, e.g. each purchase in the certified stores must pay taxes. In other words, Iroha a
valid purchase transaction must contain two commands: money transfer(purchase) to the store and money transfer(tax
payment) to the government.

3.4 Identity Management
Hyperledger Iroha has an intrinsic support for identity management. Each user in the system has a uniquely identified
account with personal information, and each transaction is signed and associated with a certain user. This makes
Hyperledger Iroha perfect for various application with KYC (Know Your Customer) features.

3.4.1 Example
For example, insurance companies can benefit from querying the information of user’s transaction without worrying
about the information truthfulness. Users can also benefit from storing personal information on a blockchain since
authenticated information will reduce the time of claims processing. Imagine a situation where a user wants to make a
hard money loan. Currently, pre-qualification is a tedious process of gathering information about income, debts and information verification. Each user in Hyperledger Iroha has an account with verified personal information, such as owning assets, job positions, and debts. User income and debts can be traced using query GetAccountTransactions,
owning assets using query GetAccountAssets and job positions using GetAccountDetail. Each query returns verified result reducing the processing time of hard money loan will take only a few seconds. To incentivize
users to share personal information, various companies can come up with business processes. For example, insurance companies can create bonus discounts for users making fitness activities. Fitness applications can push private
Proof-of-Activity to the system, and the user can decide later to share information with insurance companies using
GrantPermission with permission can_get_my_acc_detail.

3.5 Supply Chain
Governance of a decentralized system and representing legal rules as a system’s code is an essential combination of
any supply chain system. Certification system used in Hyperledger Iroha allows tokenization of physical items and
embedding them into the system. Each item comes with the information about “what, when, where and why”.
Permission systems and restricted set of secure core commands narrows the attack vector and provides effortlessly a
basic level of privacy. Each transaction is traceable within a system with a hash value, by the credentials or certificates
of the creator.

3.5.1 Example
Food supply chain is a shared system with multiple different actors, such as farmers, storehouses, grocery stores, and
customers. The goal is to deliver food from a farmer’s field to the table of a customer. The product goes through many
stages, with each stage recorded in shared space. A customer scans a code of the product via a mobile device, in which
an Iroha query is encoded. Iroha query provides a full history with all stages, information about the product and the
farmer.

For example, gangreen is a registered farmer tomato asset creator, he serves as a guarantor tokenizing physical
items, i.e. associating each tomato with an Iroha tomato item. Asset creation and distribution processes are totally
transparent for network participants. Iroha tomato goes on a journey through a multitude of vendors to finally come
to user chad.

We simplified asset creation to just a single command CreateAsset without the need to create complex smart
contracts. One the major advantages of Hyperledger Iroha is in its ease, that allows developers to focus on the provided
value of their applications.

3.6 Fund Management
With the support of multisignature transactions it is possible to maintain a fund by many managers. In that scheme
investment can only be made after the confirmation of the quorum participants.

3.6.1 Example
The fund assets should be held at one account. Its signatories should be fund managers, who are dealing with investments and portfolio distributions. That can be added via AddSignatory command. All of the assets should be held
within one account, which signatories represent the fund managers. Thus the concrete exchanges can be performed
with the multisignature transaction so that everyone will decide on a particular financial decision. The one may confirm
a deal by sending the original transaction and one of managers’ signature. Iroha will maintain the transaction sending
so that the deal will not be completed until it receives the required number of confirmation, which is parametrized with
the transaction quorum parameter.


## Need help?

* Join [telegram chat](https://t.me/hyperledgeriroha) where the maintainers team is able to help you
* Communicate in Gitter chat with our development community [![Join the chat at https://gitter.im/hyperledger-iroha/Lobby](https://badges.gitter.im/hyperledger-iroha/Lobby.svg)](https://gitter.im/hyperledger-iroha/Lobby)
* Submit issues via GitHub Iroha repository
* Join [Hyperledger RocketChat](https://chat.hyperledger.org) #iroha channel to discuss your concerns and proposals
* Use mailing list to spread your word within Iroha development community [hyperledger-iroha@lists.hyperledger.org](mailto:hyperledger-iroha@lists.hyperledger.org)

## Iroha License

Iroha codebase is licensed under the Apache License,
Version 2.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Iroha documentation files are made available under the Creative Commons
Attribution 4.0 International License (CC-BY-4.0), available at
http://creativecommons.org/licenses/by/4.0/

## How To Get Started
# These are only instructions for running a local dev enviroment

Ensure that you have docker installed.

In scripts folder excecute the "run-iroha-dev.sh" script
this will download all of the required docker images and start up a docker network
with all of the configurations applied.

Iroha requires PostGres in order to run which is also automatically downloaded in the "run-iroha-dev.sh" script, which triggers the "run-pg-dev.sh" script.

For dev purposes, all of the required configurations have been edited from the example ones provided as the configuration differs slightly from what is provided on the quick start guide

Next you need to start the Iroha Daemon, Irohad which is located in build/bin folder.
first change into thelaunch the daemon with the following command

./build/bin/irohad --config ./flask/configs/config.docker --genesis_block ./flask/configs/genesis.block --keypair_name ./flask/configs/node0

You may interact with the Iroha
