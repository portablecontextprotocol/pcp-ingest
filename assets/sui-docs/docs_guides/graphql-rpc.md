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
  * Querying Sui RPC with GraphQL (Alpha)


On this page
# Querying Sui RPC with GraphQL (Alpha)
Refer to Access Sui Data for an overview of options to access Sui network data.
Based on valuable feedback from the community, the GraphQL RPC release stage has been updated from beta to alpha. Refer to the high-level timeline for beta and GA releases in the previously linked document.
The quickest way to access the GraphQL service for Sui RPC is through the online IDE that provides a complete toolbox for fetching data and executing transactions on the network. The online IDE provides features such as auto-completion (use Ctrl+Space or just start typing), built-in documentation (Book icon, top-left), multi-tabs, and more.
The online IDE is available for Mainnet and Testnet. This guide contains various queries that you can try directly in the IDE.
  * Any existing addresses/object IDs in these examples refer to `mainnet` data only.
  * Both mainnet and testnet services are rate-limited to keep network throughput optimized.


For more details about some concepts used in the examples below, please see the GraphQL concepts page, and consult the reference for full documentation on the supported schema.
## Discovering the schema​
GraphQL introspection exposes the schema supported by the RPC service. The IDE's "Docs" pane (Book icon, top-left) and Search dialog (`Cmd`+`K` on macOS or `Ctrl`+`K` on Windows and Linux) offer a way to browse introspection output interactively.
The official documentation provides an overview on introspection, and how to interact with it programmatically.
## Finding the reference gas price for latest epoch​
```
query{  
epoch{  
referenceGasPrice  
}  
}  

```

## Finding information about a specific historical epoch​
This example finds the total stake rewards, the reference gas price, the number of checkpoints and the total gas fees for epoch 100. Note that in the query, the `id` argument is optional, and defaults to the latest epoch.
```
query{  
epoch(id:100)# note that id is optional, and without it, latest epoch is returned  
{  
epochId  
totalStakeRewards  
referenceGasPrice  
totalCheckpoints  
totalGasFees  
totalStakeSubsidies  
storageFund{  
totalObjectStorageRebates  
nonRefundableBalance  
}  
}  
}  

```

## Finding a transaction block by its digest​
This example gets a transaction block by its digest and shows information such as the gas sponsor's address, the gas price, the gas budget, and effects from executing that transaction block.
```
query{  
transactionBlock(digest:"FdKFgsQ9iRrxW6b1dh9WPGuNuaJWMXHJn1wqBQSqVqK2"){  
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

## Finding the last ten transactions that are not a system transaction​
```
query{  
transactionBlocks(last:10,filter:{kind:PROGRAMMABLE_TX}){  
nodes{  
digest  
kind{  
__typename  
}  
}  
}  
}  

```

## Finding all transactions that touched a given object​
This example finds all the transactions that touched (modified/transferred/deleted) a given object. This is useful for when we want to trace the flow of a Coin/StakeSui/NFT.
This example uses GraphQL variables and pagination. When using the online IDE, copy the variables JSON to the "Variables" window, below the main editor.
```
query($objectID:SuiAddress!){  
transactionBlocks(filter:{changedObject:$objectID}){  
nodes{  
sender{  
address  
}  
digest  
effects{  
objectChanges{  
nodes{  
address  
}  
}  
}  
}  
}  
}  

```

**Variables** :
```
{  
"objectID":"0x11c6ae8432156527fc2e12e05ac7db79f2e972510a823a4ef2e670f27ad7b52f"  
}  

```

## Filtering transaction blocks by a function​
This example finds the last ten transaction blocks that called the `public_transfer` function, (as a move call transaction command).
This example makes usage of the filter `last`, which indicates that the user only wants the last ten transaction blocks known to the service.
```
{  
transactionBlocks(  
last:10,  
filter:{  
function:"0x2::transfer::public_transfer"  
}  
){  
nodes{digest}  
}  
}  

```

## Finding transaction balance changes​
This example finds the balance changes of all the transactions where a given address called a staking-related function. This is useful when you want to get your staking or unstaking history.
```
query($address:SuiAddress!){  
transactionBlocks(filter:{  
function:"0x3::sui_system::request_add_stake"  
sentAddress:$address  
}){  
nodes{  
digest  
effects{  
balanceChanges{  
nodes{  
owner{  
address  
}  
amount  
}  
}  
}  
}  
}  
}  

```

**Variables** :
```
{  
"address":"0xa9ad44383140a07cc9ea62d185c12c4d9ef9c6a8fd2f47e16316229815862d23"  
}  

```

## Fetching a dynamic field on an object​
This example uses aliases and fragments.
```
queryDynamicField{  
object(  
address:"0xb57fba584a700a5bcb40991e1b2e6bf68b0f3896d767a0da92e69de73de226ac"  
){  
dynamicField(  
name:{  
type:"0x2::kiosk::Listing",  
bcs:"NLArx1UJguOUYmXgNG8Pv8KbKXLjWtCi6i0Yeq1VhfwA",  
}  
){  
...DynamicFieldSelect  
}  
}  
}  
  
fragmentDynamicFieldSelectonDynamicField{  
name{  
...MoveValueFields  
}  
value{  
...DynamicFieldValueSelection  
}  
}  
  
fragmentDynamicFieldValueSelectiononDynamicFieldValue{  
__typename  
...onMoveValue{  
...MoveValueFields  
}  
...onMoveObject{  
hasPublicTransfer  
contents{  
...MoveValueFields  
}  
}  
}  
  
