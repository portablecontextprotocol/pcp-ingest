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
          * Authenticator
          * DynamicFieldValue
          * EndOfEpochTransactionKind
          * ObjectOwner
          * ProgrammableTransaction
          * TransactionArgument
          * TransactionBlockKind
          * TransactionInput
          * UnchangedSharedObject
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
  * Unions
  * UnchangedSharedObject


On this page
# UnchangedSharedObject
Details pertaining to shared objects that are referenced by but not changed by a transaction. This information is considered part of the effects, because although the transaction specifies the shared object as input, consensus must schedule it and pick the version that is actually used.
```
unionUnchangedSharedObject=SharedObjectRead|SharedObjectDelete|SharedObjectCancelled  

```

### Possible types​
####  `UnchangedSharedObject.**SharedObjectRead**` object​
The transaction accepted a shared object as input, but only to read it.
####  `UnchangedSharedObject.**SharedObjectDelete**` object​
The transaction accepted a shared object as input, but it was deleted before the transaction executed.
####  `UnchangedSharedObject.**SharedObjectCancelled**` object​
The transaction accpeted a shared object as input, but its execution was cancelled.
### Member Of​
`UnchangedSharedObjectConnection` object ● `UnchangedSharedObjectEdge` object
Previous
TransactionInput
Next
Sui Full Node gRPC
  * Possible types
  * Member Of


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
