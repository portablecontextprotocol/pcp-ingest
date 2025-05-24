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
  * Owner


On this page
# Owner
An Owner is an entity that can own an object. Each Owner is identified by a SuiAddress which represents either an Address (corresponding to a public key of an account) or an Object, but never both (it is not known up-front whether a given Owner is an Address or an Object).
```
typeOwnerimplementsIOwner{  
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
asAddress:Address  
asObject:Object  
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
}  

```

### Fields​
####  `Owner.**address**`●`SuiAddress!` non-null scalar​
####  `Owner.**objects**`●`MoveObjectConnection!` non-null object​
Objects owned by this object or address, optionally `filter`-ed.
#####  `Owner.objects.**first**`●`Int` scalar​
#####  `Owner.objects.**after**`●`String` scalar​
#####  `Owner.objects.**last**`●`Int` scalar​
#####  `Owner.objects.**before**`●`String` scalar​
#####  `Owner.objects.**filter**`●`ObjectFilter` input​
####  `Owner.**balance**`●`Balance` object​
Total balance of all coins with marker type owned by this object or address. If type is not supplied, it defaults to `0x2::sui::SUI`.
#####  `Owner.balance.**type**`●`String` scalar​
####  `Owner.**balances**`●`BalanceConnection!` non-null object​
The balances of all coin types owned by this object or address.
#####  `Owner.balances.**first**`●`Int` scalar​
#####  `Owner.balances.**after**`●`String` scalar​
#####  `Owner.balances.**last**`●`Int` scalar​
#####  `Owner.balances.**before**`●`String` scalar​
####  `Owner.**coins**`●`CoinConnection!` non-null object​
The coin objects for this object or address.
`type` is a filter on the coin's type parameter, defaulting to `0x2::sui::SUI`.
#####  `Owner.coins.**first**`●`Int` scalar​
#####  `Owner.coins.**after**`●`String` scalar​
#####  `Owner.coins.**last**`●`Int` scalar​
#####  `Owner.coins.**before**`●`String` scalar​
#####  `Owner.coins.**type**`●`String` scalar​
####  `Owner.**stakedSuis**`●`StakedSuiConnection!` non-null object​
The `0x3::staking_pool::StakedSui` objects owned by this object or address.
#####  `Owner.stakedSuis.**first**`●`Int` scalar​
#####  `Owner.stakedSuis.**after**`●`String` scalar​
#####  `Owner.stakedSuis.**last**`●`Int` scalar​
#####  `Owner.stakedSuis.**before**`●`String` scalar​
####  `Owner.**defaultSuinsName**`●`String` scalar​
The domain explicitly configured as the default domain pointing to this object or address.
#####  `Owner.defaultSuinsName.**format**`●`DomainFormat` enum​
####  `Owner.**suinsRegistrations**`●`SuinsRegistrationConnection!` non-null object​
The SuinsRegistration NFTs owned by this object or address. These grant the owner the capability to manage the associated domain.
#####  `Owner.suinsRegistrations.**first**`●`Int` scalar​
#####  `Owner.suinsRegistrations.**after**`●`String` scalar​
#####  `Owner.suinsRegistrations.**last**`●`Int` scalar​
#####  `Owner.suinsRegistrations.**before**`●`String` scalar​
####  `Owner.**asAddress**`●`Address` object​
####  `Owner.**asObject**`●`Object` object​
####  `Owner.**dynamicField**`●`DynamicField` object​
Access a dynamic field on an object using its name. Names are arbitrary Move values whose type have `copy`, `drop`, and `store`, and are specified using their type, and their BCS contents, Base64 encoded.
This field exists as a convenience when accessing a dynamic field on a wrapped object.
#####  `Owner.dynamicField.**name**`●`DynamicFieldName!` non-null input​
####  `Owner.**dynamicObjectField**`●`DynamicField` object​
Access a dynamic object field on an object using its name. Names are arbitrary Move values whose type have `copy`, `drop`, and `store`, and are specified using their type, and their BCS contents, Base64 encoded. The value of a dynamic object field can also be accessed off-chain directly via its address (e.g. using `Query.object`).
This field exists as a convenience when accessing a dynamic field on a wrapped object.
#####  `Owner.dynamicObjectField.**name**`●`DynamicFieldName!` non-null input​
####  `Owner.**dynamicFields**`●`DynamicFieldConnection!` non-null object​
The dynamic fields and dynamic object fields on an object.
This field exists as a convenience when accessing a dynamic field on a wrapped object.
#####  `Owner.dynamicFields.**first**`●`Int` scalar​
#####  `Owner.dynamicFields.**after**`●`String` scalar​
#####  `Owner.dynamicFields.**last**`●`Int` scalar​
#####  `Owner.dynamicFields.**before**`●`String` scalar​
### Interfaces​
####  `IOwner` interface​
Interface implemented by GraphQL types representing entities that can own objects. Object owners are identified by an address which can represent either the public key of an account or another object. The same address can only refer to an account or an object, never both, but it is not possible to know which up-front.
### Returned By​
`owner` query
### Member Of​
`AddressOwner` object ● `BalanceChange` object ● `Parent` object ● `Validator` object
Previous
OwnedOrImmutable
Next
PageInfo
  * Fields
  * Interfaces
  * Returned By
  * Member Of


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