fragmentMoveValueFieldsonMoveValue{  
type{  
repr  
}  
data  
bcs  
}  

```

## Fetching all dynamic fields on an object​
This query can be used to paginate over the dynamic fields of an object. This works even when the object in question is wrapped, by using the owner query, so can be used for iterating over the elements of on-chain data structures, like tables and bags. See The Move Book to learn more about dynamic collections available in Move.
This example uses fragments and variables.
```
query($id:SuiAddress!){  
owner(address:$id){  
dynamicFields{  
nodes{  
name{...Value}  
value{  
__typename  
...onMoveValue{  
...Value  
}  
...onMoveObject{  
contents{  
...Value  
}  
}  
}  
}  
}  
}  
}  
  
fragmentValueonMoveValue{  
type{  
repr  
}  
json  
}  

```

## Paginating checkpoints forward, five at a time​
```
query($after:String){  
checkpoints(first:5,after:$after){  
pageInfo{  
hasNextPage  
endCursor  
}  
nodes{  
digest  
timestamp  
}  
}  
}  

```

Sets up a paginated query, starting at the genesis checkpoint, reading five checkpoints at a time, in increasing order of sequence number. The value of `pageInfo.hasNextPage` determines whether there is another page to be read, and the value of `pageInfo.endCursor` is fed back in as the cursor to read `$after`.
This example uses GraphQL variables and pagination.
## Paginating checkpoints backwards, five at a time​
```
query($before:String){  
checkpoints(last:5,before:$before){  
pageInfo{  
hasPreviousPage  
startCursor  
}  
nodes{  
digest  
timestamp  
}  
}  
}  

```

Sets up a paginated query, starting at the latest indexed checkpoint, reading five checkpoints at a time, in decreasing order of sequence number. The value of `pageInfo.hasPreviousPage` determines whether there is another page to be read, and the value of `pageInfo.startCursor` is fed back in as the cursor to read `$before`.
This example uses GraphQL variables and pagination.
## Executing a transaction​
Transaction execution takes in two arguments, `txBytes` and `signatures`. `txBytes` is the serialized unsigned transaction data, which can be generated when using the Sui CLI's `client call` command, to call a Move function by passing the `--serialize-unsigned-transaction` flag. The `signatures` can be generated using Sui CLI's keytool command `sui keytool sign`. More information on Sui CLI can be found here.
```
mutation($tx:String!,$sigs:[String!]!){  
executeTransactionBlock(txBytes:$tx,signatures:$sigs){  
errors  
effects{  
status  
epoch{  
startTimestamp  
}  
gasEffects{  
gasSummary{  
computationCost  
}  
}  
}  
}  
}  

```

**Variables** :
```
{  
"tx":"AAACACAZXApmrHgzTs3FGDyXWka+wmMCy2IwOdKLmTWHb5PnFQEASlCnLAw4qfzLF3unH9or5/L7YpOlReaSEWfoEwhTqpavSxAAAAAAACCUFUCOn8ljIxcG9O+CA1bzqjunqr4DLDSzSoNCkUvu2AEBAQEBAAEAALNQHmLi4jgC5MuwwmiMvZEeV5kuyh+waCS60voE7fpzAa3v/tOFuqDvQ+bjBpKTfjyL+6yIg+5eC3dKReVwghH/rksQAAAAAAAgxtZtKhXTr1zeFAo1JzEqVKn9J1H74ddbCJNVZGo2I1izUB5i4uI4AuTLsMJojL2RHleZLsofsGgkutL6BO36c+gDAAAAAAAAQEIPAAAAAAAA",  
"sigs":[  
"AB4ZihXxUMSs9Ju5Cstuuf/hvbTvvycuRk2TMuagLYNJgQuAeXmKyJF9DAXUtL8spIsHrDQgemn4NmojcNl8HQ3JFqhnaTC8gMX4fy/rGgqgL6CDcbikawUUjC4zlkflwg=="  
]  
}  

```

## Other examples​
You can find other examples in the repository, grouped into sub-directories. For example, there are directories for transaction block effects, protocol configs, stake connection, and more.
Examples in the repository are designed to work with the version of GraphQL built at the same revision. The links above point to examples intended for GraphQL v2024.1, the latest production version at the time of writing.
## Related links​
  * GraphQL migration: Migrating to GraphQL guides you through migrating Sui RPC projects from JSON-RPC to GraphQL.
  * GraphQL concepts: GraphQL for Sui RPC examines the elements of GraphQL that you should know to get the most from the service.
  * GraphQL reference: Auto-generated GraphQL reference for Sui RPC.
  * Sui Testnet GraphiQL: Sui GraphiQL IDE for the Testnet network.
  * Sui Mainnet GraphiQL: Sui GraphiQL IDE for the Mainnet network.


Previous
On-Chain Randomness
Next
Migrating to GraphQL (Alpha)
  * Discovering the schema
  * Finding the reference gas price for latest epoch
  * Finding information about a specific historical epoch
  * Finding a transaction block by its digest
  * Finding the last ten transactions that are not a system transaction
  * Finding all transactions that touched a given object
  * Filtering transaction blocks by a function
  * Finding transaction balance changes
  * Fetching a dynamic field on an object
  * Fetching all dynamic fields on an object
  * Paginating checkpoints forward, five at a time
  * Paginating checkpoints backwards, five at a time
  * Executing a transaction
  * Other examples
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
