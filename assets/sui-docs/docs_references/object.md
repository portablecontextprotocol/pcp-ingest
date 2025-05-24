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
          * ActiveJwkConnection
          * ActiveJwkEdge
          * ActiveJwk
          * AddressConnection
          * AddressEdge
          * AddressOwner
          * Address
          * AuthenticatorStateCreateTransaction
          * AuthenticatorStateExpireTransaction
          * AuthenticatorStateUpdateTransaction
          * AvailableRange
          * BalanceChangeConnection
          * BalanceChangeEdge
          * BalanceChange
          * BalanceConnection
          * BalanceEdge
          * Balance
          * BridgeCommitteeInitTransaction
          * BridgeStateCreateTransaction
          * ChangeEpochTransaction
          * CheckpointConnection
          * CheckpointEdge
          * Checkpoint
          * CoinConnection
          * CoinDenyListStateCreateTransaction
          * CoinEdge
          * CoinMetadata
          * Coin
          * ConsensusCommitPrologueTransaction
          * ConsensusV2
          * DependencyConnection
          * DependencyEdge
          * DisplayEntry
          * DryRunEffect
          * DryRunMutation
          * DryRunResult
          * DryRunReturn
          * DynamicFieldConnection
          * DynamicFieldEdge
          * DynamicField
          * EndOfEpochTransactionKindConnection
          * EndOfEpochTransactionKindEdge
          * EndOfEpochTransaction
          * EpochConnection
          * EpochEdge
          * Epoch
          * EventConnection
          * EventEdge
          * Event
          * ExecutionResult
          * GasCoin
          * GasCostSummary
          * GasEffects
          * GasInput
          * GenesisTransaction
          * Immutable
          * Input
          * Linkage
          * MakeMoveVecTransaction
          * MergeCoinsTransaction
          * MoveCallTransaction
          * MoveDatatypeConnection
          * MoveDatatypeEdge
          * MoveDatatype
          * MoveEnumConnection
          * MoveEnumEdge
          * MoveEnumVariant
          * MoveEnum
          * MoveField
          * MoveFunctionConnection
          * MoveFunctionEdge
          * MoveFunctionTypeParameter
          * MoveFunction
          * MoveModuleConnection
          * MoveModuleEdge
          * MoveModule
          * MoveObjectConnection
          * MoveObjectEdge
          * MoveObject
          * MovePackageConnection
          * MovePackageEdge
          * MovePackage
          * MoveStructConnection
          * MoveStructEdge
          * MoveStructTypeParameter
          * MoveStruct
          * MoveType
          * MoveValue
          * ObjectChangeConnection
          * ObjectChangeEdge
          * ObjectChange
          * ObjectConnection
          * ObjectEdge
          * Object
          * OpenMoveType
          * OwnedOrImmutable
          * Owner
          * PageInfo
          * Parent
          * ProgrammableTransactionBlock
          * ProgrammableTransactionConnection
          * ProgrammableTransactionEdge
          * ProtocolConfigAttr
          * ProtocolConfigFeatureFlag
          * ProtocolConfigs
          * PublishTransaction
          * Pure
          * RandomnessStateCreateTransaction
          * RandomnessStateUpdateTransaction
          * Receiving
          * Result
          * SafeMode
          * ServiceConfig
          * SharedInput
          * SharedObjectCancelled
          * SharedObjectDelete
          * SharedObjectRead
          * Shared
          * SplitCoinsTransaction
          * StakeSubsidy
          * StakedSuiConnection
          * StakedSuiEdge
          * StakedSui
          * StorageFund
          * StoreExecutionTimeObservationsTransaction
          * SuinsRegistrationConnection
          * SuinsRegistrationEdge
          * SuinsRegistration
          * SystemParameters
          * TransactionBlockConnection
          * TransactionBlockEdge
          * TransactionBlockEffects
          * TransactionBlock
          * TransactionInputConnection
          * TransactionInputEdge
          * TransferObjectsTransaction
          * TypeOrigin
          * UnchangedSharedObjectConnection
          * UnchangedSharedObjectEdge
          * UpgradeTransaction
          * ValidatorConnection
          * ValidatorCredentials
          * ValidatorEdge
          * ValidatorSet
          * Validator
          * ZkLoginVerifyResult
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
  * Types
  * Objects
  * Object


