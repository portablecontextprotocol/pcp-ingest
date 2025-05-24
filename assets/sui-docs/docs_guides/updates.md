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
  * Updating a Full Node


On this page
# Updating a Full Node
## Sui release process​
Each Sui network is deployed on a consistent schedule. There are extenuating circumstances that might delay releases occasionally, but these delays are rare and communicated through official channels.
  * `devnet`: Deployed every week on Mondays.
  * `testnet`: Deployed every week on Tuesdays.
  * `mainnet`: Deployed every two weeks on Wednesdays.


For additional details, see each network's release schedule and configuration.
Whenever Sui releases a new version, you must update your Full node with the release to ensure compatibility with the network it connects to. For example, if you use Sui Testnet you should install the version of Sui running on Sui Testnet.
Any release that contains a protocol change will need to be followed before the protocol upgrade takes place (when enough stake within the validator set upgrades, the new protocol version is enacted in the next epoch). If you do not update your Full node, you will not be able to connect to the network after the protocol upgrade takes place.
## Communication​
Releases are announced on Sui Discord server and node-operators Google group.
### Discord channels​
  * `devnet`: `#devnet-updates`
  * `testnet`: `#tn-validator-announcements`, `#testnet-updates`, ⁠and `#node-announcements` channels.
  * `mainnet`: `⁠#mn-validator-announcements`, `#mainnet-updates`, and `#node-announcements` channels.


## Update your Full node​
You can track the latest version of Sui on the Sui Releases page on GitHub. The schedule for each network is available in the Network Release Schedule page.
It is reasonable to have to shut down your Full node to perform an update, whether that be a rolling restart in Kubernetes, or a systemctl stop on a Linux machine to replace the sui-node binary.
Previous
Sui Node Monitoring
Next
Data Management
  * Sui release process
  * Communication
    * Discord channels
  * Update your Full node


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
