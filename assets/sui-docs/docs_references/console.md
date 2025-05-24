Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Sui RPC
    * GraphQL (Alpha)
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


  *   * Sui CLI
  * Sui Console CLI


On this page
# Sui Console CLI
The Sui CLI `console` command provides command-level access to interact with the Sui network by wrapping the Sui Client CLI command in a shell-like functionality. This command spins up a new process and provides the user an environment for running all the available Sui Client CLI commands. In addition, it also offers command history support.
## Check Sui CLI installation​
Before you can use the Sui CLI, you must install it. To check if the CLI exists on your system, open a terminal or console and type the following command:
```
$ sui --version  

```

If the terminal or console responds with a version number, you already have the Sui CLI installed.
If the command is not found, follow the instructions in Install Sui to get the Sui CLI on your system.
## Commands​
For all available commands, consult the Sui Client CLI docs. To start the Sui Console, type `sui console`, which displays some information similar to the following:
```
🚀 ~ % sui console  
   _____       _    ______                       __  
  / ___/__  __(_)  / ____/___  ____  _________  / /__  
  \__ \/ / / / /  / /   / __ \/ __ \/ ___/ __ \/ / _ \  
 ___/ / /_/ / /  / /___/ /_/ / / / (__  ) /_/ / /  __/  
/____/\__,_/_/   \____/\____/_/ /_/____/\____/_/\___/  
--- Sui Console 1.14.0 ---  
  
Managed addresses : 2  
Active address: 0x3...235  
Keystore Type : File  
Keystore Path : Some("/Users/user/.sui/sui_config/sui.keystore")  
Active environment : testnet  
RPC URL: https://fullnode.testnet.sui.io:443  
[warn] Client/Server api version mismatch, client api version : 1.14.0, server api version : 1.13.0  
Connecting to Sui full node. API version 1.13.0  
  
Available RPC methods: ["sui_devInspectTransactionBlock", "sui_dryRunTransactionBlock", "sui_executeTransactionBlock",   
"sui_getChainIdentifier", "sui_getCheckpoint", "sui_getCheckpoints", "sui_getEvents", "sui_getLatestCheckpointSequenceNumber",   
"sui_getLoadedChildObjects", "sui_getMoveFunctionArgTypes", "sui_getNormalizedMoveFunction", "sui_getNormalizedMoveModule",   
"sui_getNormalizedMoveModulesByPackage", "sui_getNormalizedMoveStruct", "sui_getObject", "sui_getProtocolConfig",   
"sui_getTotalTransactionBlocks", "sui_getTransactionBlock", "sui_multiGetObjects", "sui_multiGetTransactionBlocks",   
"sui_tryGetPastObject", "sui_tryMultiGetPastObjects", "suix_getAllBalances", "suix_getAllCoins", "suix_getBalance",   
"suix_getCoinMetadata", "suix_getCoins", "suix_getCommitteeInfo", "suix_getDynamicFieldObject", "suix_getDynamicFields",   
"suix_getLatestSuiSystemState", "suix_getOwnedObjects", "suix_getReferenceGasPrice", "suix_getStakes", "suix_getStakesByIds",   
"suix_getTotalSupply", "suix_getValidatorsApy", "suix_queryEvents", "suix_queryTransactionBlocks", "suix_resolveNameServiceAddress",   
"suix_resolveNameServiceNames", "suix_subscribeEvent", "suix_subscribeTransaction", "unsafe_batchTransaction", "unsafe_mergeCoins",   
"unsafe_moveCall", "unsafe_pay", "unsafe_payAllSui", "unsafe_paySui", "unsafe_publish", "unsafe_requestAddStake",   
"unsafe_requestWithdrawStake", "unsafe_splitCoin", "unsafe_splitCoinEqual", "unsafe_transferObject", "unsafe_transferSui"]  
  
Welcome to the Sui interactive console.  
  
sui>-$  
  

```

Previous
Sui Client PTB CLI
Next
Sui Keytool CLI
  * Check Sui CLI installation
  * Commands


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
