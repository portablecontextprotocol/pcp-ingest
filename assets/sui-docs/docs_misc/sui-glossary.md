Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Sui RPC
    * GraphQL (Alpha)
    * JSON-RPC
    * Sui Full Node gRPC
    * RPC Best Practices
  * Sui CLI
    * Sui CLI Cheat Sheet
    * Sui Client CLI
    * Sui Client PTB CLI
    * Sui Console CLI
    * Sui Keytool CLI
    * Sui Move CLI
    * Sui Validator CLI
  * Sui IDE Support
    * Move Analyzer
    * Move Trace Debugger
  * Sui SDKs
    * dApp Kit
    * Rust SDK
    * TypeScript SDK
    * zkSend SDK
  * Move
    * Framework
    * The Move Book
    * The Move Reference
  * Glossary
  * Contribute


  *   * Glossary


On this page
# Glossary
Find terms used in Sui defined below.
### Causal history​
Causal history is the relationship between an object in Sui and its direct predecessors and successors. This history is essential to the causal order Sui uses to process transactions. In contrast, other blockchains read the entire state of their world for each transaction, introducing latency.
### Causal order​
Causal order is a representation of the relationship between transactions and the objects they produce, laid out as dependencies. Validators cannot execute a transaction dependent on objects created by a prior transaction that has not finished. Rather than total order, Sui uses causal order (a partial order).
### Certificate​
A certificate is the mechanism proving a transaction was approved or certified. Validators vote on transactions, and aggregators collect a Byzantine-resistant-majority of these votes into a certificate and broadcasts it to all Sui validators, thereby ensuring finality.
### Epoch​
Operation of the Sui network is temporally partitioned into non-overlapping, fixed-duration epochs. During a particular epoch, the set of validators participating in the network is fixed.
### Equivocation​
Equivocation in blockchains is the malicious action of dishonest actors giving conflicting information for the same message, such as inconsistent or duplicate voting.
### Eventual consistency​
Eventual consistency is the consensus model employed by Sui; if one honest validator certifies the transaction, all of the other honest validators will too eventually.
### Finality​
Finality is the assurance a transaction will not be revoked. This stage is considered closure for an exchange or other blockchain transaction.
### Gas​
Gas refers to the computational effort required for executing operations on the Sui network. In Sui, gas is paid with the network's native currency SUI. The cost of executing a transaction in SUI units is referred to as the transaction fee.
### Genesis​
Genesis is the initial act of creating accounts and gas objects for a Sui network. Sui provides a `genesis` command that allows users to create and inspect the genesis object setting up the network for operation.
### Multi-writer objects​
Multi-writer objects are objects that are owned by more than one address. Transactions affecting multi-writer objects require consensus in Sui. This contrasts with transactions affecting only single-writer objects, which require only a confirmation of the owner's address contents.
### Object​
The basic unit of storage in Sui is object. In contrast to many other blockchains, where storage is centered around address and each address contains a key-value store, Sui's storage is centered around objects. Sui objects have one of the following primary states:
  * _Immutable_ - the object cannot be modified.
  * _Mutable_ - the object can be changed.


Further, mutable objects are divided into these categories:
  * _Owned_ - the object can be modified only by its owner.
  * _Shared_ - the object can be modified by anyone.


Immutable objects do not need this distinction because they have no owner.
### Proof-of-stake​
Proof-of-stake is a blockchain consensus mechanism where the voting weights of validators or validators is proportional to a bonded amount of the network's native currency (called their stake in the network). This mitigates Sybil attacks by forcing bad actors to gain a large stake in the blockchain first.
### Single-writer objects​
Single-writer objects are owned by one address. In Sui, transactions affecting only single-writer objects owned by the same address may proceed with only a verification of the sender's address, greatly speeding transaction times. These are _simple transactions_. See Single-Writer Apps for example applications of this simple transaction model.
### Smart contract​
A smart contract is an agreement based upon the protocol for conducting transactions in a blockchain. In Sui, smart contracts are written in the Move programming language.
### Sui​
Sui refers to the Sui blockchain, and the Sui open source project as a whole.
### SUI​
SUI is the native token to the Sui network.
### Total order​
Total order refers to the ordered presentation of the history of all transactions processed by a traditional blockchain up to a given time. This is maintained by many blockchain systems, as the only way to process transactions. In contrast, Sui uses a causal (partial) order wherever possible and safe.
### Transaction​
A transaction in Sui is a change to the blockchain. This may be a _simple transaction_ affecting only single-writer, single-address objects, such as minting an NFT or transferring an NFT or another token. These transactions may bypass the consensus protocol in Sui.
More _complex transactions_ affecting objects that are shared or owned by multiple addresses, such as asset management and other DeFi use cases, do go through consensus.
### Transfer​
A transfer is switching the owner address of a token to a new one via command in Sui. This is accomplished via the Sui CLI client command line interface. It is one of the more common of many commands available in the CLI client.
### Validator​
A validator in Sui plays a passive role analogous to the more active role of validators and minors in other blockchains. In Sui, validators do not continuously participate in the consensus protocol but are called into action only when receiving a transaction or certificate.
Previous
voting_power
Next
Docs Contribution
  * Causal history
  * Causal order
  * Certificate
  * Epoch
  * Equivocation
  * Eventual consistency
  * Finality
  * Gas
  * Genesis
  * Multi-writer objects
  * Object
  * Proof-of-stake
  * Single-writer objects
  * Smart contract
  * Sui
  * SUI
  * Total order
  * Transaction
  * Transfer
  * Validator


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
