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
  * Migrating to GraphQL (Alpha)


On this page
# Migrating to GraphQL (Alpha)
⚙️Early-Stage Feature
This content describes an alpha/beta feature or service. These early stage features and services are in active development, so details are likely to change.
This feature or service is currently available in
  * Devnet
  * Testnet
  * Mainnet


This guide compares JSON-RPC queries to their equivalent GraphQL counterpart. While it is possible to systematically rewrite JSON-RPC queries (for example, `sui_getTotalTransactionBlocks`) to their GraphQL counterparts using this guide, it is recommended that you revisit your application's query patterns to take full advantage of the flexibility that GraphQL offers in serving queries that touch multiple potentially nested endpoints (for example transactions, balances, coins), and use the following examples to get a flavor of how the two APIs express similar concepts.
For a comprehensive list of all available GraphQL features, consult the reference.
Refer to Access Sui Data for an overview of options to access Sui network data.
Based on valuable feedback from the community, the GraphQL RPC release stage has been updated from beta to alpha. Refer to the high-level timeline for beta and GA releases in the previously linked document.
### Example 1: Get total transaction blocks​
The goal is to get the total number of transaction blocks in the network.
  * JSON-RPC
  * GraphQL


```
{  
"jsonrpc":"2.0",  
"id":1,  
"method":"sui_getTotalTransactionBlocks",  
"params":[]  
}  

```

```
query{  
checkpoint{  
networkTotalTransactions  
}  
}  

```

### Example 2: Get a specific transaction block​
The goal is to get the transaction block by its digest.
  * JSON-RPC
  * GraphQL


```
{  
"jsonrpc":"2.0",  
"id":1,  
"method":"sui_getTransactionBlock",  
"params":[  
"Hay2tj3GcDYcE3AMHrej5WDsHGPVAYsegcubixLUvXUF",  
{  
"showInput":true,  
"showRawInput":false,  
"showEffects":true,  
"showEvents":true,  
"showObjectChanges":false,  
"showBalanceChanges":false  
}  
]  
}  

```

```
query{  
transactionBlock(digest:"Hay2tj3GcDYcE3AMHrej5WDsHGPVAYsegcubixLUvXUF"){  
gasInput{  
gasSponsor{  
address  
}  
gasPrice  
gasBudget  
}  
effects{  
status  
timestamp  
checkpoint{  
sequenceNumber  
}  
epoch{  
epochId  
referenceGasPrice  
}  
}  
}  
}  

```

### Example 3: Get coin objects owned by an address​
The goal is to return all `Coin<0x2::sui::SUI>` objects an address owns.
  * JSON-RPC
  * GraphQL


```
query {  
"jsonrpc":"2.0",  
"id":1,  
"method":"suix_getCoins",  
"params":[  
"0x5094652429957619e6efa79a404a6714d1126e63f551f4b6c7fb76440f8118c9",//owner  
"0x2::sui::SUI",//coin type  
"0xe5c651321915b06c81838c2e370109b554a448a78d3a56220f798398dde66eab",//cursor  
3//limit  
]  
}  

```

```
query{  
address(address:"0x5094652429957619e6efa79a404a6714d1126e63f551f4b6c7fb76440f8118c9"){  
coins(  
first:3,  
after:"IAB3ha2PEA4ESRF4UErsJufJEwYpmSbCq7UNpxIHnLhG",  
type:"0x2::sui::SUI"  
){  
nodes{  
address  
}  
}  
}  
}  

```

The cursor is now passed in the `after` (or `before`) fields on the connection, and the limit in the `first` or `last` fields.
## New features​
There are also things that GraphQL can do, which JSON-RPC cannot:
### Example 4: Getting objects by type​
This query fetches the latest versions of objects of type `0x2::package::Publisher` that are currently live on-chain.
```
query{  
objects(filter:{type:"0x2::package::Publisher"}){  
nodes{  
address  
digest  
asMoveObject{  
contents{json}  
}  
}  
}  
}  

```

### Example 5: Paging through package versions​
The goal is to find all versions of the Sui framework, and list their modules:
```
query{  
packageVersions(address:"0x2"){  
nodes{  
version  
modules{  
nodes{  
name  
}  
}  
}  
}  
}  

```

## Related links​
  * GraphQL reference: Auto-generated GraphQL reference for Sui RPC.
  * GraphQL quick-start: Querying Sui RPC with GraphQL gets you started using GraphQL to query the Sui RPC for on-chain data.
  * GraphQL concepts: GraphQL for Sui RPC examines the elements of GraphQL that you should know to get the most from the service.


Previous
Querying Sui RPC with GraphQL (Alpha)
Next
Object-Based Local Fee Markets
  * Example 1: Get total transaction blocks
  * Example 2: Get a specific transaction block
  * Example 3: Get coin objects owned by an address
  * New features
    * Example 4: Getting objects by type
    * Example 5: Paging through package versions
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