On this page
# Object
An object in Sui is a package (set of Move bytecode modules) or object (typed data structure with fields) with additional metadata detailing its id, version, transaction digest, owner field indicating how this object can be accessed.
```
typeObjectimplementsIObject,IOwner{  
address:SuiAddress!  
objects(  
first:Int  
after:String  
last:Int  
before:String  
filter:ObjectFilter  
):MoveObjectConnection!  
balance(  
type:String  
):Balance  
balances(  
first:Int  
after:String  
last:Int  
before:String  
):BalanceConnection!  
coins(  
first:Int  
after:String  
last:Int  
before:String  
type:String  
):CoinConnection!  
stakedSuis(  
first:Int  
after:String  
last:Int  
before:String  
):StakedSuiConnection!  
defaultSuinsName(  
format:DomainFormat  
):String  
suinsRegistrations(  
first:Int  
after:String  
last:Int  
before:String  
):SuinsRegistrationConnection!  
version:UInt53!  
status:ObjectKind!  
digest:String  
owner:ObjectOwner  
previousTransactionBlock:TransactionBlock  
storageRebate:BigInt  
receivedTransactionBlocks(  
first:Int  
after:String  
last:Int  
before:String  
filter:TransactionBlockFilter  
scanLimit:Int  
):TransactionBlockConnection!  
bcs:Base64  
display:[DisplayEntry!]  
dynamicField(  
name:DynamicFieldName!  
):DynamicField  
dynamicObjectField(  
name:DynamicFieldName!  
):DynamicField  
dynamicFields(  
first:Int  
after:String  
last:Int  
before:String  
):DynamicFieldConnection!  
asMoveObject:MoveObject  
asMovePackage:MovePackage  
}  

```

