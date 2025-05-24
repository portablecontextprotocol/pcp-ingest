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
  * Sui CLI Cheat Sheet


On this page
# Sui CLI Cheat Sheet
The cheat sheet highlights common Sui CLI commands.
Download sheet as PDF
## Addresses & Aliases​
Command | Description  
---|---  
`sui client active-address` | Get the active address  
`sui client addresses` | List the addresses, their aliases, and the active address  
`sui client new-address ed25519` | Create a new address with ED25519 scheme  
`sui client new-address ed25519 MY_ALIAS` | Create a new address with ED25519 scheme and alias  
`sui client switch --address ADDRESS` | Make this the active address (accepts also an alias)  
`sui keytool convert PRIVATE_KEY` | Convert private key in Hex or Base64 to new format (Bech32 encoded 33 byte flag || private key starting with "suiprivkey")  
`sui keytool generate ed25519` | Generate a new keypair with ED25519 scheme and save it to file  
`sui keytool import INPUT KEY_SCHEME` | Add a new key to Sui CLI Keystore using either the input mnemonic phrase or a Bech32 encoded 33-byte flag || privkey starting with "suiprivkey"  
`sui keytool update-alias OLD_ALIAS NEW_ALIAS` | Update the alias of an address  
## Faucet & Gas​
Command | Description  
---|---  
`sui client faucet` | Get a SUI coin from the faucet associated with the active network  
`sui client faucet --address ADDRESS` | Get a SUI coin for the address (accepts also an alias)  
`sui client faucet --url CUSTOM_FAUCET_URL` | Get a SUI coin from custom faucet  
`sui client gas` | List the gas coins for the active address  
`sui client gas ADDRESS` | List the gas coins for the given address (accepts also an alias)  
## Network Command Description​
Command | Description  
---|---  
`sui client active-env` | Get the active environment  
`sui client envs` | List defined environments  
`sui client new-env --rpc URL --alias ALIAS` | Create a new environment with URL and alias  
`sui client switch --env ENV_ALIAS` | Switch to the given environment  
`sui genesis` | Bootstrap and initialize a new Sui network  
`sui start` | Start the local Sui network  
`sui-faucet` | Start a local faucet. Note this is a different binary  
## Create, Build, and Test a Move Project​
Command | Description  
---|---  
`sui move build` | Build the Move project in the current directory  
`sui move build --path PATH` | Build the Move project from the given path  
`sui move migrate PATH` | Migrate to Move 2024 for the package at provided path  
`sui move new PROJECT_NAME` | Create a new Move project in the given folder  
`sui move test` | Test the Move project in the current directory  
`sui move test --trace-execution` | Create an execution trace for the Move tests in the current directory. Use with the Move Trace Debugger extension.  
## Executing Transactions​
Command | Description  
---|---  
`sui client call \`  
`--package PACKAGE \`  
`--module MODULE \`  
`--function FUNCTION` | Call a Move package  
`sui client merge-coin \`  
`--primary-coin COIN_ID \`  
`--coin-to-merge COIN_ID` | Merge two coins  
`sui client split-coin \`  
`--coin-id COIN_ID \`  
`--amounts 1000` | Split a coin into two coins: one with 1000 MIST and the rest  
`sui client pay-sui \`  
`--input-coins COIN_ID \`  
`--recipients ADDRESS \`  
`--amounts 100000000` | Transfer 0.1 SUI to an address and use the same coin for gas  
`sui client transfer-sui \`  
`--sui-coin-object-id COIN_ID \`  
`--to ADDRESS` | Transfer SUI object to an address and use the same coin for gas  
## Programmable Transaction Blocks (PTBs)​
Command | Description  
---|---  
`sui client ptb --move-call p::m::f "<type>" args` | Call a Move function from a package and module  
`sui client ptb --make-move-vec "<u64>" "[1000,2000]"` | Make a Move vector with two elements of type u64  
`sui client ptb \`  
`--split-coins gas "[1000]" \`  
`--assign new_coins \`  
`--transfer-objects 				"[new_coins]" ADDRESS` | Split a gas coin and transfer it to address  
`sui client ptb --transfer-objects "[object_id]" ADDRESS` | Transfer an object to an address. Note that you can pass multiple objects in the array  
`sui client ptb \`  
`--move-call sui::tx_context::sender \`  
`--assign sender \`  
`--publish "." \`  
`--assign 				upgrade_cap \`  
`--transfer-objects "[upgrade_cap]" sender` | Publish a Move package, and transfer the upgrade capability to sender  
Previous
Sui CLI
Next
Sui Client CLI
  * Addresses & Aliases
  * Faucet & Gas
  * Network Command Description
  * Create, Build, and Test a Move Project
  * Executing Transactions
  * Programmable Transaction Blocks (PTBs)


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
