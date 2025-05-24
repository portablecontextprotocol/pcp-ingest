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
      * Distributed Counter
      * Trustless Swap
      * Coin Flip
      * Review Rating
      * Blackjack
      * Plinko
      * Tic-Tac-Toe
      * Oracles
        * Sui Weather Oracle
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * App Examples
  * Oracles


On this page
# Oracles
Oracles are services that connect on-chain smart contracts with off-chain data. Blockchains are inherently isolated from outside sources for the purpose of security and reliability. Sui is no different, which means your projects cannot directly fetch real-world information, like stock prices, weather data, or sports scores. Oracles provide a bridge between the blockchain and external data sources, pulling in this information and making it available to smart contracts in a secure and verifiable way.
## Oracles available for the Sui network​
The guides in this section demonstrate how to create basic oracle services for your Sui projects. As your needs become more advanced, you might consider integrating third-party services to perform the heavy lifting. There are several oracle services available for the Sui network:
Service | Description  
---|---  
**Pyth** | Pyth is a blockchain oracle for market data. Check the Sui guide on the Pyth website to learn how to integrate into your Sui projects.  
**Stork** | Stork is an open data marketplace designed to address the limitations of traditional blockchain oracles. Check the Stork documentation for implementation details.  
**Supra** | Supra is a decentralized oracle network designed to connect blockchain smart contracts with real-world data, enhancing the functionality of decentralized applications (dApps) across various blockchain ecosystems. Check the Index Fund and Crowdfunding examples for how to integrate with Sui.  
**Switchboard** | Switchboard is a permissionless oracle network that seamlessly connects dApps to real-world data. Check the On Sui guide for integration details.  
## Oracle guides​
The following guides demonstrate how to build oracles on the Sui network. Currently, there is one guide but more are planned.
  * Sui Weather Oracle: Fetches weather data from OpenWeather API to provide real-time weather data for 1,000+ locations around the world.


Previous
Tic-Tac-Toe
Next
Sui Weather Oracle
  * Oracles available for the Sui network
  * Oracle guides


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
