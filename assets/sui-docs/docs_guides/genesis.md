Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Developer Guides
    * Getting Started
      * Install Sui
      * Connect to a Sui Network
      * Connect to a Local Network
      * Get Sui Address
      * Get SUI Tokens
      * Access Sui Data
    * Your First Sui dApp
    * Sui 101
    * Coins and Tokens
    * Stablecoins
    * NFTs
    * Cryptography
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides
    * Sui Full Node Configuration
    * Sui Validator Node Configuration
    * Genesis
    * Sui Node Monitoring
    * Updating a Full Node
    * Data Management
    * Database Snapshots
    * Sui Archives
    * Node Tools
    * Sui Exchange Integration Guide
    * Sui Bridge Node Configuration
    * Validator Committee
    * Validator Tasks


  *   * Operator Guides
  * Genesis


On this page
# Genesis
Genesis is the initial state of the Sui blockchain. To launch a network, the initial committee of validators collaborate by providing their validator information (public keys, network addresses, and so on) to a shared workspace. After all of the initial validators have contributed their information, Sui generates the initial, unsigned genesis checkpoint (checkpoint with sequence number 0) and each validator provides their signature. Sui aggregates these signatures to form a certificate on the genesis checkpoint. Sui bundles this checkpoint, as well as the initial objects, together into a single genesis.blob file that is used to initialize the state when running the `sui-node` binary for both validators and Full nodes.
## Genesis blob locations​
The genesis.blob files for each network are in the sui-genesis repository.
See Sui Full Node for how to get the genesis.blob file for each network.
Previous
Sui Validator Node Configuration
Next
Sui Node Monitoring
  * Genesis blob locations


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
