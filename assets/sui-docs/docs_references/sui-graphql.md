Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Sui RPC
    * GraphQL (Alpha)
      * Operations
        * Directives
        * Mutations
        * Queries
      * Types
        * Directives
        * Enums
        * Inputs
        * Interfaces
        * Objects
        * Scalars
        * Unions
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


  *   * Sui RPC
  * GraphQL (Alpha)


On this page
# GraphQL for Sui RPC (Alpha)
⚙️Early-Stage Feature
This content describes an alpha/beta feature or service. These early stage features and services are in active development, so details are likely to change.
This feature or service is currently available in
  * Devnet
  * Testnet
  * Mainnet


GraphQL for the Sui RPC is a public service that enables interacting with the Sui network.
To get started with GraphQL for the Sui RPC, check out the Getting Started guide. If you'd like to learn more about the concepts used in the GraphQL service, check out the GraphQL for Sui RPC concepts page.
Refer to Access Sui Data for an overview of options to access Sui network data.
Based on valuable feedback from the community, the GraphQL RPC release stage has been updated from beta to alpha. Refer to the high-level timeline for beta and GA releases in the previously linked document.
## Key Types​
All GraphQL API elements are accessible via the left sidebar, the following are good starting points to explore from.
  * "Queries" lists all top-level queries for reading the chain state, from reading details about addresses and objects to dryRunTransactionBlock, which has an execution-like interface but does not modify the chain.
  * "Mutations" lists operations that can modify chain state, like executeTransactionBlock.
  * Object is the type representing all on-chain objects (Move values and packages).
  * Address corresponds to account addresses (derived from the public keys of signatures that sign transactions) and can be used to query the objects owned by these accounts and the transactions they have signed or been affected by.
  * Owner represents any entity that can own a MoveObject to handle cases where it is not known whether the owner is an Object or an Address (for example, from the perspective of a Move object looking at its owner).


## Related links​
  * GraphQL migration: Migrating to GraphQL guides you through migrating Sui RPC projects from JSON-RPC to GraphQL.
  * GraphQL quick-start: Querying Sui RPC with GraphQL gets you started using GraphQL to query the Sui RPC for on-chain data.
  * GraphQL concepts: GraphQL for Sui RPC examines the elements of GraphQL that you should know to get the most from the service.


Previous
Sui RPC
Next
include
  * Key Types
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
