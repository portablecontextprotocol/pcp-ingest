Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search
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
      * Migrating to Move 2024
      * Custom Indexer
      * On-Chain Randomness
      * Querying Sui RPC with GraphQL (Alpha)
      * Migrating to GraphQL (Alpha)
      * Object-Based Local Fee Markets
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Advanced Topics


On this page
# Advanced Topics
Information in the Advanced Topics section covers coding practices, useful features, and other developer-focused considerations that might arise as you continue your development journey on Sui. The topics in this section aren't necessarily more difficult than other topics, but they include subjects you might not encounter or need to consider until you're developing more advanced solutions on the Sui network.
## Custom Indexer​
You can build custom indexers using the Sui micro-data ingestion framework. To create an indexer, you subscribe to a checkpoint stream with full checkpoint content. Establishing a custom indexer helps improve latency, allows pruning the data of your Sui Full node, and provides efficient assemblage of checkpoint data.
Go to Custom Indexer.
## Migrating to GraphQL​
See the Migrating to GraphQL guide to upgrade your smart contracts to use the GraphQL API.
This guide compares JSON-RPC queries to their equivalent GraphQL counterpart. While it is possible to systematically rewrite JSON-RPC queries (for example, `sui_getTotalTransactionBlocks`) to their GraphQL counterparts using this guide, it is recommended that you revisit your application's query patterns to take full advantage of the flexibility that GraphQL offers in serving queries that touch multiple potentially nested endpoints (for example transactions, balances, coins), and use the following examples to get a flavor of how the two APIs express similar concepts.
Go to Migrating to GraphQL.
Previous
zkLogin Example
Next
Migrating to Move 2024
  * Custom Indexer
  * Migrating to GraphQL


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