### Fields​
####  `Object.**address**`●`SuiAddress!` non-null scalar​
####  `Object.**objects**`●`MoveObjectConnection!` non-null object​
Objects owned by this object, optionally `filter`-ed.
#####  `Object.objects.**first**`●`Int` scalar​
#####  `Object.objects.**after**`●`String` scalar​
#####  `Object.objects.**last**`●`Int` scalar​
#####  `Object.objects.**before**`●`String` scalar​
#####  `Object.objects.**filter**`●`ObjectFilter` input​
####  `Object.**balance**`●`Balance` object​
Total balance of all coins with marker type owned by this object. If type is not supplied, it defaults to `0x2::sui::SUI`.
#####  `Object.balance.**type**`●`String` scalar​
####  `Object.**balances**`●`BalanceConnection!` non-null object​
The balances of all coin types owned by this object.
#####  `Object.balances.**first**`●`Int` scalar​
#####  `Object.balances.**after**`●`String` scalar​
#####  `Object.balances.**last**`●`Int` scalar​
#####  `Object.balances.**before**`●`String` scalar​
####  `Object.**coins**`●`CoinConnection!` non-null object​
The coin objects for this object.
`type` is a filter on the coin's type parameter, defaulting to `0x2::sui::SUI`.
#####  `Object.coins.**first**`●`Int` scalar​
#####  `Object.coins.**after**`●`String` scalar​
#####  `Object.coins.**last**`●`Int` scalar​
#####  `Object.coins.**before**`●`String` scalar​
#####  `Object.coins.**type**`●`String` scalar​
####  `Object.**stakedSuis**`●`StakedSuiConnection!` non-null object​
The `0x3::staking_pool::StakedSui` objects owned by this object.
#####  `Object.stakedSuis.**first**`●`Int` scalar​
#####  `Object.stakedSuis.**after**`●`String` scalar​
#####  `Object.stakedSuis.**last**`●`Int` scalar​
#####  `Object.stakedSuis.**before**`●`String` scalar​
####  `Object.**defaultSuinsName**`●`String` scalar​
The domain explicitly configured as the default domain pointing to this object.
#####  `Object.defaultSuinsName.**format**`●`DomainFormat` enum​
####  `Object.**suinsRegistrations**`●`SuinsRegistrationConnection!` non-null object​
The SuinsRegistration NFTs owned by this object. These grant the owner the capability to manage the associated domain.
#####  `Object.suinsRegistrations.**first**`●`Int` scalar​
#####  `Object.suinsRegistrations.**after**`●`String` scalar​
#####  `Object.suinsRegistrations.**last**`●`Int` scalar​
#####  `Object.suinsRegistrations.**before**`●`String` scalar​
####  `Object.**version**`●`UInt53!` non-null scalar​
####  `Object.**status**`●`ObjectKind!` non-null enum​
The current status of the object as read from the off-chain store. The possible states are: NOT_INDEXED, the object is loaded from serialized data, such as the contents of a genesis or system package upgrade transaction. LIVE, the version returned is the most recent for the object, and it is not deleted or wrapped at that version. HISTORICAL, the object was referenced at a specific version or checkpoint, so is fetched from historical tables and may not be the latest version of the object. WRAPPED_OR_DELETED, the object is deleted or wrapped and only partial information can be loaded."
####  `Object.**digest**`●`String` scalar​
32-byte hash that identifies the object's current contents, encoded as a Base58 string.
####  `Object.**owner**`●`ObjectOwner` union​
The owner type of this object: Immutable, Shared, Parent, Address Immutable and Shared Objects do not have owners.
####  `Object.**previousTransactionBlock**`●`TransactionBlock` object​
The transaction block that created this version of the object.
####  `Object.**storageRebate**`●`BigInt` scalar​
The amount of SUI we would rebate if this object gets deleted or mutated. This number is recalculated based on the present storage gas price.
####  `Object.**receivedTransactionBlocks**`●`TransactionBlockConnection!` non-null object​
The transaction blocks that sent objects to this object.
`scanLimit` restricts the number of candidate transactions scanned when gathering a page of results. It is required for queries that apply more than two complex filters (on function, kind, sender, recipient, input object, changed object, or ids), and can be at most `serviceConfig.maxScanLimit`.
When the scan limit is reached the page will be returned even if it has fewer than `first` results when paginating forward (`last` when paginating backwards). If there are more transactions to scan, `pageInfo.hasNextPage` (or `pageInfo.hasPreviousPage`) will be set to `true`, and `PageInfo.endCursor` (or `PageInfo.startCursor`) will be set to the last transaction that was scanned as opposed to the last (or first) transaction in the page.
Requesting the next (or previous) page after this cursor will resume the search, scanning the next `scanLimit` many transactions in the direction of pagination, and so on until all transactions in the scanning range have been visited.
By default, the scanning range includes all transactions known to GraphQL, but it can be restricted by the `after` and `before` cursors, and the `beforeCheckpoint`, `afterCheckpoint` and `atCheckpoint` filters.
#####  `Object.receivedTransactionBlocks.**first**`●`Int` scalar​
#####  `Object.receivedTransactionBlocks.**after**`●`String` scalar​
#####  `Object.receivedTransactionBlocks.**last**`●`Int` scalar​
#####  `Object.receivedTransactionBlocks.**before**`●`String` scalar​
#####  `Object.receivedTransactionBlocks.**filter**`●`TransactionBlockFilter` input​
#####  `Object.receivedTransactionBlocks.**scanLimit**`●`Int` scalar​
####  `Object.**bcs**`●`Base64` scalar​
The Base64-encoded BCS serialization of the object's content.
####  `Object.**display**`●`[DisplayEntry!]` list object​
The set of named templates defined on-chain for the type of this object, to be handled off-chain. The server substitutes data from the object into these templates to generate a display string per template.
####  `Object.**dynamicField**`●`DynamicField` object​
Access a dynamic field on an object using its name. Names are arbitrary Move values whose type have `copy`, `drop`, and `store`, and are specified using their type, and their BCS contents, Base64 encoded.
Dynamic fields on wrapped objects can be accessed by using the same API under the Owner type.
#####  `Object.dynamicField.**name**`●`DynamicFieldName!` non-null input​
####  `Object.**dynamicObjectField**`●`DynamicField` object​
Access a dynamic object field on an object using its name. Names are arbitrary Move values whose type have `copy`, `drop`, and `store`, and are specified using their type, and their BCS contents, Base64 encoded. The value of a dynamic object field can also be accessed off-chain directly via its address (e.g. using `Query.object`).
Dynamic fields on wrapped objects can be accessed by using the same API under the Owner type.
#####  `Object.dynamicObjectField.**name**`●`DynamicFieldName!` non-null input​
####  `Object.**dynamicFields**`●`DynamicFieldConnection!` non-null object​
The dynamic fields and dynamic object fields on an object.
Dynamic fields on wrapped objects can be accessed by using the same API under the Owner type.
#####  `Object.dynamicFields.**first**`●`Int` scalar​
#####  `Object.dynamicFields.**after**`●`String` scalar​
#####  `Object.dynamicFields.**last**`●`Int` scalar​
#####  `Object.dynamicFields.**before**`●`String` scalar​
####  `Object.**asMoveObject**`●`MoveObject` object​
Attempts to convert the object into a MoveObject
####  `Object.**asMovePackage**`●`MovePackage` object​
Attempts to convert the object into a MovePackage
### Interfaces​
####  `IObject` interface​
Interface implemented by on-chain values that are addressable by an ID (also referred to as its address). This includes Move objects and packages.
####  `IOwner` interface​
Interface implemented by GraphQL types representing entities that can own objects. Object owners are identified by an address which can represent either the public key of an account or another object. The same address can only refer to an account or an object, never both, but it is not possible to know which up-front.
### Returned By​
`multiGetObjects` query ● `object` query
### Member Of​
`GasEffects` object ● `ObjectChange` object ● `ObjectConnection` object ● `ObjectEdge` object ● `OwnedOrImmutable` object ● `Owner` object ● `Receiving` object ● `SharedObjectRead` object
Previous
ObjectEdge
Next
OpenMoveType
  * Fields
  * Interfaces
  * Returned By
  * Member Of


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
