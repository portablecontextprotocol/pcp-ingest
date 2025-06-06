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
  * Sui Client CLI


On this page
# Sui Client CLI
The Sui CLI `client` command provides command-level access to interact with the Sui network. Typical uses for `sui client` include publishing Move smart contracts, getting the information of an object, executing transactions, or managing addresses.
## Check Sui CLI installation​
Before you can use the Sui CLI, you must install it. To check if the CLI exists on your system, open a terminal or console and type the following command:
```
$ sui --version  

```

If the terminal or console responds with a version number, you already have the Sui CLI installed.
If the command is not found, follow the instructions in Install Sui to get the Sui CLI on your system.
## Commands​
The following list itemizes all the available subcommands for the `sui client` command.
```
Usage: sui client [OPTIONS] [COMMAND]  
  
Commands:  
  active-address              Default address used for commands when none specified  
  active-env                  Default environment used for commands when none specified  
  addresses                   Obtain the Addresses managed by the client  
  balance                     List the coin balance of an address  
  call                        Call Move function  
  chain-identifier            Query the chain identifier from the rpc endpoint  
  dynamic-field               Query a dynamic field by its address  
  envs                        List all Sui environments  
  execute-signed-tx           Execute a Signed Transaction. This is useful when the user prefers to sign elsewhere and use this command to execute  
  execute-combined-signed-tx  Execute a combined serialized SenderSignedData string  
  faucet                      Request gas coin from faucet. By default, it will use the active address and the active network  
  gas                         Obtain all gas objects owned by the address. An address' alias can be used instead of the address  
  merge-coin                  Merge two coin objects into one coin  
  new-address                 Generate new address and keypair with keypair scheme flag {ed25519 | secp256k1 | secp256r1} with optional derivation path, default to m/44'/784'/0'/0'/0' for ed25519 or m/54'/784'/0'/0/0  
                                  for secp256k1 or m/74'/784'/0'/0/0 for secp256r1. Word length can be { word12 | word15 | word18 | word21 | word24} default to word12 if not specified  
  new-env                     Add new Sui environment  
  object                      Get object info  
  objects                     Obtain all objects owned by the address. It also accepts an address by its alias  
  pay                         Pay coins to recipients following specified amounts, with input coins. Length of recipients must be the same as that of amounts  
  pay-all-sui                 Pay all residual SUI coins to the recipient with input coins, after deducting the gas cost. The input coins also include the coin for gas payment, so no extra gas coin is required  
  pay-sui                     Pay SUI coins to recipients following following specified amounts, with input coins. Length of recipients must be the same as that of amounts. The input coins also include the coin for  
                                  gas payment, so no extra gas coin is required  
  publish                     Publish Move modules  
  split-coin                  Split a coin object into multiple coins  
  switch                      Switch active address and network(e.g., devnet, local rpc server)  
  tx-block                    Get the effects of executing the given transaction block  
  transfer                    Transfer object  
  transfer-sui                Transfer SUI, and pay gas with the same SUI coin object. If amount is specified, only the amount is transferred; otherwise the entire object is transferred  
  upgrade                     Upgrade Move modules  
  verify-bytecode-meter       Run the bytecode verifier on the package  
  verify-source               Verify local Move packages against on-chain packages, and optionally their dependencies  
  profile-transaction         Profile the gas usage of a transaction. Unless an output filepath is not specified, outputs a file `gas_profile_{tx_digest}_{unix_timestamp}.json` which can be opened in a flamegraph  
                                  tool such as speedscope  
  replay-transaction          Replay a given transaction to view transaction effects. Set environment variable MOVE_VM_STEP=1 to debug  
  replay-batch                Replay transactions listed in a file  
  replay-checkpoint           Replay all transactions in a range of checkpoints  
  help                        Print this message or the help of the given subcommand(s)  
  
Options:  
      --client.config <CONFIG>  Sets the file storing the state of our user accounts (an empty one will be created if missing)  
      --json                    Return command outputs in json format  
  -y, --yes  
  -h, --help                    Print help  

```

## JSON output​
Append the `--json` flag to commands to format responses in JSON instead of the more human-friendly default Sui CLI output. This can be useful for extremely large datasets, for example, as those results can have a troublesome display on smaller screens. In these cases, the `--json` flag is useful.
## Examples​
The following examples demonstrate some of the most often used commands.
### List available network environments​
Use the `sui client envs` command to find the network environments set up in the CLI. The information for these environments is also stored in the client.yaml file in the Sui configuration directory (`~/.sui/sui_config`).
```
╭────────┬────────────────────────────────────┬────────╮  
│ alias  │ url                                │ active │  
├────────┼────────────────────────────────────┼────────┤  
│ devnet │ https://fullnode.devnet.sui.io:443 │ *  	   │  
╰────────┴────────────────────────────────────┴────────╯  

```

### Create network environment​
Use `client new-env` to add details for a new network environment. This example creates an environment pointer to Sui Mainnet. Setting the `alias` value makes referencing the environment less prone to typographical errors. After running this command, Sui updates your client.yaml file in `~/.sui/sui_config` with the new information.
```
$ sui client new-env --alias=mainnet --rpc https://fullnode.mainnet.sui.io:443  
  
Added new Sui env [mainnet] to config.  

```

### Set current environment​
Use the `sui client switch` command to change the current network. This example switches the current network to `mainnet`.
```
$ sui client switch --env mainnet  

```

```
Active environment switched to [mainnet]  

```

If you run `sui client envs` after this command, you see the asterisk in the `active` column on the `mainnet` row of the table.
### Get current active address​
Use the `sui client active-address` command to reveal the current address. The CLI uses the current active address to execute address-specific CLI commands (like `sui client objects`) when you don't provide them with a Sui address value.
```
$ sui client active-address  

```

```
0x514692f08249c3e9951234ce29074695840422564bff85e424b56de462913e0d  

```

### Request a SUI coin from faucet​
If you use one of the standard public RPCs (for example, `fullnode.devnet.sui.io:443`), you can use the `faucet` command to request gas coins. If you use a custom faucet service, then pass in the URL to the faucet using the `--url` option. The `faucet` command works for a local network, as well. If you start your network with a custom faucet port, include the `--url` option.
```
$ sui client faucet  

```

```
Request successful. It can take up to 1 minute to get the coin. Run sui client gas to check your gas coins.  

```

### Get objects owned by an address​
Use `sui client objects` to list summary information about the objects the current active address owns. You can provide a Sui address value to the command to list objects for a particular address. This example lists objects for the current active address.
```
$ sui client objects 0x36df11369cf00ecf0be68d6ba965b0abe2e883bc5245911e3a29ebfa0aaf6b69  

```

```
╭───────────────────────────────────────────────────────────────────────────────────────╮  
| ╭────────────┬──────────────────────────────────────────────────────────────────────╮ │  
│ │ objectId   │  0xfffbb30ccb631f15f6cd36700589fc9c31cb04af28a95f3ed26d62daf3acb57f  │ │  
│ │ version	   │  33363559                                                        	  │ │  
│ │ digest 	   │  IY7/qsIJhliQL0uxwSzNYu0SMcn5AMsqQklSGngn1V0=                    	  │ │  
│ │ objectType │  0x0000..0002::coin::Coin                                        	  │ │  
│ ╰────────────┴──────────────────────────────────────────────────────────────────────╯ │  
│ ╭────────────┬──────────────────────────────────────────────────────────────────────╮ │  
│ │ objectId   │  0xfffe59fb6f78b1ced7f6537e69a205cc45d105270857bfd66332f9a627a38ae0  │ │  
│ │ version	   │  33370864                                                            │ │  
│ │ digest     │  b+tKChvujbCk/UCm8L+lflyb6Vjt7beB+uz6+ahUHmM=                    	  │ │  
│ │ objectType │  0x0000..0002::coin::Coin                                        	  │ │  
│ ╰────────────┴──────────────────────────────────────────────────────────────────────╯ │  
╰───────────────────────────────────────────────────────────────────────────────────────╯  

```

### Get complete object information​
Use `sui client object <OBJECT-ID>` to list object information for the ID you provide. This example displays the information for a Coin object.
```
$ sui client object 0xfffbb30ccb631f15f6cd36700589fc9c31cb04af28a95f3ed26d62daf3acb57f  

```

```
╭───────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ objectId  	  │  0xfffbb30ccb631f15f6cd36700589fc9c31cb04af28a95f3ed26d62daf3acb57f                                             	  │  
│ version   	  │  33363559                                                                                                       	  │  
│ digest    	  │  3FzvXJVVVcXb9H6dEXdARaY9EmxXyyNFduet3X4eYV4x                                                                   	  │  
│ objType   	  │  0x2::coin::Coin<0x2::sui::SUI>                                                                                 	  │  
│ ownerType 	  │  AddressOwner                                                                                                   	  │  
│ prevTx    	  │  ES2RQThjRE5u8rwiUEnhcnMoLA3cHeEGYJ8Pq98tmyAc                                                                   	  │  
│ storageRebate │  988000                                                                                                         	  │  
│ content   	  │ ╭───────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────╮ │  
│           	  │ │ dataType      	  │  moveObject                                                                            	    │ │  
│           	  │ │ type          	  │  0x2::coin::Coin<0x2::sui::SUI>                                                       	    │ │  
│           	  │ │ hasPublicTransfer │  true                                                                                    	  │ │  
│           	  │ │ fields        	  │ ╭─────────┬───────────────────────────────────────────────────────────────────────────────╮ │ │  
│           	  │ │               	  │ │ balance │  530076676                                                                	  │ │ │  
│           	  │ │               	  │ │ id  	  │ ╭────┬──────────────────────────────────────────────────────────────────────╮ │ │ │  
│           	  │ │               	  │ │     	  │ │ id │  0xfffbb30ccb631f15f6cd36700589fc9c31cb04af28a95f3ed26d62daf3acb57f  │ │ │ │  
│           	  │ │               	  │ │     	  │ ╰────┴──────────────────────────────────────────────────────────────────────╯ │ │ │  
│           	  │ │               	  │ ╰─────────┴───────────────────────────────────────────────────────────────────────────────╯ │ │  
│           	  │ ╰───────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────╯ │  
╰───────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯  

```

### Get dynamic fields of an object​
Use the `sui client dynamic-field <DYNAMIC-FIELD-ID>` command to list the details of the dynamic field with the ID you provide.
```
$ sui client dynamic-field 0x5  

```

```
╭─────────────┬───────────────────────────────────────────────────────────────────────────────────────────╮  
│ hasNextPage │  false                                                                                	  │  
│ nextCursor  │  0x5b890eaf2abcfa2ab90b77b8e6f3d5d8609586c3e583baf3dccd5af17edf48d1                   	  │  
│ data     	  │ ╭───────────────────────────────────────────────────────────────────────────────────────╮ │  
│         	  │ │ ╭────────────┬──────────────────────────────────────────────────────────────────────╮ │ │  
│         	  │ │ │ name   	   │ ╭───────┬───────╮                                                	  │ │ │  
│         	  │ │ │        	   │ │ type  │  u64  │                                                	  │ │ │  
│         	  │ │ │        	   │ │ value │  2	 │                                                	    │ │ │  
│         	  │ │ │        	   │ ╰───────┴───────╯                                                	  │ │ │  
│         	  │ │ │ bcsName	   │  LQM2cdzDY3                                                      	  │ │ │  
│         	  │ │ │ type   	   │  DynamicField                                                    	  │ │ │  
│         	  │ │ │ objectType │  0x3::sui_system_state_inner::SuiSystemStateInnerV2              	  │ │ │  
│         	  │ │ │ objectId   │  0x5b890eaf2abcfa2ab90b77b8e6f3d5d8609586c3e583baf3dccd5af17edf48d1  │ │ │  
│         	  │ │ │ version	   │  112                                                             	  │ │ │  
│         	  │ │ │ digest 	   │  HMrm1KNKjq3GfB1cWTRdvRo8gk7auhgvoZXaVoyEHqUR                    	  │ │ │  
│         	  │ │ ╰────────────┴──────────────────────────────────────────────────────────────────────╯ │ │  
│         	  │ ╰───────────────────────────────────────────────────────────────────────────────────────╯ │  
╰─────────────┴───────────────────────────────────────────────────────────────────────────────────────────╯  

```

### Send SUI or objects​
In this example, let's see how to transfer SUI or transfer an object from one address to another. First of all, there two main commands for sending SUI or transferring objects: `pay` and `transfer`. Both `pay` and `transfer` have a few sister commands: `pay-sui`, `pay-all-sui`, `transfer-sui`.
The differences between these commands are:
  * commands that end in `-sui` deal with Sui's native coin, and they use the input coints to pay for gas and for transferring SUI or the object.
  * `pay-` commands typically deal with coins and handle gas smashing for you, whereas `transfer` commands can handle the transfer of any object that has public transfer, meaning any object that has the `store` ability.
  * `pay` commands allow you to send coins to multiple recipients, whereas `transfer` commands only accept one recipient.
  * `pay-all-sui` is a special case of `pay-sui` that offers a way to transfer the entire balance after smashing.
  * `transfer-sui` is a legacy command and has been entirely superseded by `pay-sui` or `pay-all-sui` depending on whether an amount is specified or not.


Assume you have two addresses:
```
╭───────────────────┬────────────────────────────────────────────────────────────────────┬────────────────╮  
│ alias             │ address                                                            │ active address │  
├───────────────────┼────────────────────────────────────────────────────────────────────┼────────────────┤  
│ hungry-spodumene  │ 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea │ *              │  
│ eloquent-amber    │ 0x3d78abc33ccd173c521b4f9e78b21ea2c989960b631732c539efaa38bda30976 │                │  
╰───────────────────┴────────────────────────────────────────────────────────────────────┴────────────────╯  

```

Address `hungry-spodumene` has a few coins:
```
$ sui client gas hungry-spodumene  

```

```
╭────────────────────────────────────────────────────────────────────┬────────────────────┬──────────────────╮  
│ gasCoinId                                                          │ mistBalance (MIST) │ suiBalance (SUI) │  
├────────────────────────────────────────────────────────────────────┼────────────────────┼──────────────────┤  
│ 0x205972830acd8264a38b9a1776a1b72a1ae626fa23a4d1f12249349ce3b83c06 │ 200000000000       │ 200.00           │  
│ 0x56d76420a5bc7d356e3930e6a2ddc61cbbc0c87ea5c5f3cc3ac5952b4d52be5a │ 200000000000       │ 200.00           │  
│ 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52 │ 200000000000       │ 200.00           │  
│ 0xe373de9bdbd3dbd4f5f707f144c83af74a181cdb3903a953ee366f48e33865c7 │ 200000000000       │ 200.00           │  
│ 0xf7adb6aeb18eb409c03fe88cc31711b61a65333e0fdd88c1815d4ec75f713f31 │ 200000000000       │ 200.00           │  
╰────────────────────────────────────────────────────────────────────┴────────────────────┴──────────────────╯  

```

You want to send 0.5 SUI to `eloquent-amber`. Given that you have a few gas coins, you can use `pay`. If only one gas coin exists, then you need to use `transfer-sui` or `pay-sui`, or you would need to split the coin first to have another coin to use for paying gas. In this case, let's use the `pay-sui` command as you do not need to provide a separate gas coin to be used for the gas fees. In the command below, you set the recipient to be `eloquent-amber`, which coin to use to transfer SUI from, and the amount of SUI to transfer.
Beginning with the Sui `v1.24.1` release, the `--gas-budget` option is no longer required for CLI commands.
```
$ sui client pay-sui --recipients eloquent-amber --input-coins 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52 --amounts 500000000 --gas-budget 5000000  

```

The result is:
```
Transaction Digest: AsWkciVhLHeCmqVipjjyAA7Hv5y87pFjHS59K8m4zBJV  
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Transaction Data                                                                                             │  
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤  
│ Sender: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                                   │  
│ Gas Owner: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                                │  
│ Gas Budget: 5000000 MIST                                                                                     │  
│ Gas Price: 1000 MIST                                                                                         │  
│ Gas Payment:                                                                                                 │  
│  ┌──                                                                                                         │  
│  │ ID: 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52                                    │  
│  │ Version: 2                                                                                                │  
│  │ Digest: 9MEH7kr1YkBDx7pdUPCDnVb3FtPz9UZVeWmCot5Dhxqr                                                      │  
│  └──                                                                                                         │  
│                                                                                                              │  
│ Transaction Kind: Programmable                                                                               │  
│ ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────╮ │  
│ │ Input Objects                                                                                            │ │  
│ ├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │  
│ │ 0   Pure Arg: Type: address, Value: "0x3d78abc33ccd173c521b4f9e78b21ea2c989960b631732c539efaa38bda30976" │ │  
│ │ 1   Pure Arg: Type: u64, Value: "500000000"                                                              │ │  
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │  
│ ╭──────────────────────╮                                                                                     │  
│ │ Commands             │                                                                                     │  
│ ├──────────────────────┤                                                                                     │  
│ │ 0  SplitCoins:       │                                                                                     │  
│ │  ┌                   │                                                                                     │  
│ │  │ Coin: GasCoin     │                                                                                     │  
│ │  │ Amounts:          │                                                                                     │  
│ │  │   Input  1        │                                                                                     │  
│ │  └                   │                                                                                     │  
│ │                      │                                                                                     │  
│ │ 1  TransferObjects:  │                                                                                     │  
│ │  ┌                   │                                                                                     │  
│ │  │ Arguments:        │                                                                                     │  
│ │  │   Result 0        │                                                                                     │  
│ │  │ Address: Input  0 │                                                                                     │  
│ │  └                   │                                                                                     │  
│ ╰──────────────────────╯                                                                                     │  
│                                                                                                              │  
│ Signatures:                                                                                                  │  
│    eZc/iFO3i4Y8Le92zu9q75jILs+yg0sSXd1yPV9Dta+knH99VfkSCnzNQG1KbXSvY24wexmVtiuU6NkfudbiAQ==                  │  
│                                                                                                              │  
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯  
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Transaction Effects                                                                               │  
├───────────────────────────────────────────────────────────────────────────────────────────────────┤  
│ Digest: AsWkciVhLHeCmqVipjjyAA7Hv5y87pFjHS59K8m4zBJV                                              │  
│ Status: Success                                                                                   │  
│ Executed Epoch: 0                                                                                 │  
│                                                                                                   │  
│ Created Objects:                                                                                  │  
│  ┌──                                                                                              │  
│  │ ID: 0xa031d3f8fd53b5f9885172e1c6bd8b770b25e42371c9ee215c6d4b21b2b73241                         │  
│  │ Owner: Account Address ( 0x3d78abc33ccd173c521b4f9e78b21ea2c989960b631732c539efaa38bda30976 )  │  
│  │ Version: 3                                                                                     │  
│  │ Digest: Fq3maqq3pShgKw58Ssm8cS2j1pspfhanedVK2MMxfQWQ                                           │  
│  └──                                                                                              │  
│ Mutated Objects:                                                                                  │  
│  ┌──                                                                                              │  
│  │ ID: 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52                         │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ Version: 3                                                                                     │  
│  │ Digest: GFB9mpxTP4z6CCShTbvD58FYxtu9G4mnxN3JtFeRupM3                                           │  
│  └──                                                                                              │  
│ Gas Object:                                                                                       │  
│  ┌──                                                                                              │  
│  │ ID: 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52                         │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ Version: 3                                                                                     │  
│  │ Digest: GFB9mpxTP4z6CCShTbvD58FYxtu9G4mnxN3JtFeRupM3                                           │  
│  └──                                                                                              │  
│ Gas Cost Summary:                                                                                 │  
│    Storage Cost: 1976000 MIST                                                                     │  
│    Computation Cost: 1000000 MIST                                                                 │  
│    Storage Rebate: 978120 MIST                                                                    │  
│    Non-refundable Storage Fee: 9880 MIST                                                          │  
│                                                                                                   │  
│ Transaction Dependencies:                                                                         │  
│    GThyjtRFysBgVppXDc9iduNPzB2bLteXBnJcBEYXz4vG                                                   │  
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯  
╭─────────────────────────────╮  
│ No transaction block events │  
╰─────────────────────────────╯  
  
╭──────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Object Changes                                                                                   │  
├──────────────────────────────────────────────────────────────────────────────────────────────────┤  
│ Created Objects:                                                                                 │  
│  ┌──                                                                                             │  
│  │ ObjectID: 0xa031d3f8fd53b5f9885172e1c6bd8b770b25e42371c9ee215c6d4b21b2b73241                  │  
│  │ Sender: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                    │  
│  │ Owner: Account Address ( 0x3d78abc33ccd173c521b4f9e78b21ea2c989960b631732c539efaa38bda30976 ) │  
│  │ ObjectType: 0x2::coin::Coin<0x2::sui::SUI>                                                    │  
│  │ Version: 3                                                                                    │  
│  │ Digest: Fq3maqq3pShgKw58Ssm8cS2j1pspfhanedVK2MMxfQWQ                                          │  
│  └──                                                                                             │  
│ Mutated Objects:                                                                                 │  
│  ┌──                                                                                             │  
│  │ ObjectID: 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52                  │  
│  │ Sender: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                    │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea ) │  
│  │ ObjectType: 0x2::coin::Coin<0x2::sui::SUI>                                                    │  
│  │ Version: 3                                                                                    │  
│  │ Digest: GFB9mpxTP4z6CCShTbvD58FYxtu9G4mnxN3JtFeRupM3                                          │  
│  └──                                                                                             │  
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯  
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Balance Changes                                                                                   │  
├───────────────────────────────────────────────────────────────────────────────────────────────────┤  
│  ┌──                                                                                              │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ CoinType: 0x2::sui::SUI                                                                        │  
│  │ Amount: -501997880                                                                             │  
│  └──                                                                                              │  
│  ┌──                                                                                              │  
│  │ Owner: Account Address ( 0x3d78abc33ccd173c521b4f9e78b21ea2c989960b631732c539efaa38bda30976 )  │  
│  │ CoinType: 0x2::sui::SUI                                                                        │  
│  │ Amount: 500000000                                                                              │  
│  └──                                                                                              │  
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯  
  

```

Check the gas for the sender and the recipient's coins using `sui client gas <address>`. The sender now has 199.49 SUI for that gas coin that was used. 0.5 SUI was transferred, and the remaining 0.01 SUI paid the gas fees.
```
$ sui client gas  

```

```
╭────────────────────────────────────────────────────────────────────┬────────────────────┬──────────────────╮  
│ gasCoinId                                                          │ mistBalance (MIST) │ suiBalance (SUI) │  
├────────────────────────────────────────────────────────────────────┼────────────────────┼──────────────────┤  
│ 0x205972830acd8264a38b9a1776a1b72a1ae626fa23a4d1f12249349ce3b83c06 │ 200000000000       │ 200.00           │  
│ 0x56d76420a5bc7d356e3930e6a2ddc61cbbc0c87ea5c5f3cc3ac5952b4d52be5a │ 200000000000       │ 200.00           │  
│ 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52 │ 199498002120       │ 199.49           │  
│ 0xe373de9bdbd3dbd4f5f707f144c83af74a181cdb3903a953ee366f48e33865c7 │ 200000000000       │ 200.00           │  
│ 0xf7adb6aeb18eb409c03fe88cc31711b61a65333e0fdd88c1815d4ec75f713f31 │ 200000000000       │ 200.00           │  
╰────────────────────────────────────────────────────────────────────┴────────────────────┴──────────────────╯  

```

```
$ sui client gas eloquent-amber  

```

```
╭────────────────────────────────────────────────────────────────────┬────────────────────┬──────────────────╮  
│ gasCoinId                                                          │ mistBalance (MIST) │ suiBalance (SUI) │  
├────────────────────────────────────────────────────────────────────┼────────────────────┼──────────────────┤  
│ 0xa031d3f8fd53b5f9885172e1c6bd8b770b25e42371c9ee215c6d4b21b2b73241 │ 500000000          │ 0.50             │  
╰────────────────────────────────────────────────────────────────────┴────────────────────┴──────────────────╯  

```

If you want to transfer the whole object, you can use `sui client pay-all-sui` or `sui client transfer-sui` (without passing the amount):
```
$ sui client pay-sui --recipient eloquent-amber --input-coins 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52 --gas-budget 5000000  

```

or
```
$ sui client transfer-sui --to eloquent-amber --sui-coin-object-id 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52 --gas-budget 5000000  

```

Then check the gas for `eloquent-amber` again:
```
$ sui client gas eloquent-amber  

```

```
╭────────────────────────────────────────────────────────────────────┬────────────────────┬──────────────────╮  
│ gasCoinId                                                          │ mistBalance (MIST) │ suiBalance (SUI) │  
├────────────────────────────────────────────────────────────────────┼────────────────────┼──────────────────┤  
│ 0xa031d3f8fd53b5f9885172e1c6bd8b770b25e42371c9ee215c6d4b21b2b73241 │ 500000000          │ 0.50             │  
│ 0xc9b447fff18f13fa035e028534b8344d5fc8a8760248fad10155e78f44dc3a52 │ 199496992240       │ 199.49           │  
╰────────────────────────────────────────────────────────────────────┴────────────────────┴──────────────────╯  

```

### Replay a transaction​
Use the `sui client replay-transaction --tx-digest <TRANSACTION-DIGEST>` to re-execute a transaction locally and show the transaction effects. This command will fetch the transaction dependencies from the Full node specified in the client env. For transactions that happened quite far in the past, it is advised to set the client Full node to one that has non-pruned chain data for that transaction. This will also verify that the resulting effects from the locally executed transaction match the effects of the transaction stored on-chain.
You can add additional flags `--gas-info` and `--ptb-info` to this command to see more information about the transaction.
```
$ sui client replay-transaction --tx-digest 51MzJP2Uesvza8vXGpPCGbfLrY6UCfdvdoErN1z4oXPW  

```

```
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Transaction Effects                                                                               │  
├───────────────────────────────────────────────────────────────────────────────────────────────────┤  
│ Digest: 51MzJP2Uesvza8vXGpPCGbfLrY6UCfdvdoErN1z4oXPW                                              │  
│ Status: Success                                                                                   │  
│ Executed Epoch: 237                                                                               │  
│                                                                                                   │  
│ Mutated Objects:                                                                                  │  
│  ┌──                                                                                              │  
│  │ ID: 0x0000000000000000000000000000000000000000000000000000000000000006                         │  
│  │ Owner: Shared                                                                                  │  
│  │ Version: 20303014                                                                              │  
│  │ Digest: 3FyU88FpFFa2mhDFJWcabwQNdfaVaWvvnbjkfErD6AgJ                                           │  
│  └──                                                                                              │  
│                                                                                                   │  
│ Shared Objects:                                                                                   │  
│  ┌──                                                                                              │  
│  │ ID: 0x0000000000000000000000000000000000000000000000000000000000000006                         │  
│  │ Version: 20303013                                                                              │  
│  │ Digest: 7uGV3aHa9NDAWLX1UUyV1DG7wAuhfFkzSGo514wtco1C                                           │  
│  └──                                                                                              │  
│                                                                                                   │  
│ Gas Object:                                                                                       │  
│  ┌──                                                                                              │  
│  │ ID: 0x0000000000000000000000000000000000000000000000000000000000000000                         │  
│  │ Owner: Account Address ( 0x0000000000000000000000000000000000000000000000000000000000000000 )  │  
│  │ Version: 0                                                                                     │  
│  │ Digest: 11111111111111111111111111111111                                                       │  
│  └──                                                                                              │  
│                                                                                                   │  
│ Gas Cost Summary:                                                                                 │  
│    Storage Cost: 0                                                                                │  
│    Computation Cost: 0                                                                            │  
│    Storage Rebate: 0                                                                              │  
│    Non-refundable Storage Fee: 0                                                                  │  
│                                                                                                   │  
│ Transaction Dependencies:                                                                         │  
│    EvDLzYeKbrxDNHJomgrr2zwAJ7FJDtb2uNwfbonF2uGK                                                   │  
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯  
Execution finished successfully. Local and on-chain effects match.  

```

Use `sui client replay-batch --path <FILEPATH>` to replay several transactions listed in a newline-separated file. This will verify that all transactions local execution results match the effects on-chain.
### Profile a transaction​
Use the `sui client profile-transaction --tx-digest <TRANSACTION-DIGEST>` command to re-execute a transaction locally and produce a gas profile. Similar to the `replay` command, this command fetches the transaction dependencies from the Full node specified in the client environment that are needed to execute the transaction. During the local execution of the transaction, this command records all the Move function invocations and the gas cost breakdown for each invocation.
To enable the profiler, you must either install or build the Sui Client binary locally with the `--features tracing` flag if it has not already been built with that feature enabled.
```
$ cargo install --locked --git https://github.com/MystenLabs/sui.git --branch <BRANCH-NAME> --features tracing sui  

```

The command outputs a profile to the current working directory in the format `gas_profile_{tx_digest}_{unix_timestamp}.json`. You can include the optional flag `--profile-output </PATH/OUTPUT.json>` to write the profile to `/PATH/OUTPUT_{tx_digest}_{unix_timestamp}.json` instead. Use speedscope to inspect the profile.
To install speedscope run
```
$ npm install -g speedscope  

```

To open a profile in speedscope run
```
$ speedscope <PATH/PROFILE-OUTPUT-FILE>  

```

When looking at the profile in speedscope, there are three different views available from the top left menu: **Timer Order** , **Left Heavy** , and **Sandwich**. In each view, each bar's vertical width corresponds to the percentage of gas consumption incurred by the function, and you can hover your mouse over a bar or click a bar to see the computation units accrued by the function invocation. The transaction's total computation units, along with the storage computation units, are multiplied by the gas price to determine the gas cost of the transaction based on a tier system.
**Time Order** shows the callstack of function invocations from left to right in the order of invocation, while **Left Heavy** combines repeated sequences of nested invocations into a single combined call stack. **Left Heavy** displays these sequences from left to right by total incurred gas consumption per combined call stack. This is useful when there have been hundreds of repeated calls to the same function to quickly observe the total gas consumption over all calls to that function. In both these views, you can click the top section and drag to zoom in and out over different sections of the profile.
**Sandwich** view shows a list of discrete values that correspond to gas consumption per function, with **Total** showing gas cost incurred in all the functions called by the function, and **Self** showing the gas cost done by only the given function.
Observing a transaction's gas consumption provides useful insight of expected gas cost usage of a smart contract. When developing a smart contract, you can run a local network and publish the package to the local network. Then create a transaction that calls your published smart contract, and finally run the profiler on the transaction to see a breakdown of the gas cost.
## Publish a Move package​
One of the main uses of the `sui client` command is to publish smart contracts on the Sui network. This example switches the current environment to the Devnet network, then builds, tests, and publishes one of the existing Move examples available in the Sui repository: sui/examples/move
This example also makes use of `sui move` commands. To learn more about those commands, see Sui Move CLI.
  1. Open a terminal or console to the root of your local Sui repository and navigate to the `move_tutorial` example.
```
$ cd examples/move/first_package  

```

  2. Switch to the Devnet network. This command uses an alias, so the `devnet` value might be different for you, depending on the alias name set in your configuration (use `sui client envs` for a list of your defined networks and their aliases).
```
$ sui client switch --env devnet  

```

  3. Use `sui move build` to build the package. You must run this command at the same level as the package manifest file (Move.toml).
```
$ sui move build  

```

The console responds with the status of the build.
```
INCLUDING DEPENDENCY Sui  
INCLUDING DEPENDENCY MoveStdlib  
BUILDING first_package  

```

  4. Use `sui move test` to run the unit tests.
```
$ sui move test  

```

The console responds with updates of its progress.
```
INCLUDING DEPENDENCY Sui  
INCLUDING DEPENDENCY MoveStdlib  
BUILDING first_package  
Running Move unit tests  
[ PASS    ] 0x0::example::test_module_init  
[ PASS    ] 0x0::example::test_sword_transactions  
Test result: OK. Total tests: 2; passed: 2; failed: 0  

```

  5. Use the `sui client verify-bytecode-meter` to check if the module passes the bytecode meter.
```
$ sui client verify-bytecode-meter  

```

The console responds with the maximum allowed values, as well as the amount the package uses.
```
Running bytecode verifier for 1 modules  
╭──────────────────────────────────╮  
│ Module will pass metering check! │  
├────────┬────────────┬────────────┤  
│        │ Module     │ Function   │  
│ Max    │ 16000000   │ 16000000   │  
│ Used   │ 4565       │ 4565       │  
╰────────┴────────────┴────────────╯  

```

  6. Use `sui client gas` to verify that the active address has a gas coin for paying gas.
```
$ sui client gas  

```

In the case of this example, the console responds with the information that the address is coinless.
```
No gas coins are owned by this address  

```

  7. If you need coins, use `sui client faucet` (not available for Mainnet). For more information on getting gas tokens, see Get Sui Tokens.
```
$ sui client faucet  

```

  8. Use `sui client gas` to verify the current active address received the coins.
```
$ sui client gas  

```

```
╭────────────────────────────────────────────────────────────────────┬─────────────╮  
│ gasCoinId                                                          │ gasBalance  │  
├────────────────────────────────────────────────────────────────────┼─────────────┤  
│ 0x01b2795ba5800c8f7cb7d7c56abe19e24c656ed6764f3ccc5e66da3de52402a8 │ 10000000000 │  
╰────────────────────────────────────────────────────────────────────┴─────────────╯  

```

  9. Use `sui client publish` to publish the package, being sure to set an appropriate value for the `gas-budget` flag if you're using an older version of Sui. The console responds with the details of the publish. You can use `sui client object <OBJECT-ID>` to check the details of any of the objects from the process.
```
$ sui client publish --gas-budget 100000000 .  

```

```
 Transaction Digest: ABPd7v8BxLkcyHvX8Jt1SbneQRwzE9WzcEoptT2RDNVF  
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Transaction Data                                                                                             │  
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤  
│ Sender: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                                   │  
│ Gas Owner: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                                │  
│ Gas Budget: 5000000000 MIST                                                                                  │  
│ Gas Price: 1000 MIST                                                                                         │  
│ Gas Payment:                                                                                                 │  
│  ┌──                                                                                                         │  
│  │ ID: 0x01b2795ba5800c8f7cb7d7c56abe19e24c656ed6764f3ccc5e66da3de52402a8                                    │  
│  │ Version: 2                                                                                                │  
│  │ Digest: GZQwvpxLeTciVboEWeC8EZ2KYYU9o6XoBtW6LrA5Si1h                                                      │  
│  └──                                                                                                         │  
│                                                                                                              │  
│ Transaction Kind: Programmable                                                                               │  
│ ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────╮ │  
│ │ Input Objects                                                                                            │ │  
│ ├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤ │  
│ │ 0   Pure Arg: Type: address, Value: "0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea" │ │  
│ ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │  
│ ╭─────────────────────────────────────────────────────────────────────────╮                                  │  
│ │ Commands                                                                │                                  │  
│ ├─────────────────────────────────────────────────────────────────────────┤                                  │  
│ │ 0  Publish:                                                             │                                  │  
│ │  ┌                                                                      │                                  │  
│ │  │ Dependencies:                                                        │                                  │  
│ │  │   0x0000000000000000000000000000000000000000000000000000000000000001 │                                  │  
│ │  │   0x0000000000000000000000000000000000000000000000000000000000000002 │                                  │  
│ │  └                                                                      │                                  │  
│ │                                                                         │                                  │  
│ │ 1  TransferObjects:                                                     │                                  │  
│ │  ┌                                                                      │                                  │  
│ │  │ Arguments:                                                           │                                  │  
│ │  │   Result 0                                                           │                                  │  
│ │  │ Address: Input  0                                                    │                                  │  
│ │  └                                                                      │                                  │  
│ ╰─────────────────────────────────────────────────────────────────────────╯                                  │  
│                                                                                                              │  
│ Signatures:                                                                                                  │  
│    x437h/JxDAba2zkx4a2kEfz6iaXQ08T7+inyP5YkbmlSB5K7IYasM6onckjYDB19FNM1ZNqXm1z13VyTmDHXCw==                  │  
│                                                                                                              │  
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯  
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Transaction Effects                                                                               │  
├───────────────────────────────────────────────────────────────────────────────────────────────────┤  
│ Digest: ABPd7v8BxLkcyHvX8Jt1SbneQRwzE9WzcEoptT2RDNVF                                              │  
│ Status: Success                                                                                   │  
│ Executed Epoch: 0                                                                                 │  
│                                                                                                   │  
│ Created Objects:                                                                                  │  
│  ┌──                                                                                              │  
│  │ ID: 0x569828cc4e134ccccd7408def18b80af1465ac791fd4ef40483f6b16e2f00d95                         │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ Version: 3                                                                                     │  
│  │ Digest: 4iD7ZhsFS9iFuszqxBSEL6xZdcnWG76WGgU4D5PH1PeL                                           │  
│  └──                                                                                              │  
│  ┌──                                                                                              │  
│  │ ID: 0xde670ae990c8f20fd53e9f597a0da056bdb634175176602658e9da2c2ec9cb93                         │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ Version: 3                                                                                     │  
│  │ Digest: AV27tn7ePXhdDyDV9TCkSQZA3mkMei9DV63AmB4DEjGN                                           │  
│  └──                                                                                              │  
│  ┌──                                                                                              │  
│  │ ID: 0xe1d9d66b7a19b27ebda338a52593cd10e728f666f34ecd30a7cc2ad3fed186da                         │  
│  │ Owner: Immutable                                                                               │  
│  │ Version: 1                                                                                     │  
│  │ Digest: 4bzxMQgcSZoKzppNiRtQwAWDBvCgjr18gQi2H8Yk1tQZ                                           │  
│  └──                                                                                              │  
│ Mutated Objects:                                                                                  │  
│  ┌──                                                                                              │  
│  │ ID: 0x01b2795ba5800c8f7cb7d7c56abe19e24c656ed6764f3ccc5e66da3de52402a8                         │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ Version: 3                                                                                     │  
│  │ Digest: 46rvdbXkw5qqsBYbUGChzgFatJAYPmarPmFHgRRJiiU9                                           │  
│  └──                                                                                              │  
│ Gas Object:                                                                                       │  
│  ┌──                                                                                              │  
│  │ ID: 0x01b2795ba5800c8f7cb7d7c56abe19e24c656ed6764f3ccc5e66da3de52402a8                         │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ Version: 3                                                                                     │  
│  │ Digest: 46rvdbXkw5qqsBYbUGChzgFatJAYPmarPmFHgRRJiiU9                                           │  
│  └──                                                                                              │  
│ Gas Cost Summary:                                                                                 │  
│    Storage Cost: 9978800                                                                          │  
│    Computation Cost: 1000000                                                                      │  
│    Storage Rebate: 978120                                                                         │  
│    Non-refundable Storage Fee: 9880                                                               │  
│                                                                                                   │  
│ Transaction Dependencies:                                                                         │  
│    891Qjq6qDZ6SzAJiAg3CEaHobXrpDL5bAy2o45ZJPTuB                                                   │  
│    ESHcS3y3VCuaCVmWkKDx3EXX3icfPtj4bHhk86gaGWdo                                                   │  
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯  
╭─────────────────────────────╮  
│ No transaction block events │  
╰─────────────────────────────╯  
╭────────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Object Changes                                                                                     │  
├────────────────────────────────────────────────────────────────────────────────────────────────────┤  
│ Created Objects:                                                                                   │  
│  ┌──                                                                                               │  
│  │ ObjectID: 0x569828cc4e134ccccd7408def18b80af1465ac791fd4ef40483f6b16e2f00d95                    │  
│  │ Sender: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                      │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )   │  
│  │ ObjectType: 0xe1d9d66b7a19b27ebda338a52593cd10e728f666f34ecd30a7cc2ad3fed186da::example::Forge  │  
│  │ Version: 3                                                                                      │  
│  │ Digest: 4iD7ZhsFS9iFuszqxBSEL6xZdcnWG76WGgU4D5PH1PeL                                            │  
│  └──                                                                                               │  
│  ┌──                                                                                               │  
│  │ ObjectID: 0xde670ae990c8f20fd53e9f597a0da056bdb634175176602658e9da2c2ec9cb93                    │  
│  │ Sender: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                      │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )   │  
│  │ ObjectType: 0x2::package::UpgradeCap                                                            │  
│  │ Version: 3                                                                                      │  
│  │ Digest: AV27tn7ePXhdDyDV9TCkSQZA3mkMei9DV63AmB4DEjGN                                            │  
│  └──                                                                                               │  
│ Mutated Objects:                                                                                   │  
│  ┌──                                                                                               │  
│  │ ObjectID: 0x01b2795ba5800c8f7cb7d7c56abe19e24c656ed6764f3ccc5e66da3de52402a8                    │  
│  │ Sender: 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea                      │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )   │  
│  │ ObjectType: 0x2::coin::Coin<0x2::sui::SUI>                                                      │  
│  │ Version: 3                                                                                      │  
│  │ Digest: 46rvdbXkw5qqsBYbUGChzgFatJAYPmarPmFHgRRJiiU9                                            │  
│  └──                                                                                               │  
│ Published Objects:                                                                                 │  
│  ┌──                                                                                               │  
│  │ PackageID: 0xe1d9d66b7a19b27ebda338a52593cd10e728f666f34ecd30a7cc2ad3fed186da                   │  
│  │ Version: 1                                                                                      │  
│  │ Digest: 4bzxMQgcSZoKzppNiRtQwAWDBvCgjr18gQi2H8Yk1tQZ                                            │  
│  │ Modules: example                                                                                │  
│  └──                                                                                               │  
╰────────────────────────────────────────────────────────────────────────────────────────────────────╯  
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ Balance Changes                                                                                   │  
├───────────────────────────────────────────────────────────────────────────────────────────────────┤  
│  ┌──                                                                                              │  
│  │ Owner: Account Address ( 0x0fe375fff0ee40d20c54a7f2478b9b5c7eaa3625b7611f9661ec5faefb4a6fea )  │  
│  │ CoinType: 0x2::sui::SUI                                                                        │  
│  │ Amount: -10000680                                                                              │  
│  └──                                                                                              │  
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯  

```



## Help​
Each command has its own help section. For example, `sui client call --help` displays the following prompt:
```
Call Move function  
  
Usage: sui client call [OPTIONS] --package <PACKAGE> --module <MODULE> --function <FUNCTION>  
  
Options:  
      --package <PACKAGE>               Object ID of the package, which contains the module  
      --module <MODULE>                 The name of the module in the package  
      --function <FUNCTION>             Function name in module  
      --type-args <TYPE_ARGS>...        Type arguments to the generic function being called. All must be specified, or the call will fail  
      --args <ARGS>...                  Simplified ordered args like in the function syntax ObjectIDs, Addresses must be hex strings  
      --gas <GAS>                       ID of the gas object for gas payment. If not provided, a gas object with at least gas_budget value will be selected  
      --gas-budget <GAS_BUDGET>         An optional gas budget for this transaction (in MIST). If gas budget is not provided, the tool will first perform a dry  
                                        run to estimate the gas cost, and then it will execute the transaction. Please note that this incurs a small cost in  
                                        performance due to the additional dry run call  
      --dry-run                         Perform a dry run of the transaction, without executing it  
      --dev-inspect                     Perform a dev inspect  
      --serialize-unsigned-transaction  Instead of executing the transaction, serialize the bcs bytes of the unsigned transaction data (TransactionData) using  
                                        base64 encoding, and print out the string <TX_BYTES>. The string can be used to execute transaction with `sui client  
                                        execute-signed-tx --tx-bytes <TX_BYTES>`  
      --serialize-signed-transaction    Instead of executing the transaction, serialize the bcs bytes of the signed transaction data (SenderSignedData) using  
                                        base64 encoding, and print out the string <SIGNED_TX_BYTES>. The string can be used to execute transaction with `sui  
                                        client execute-combined-signed-tx --signed-tx-bytes <SIGNED_TX_BYTES>`  
      --json                            Return command outputs in json format  
  -h, --help                            Print help  
  -V, --version                         Print version  

```

Previous
Sui CLI Cheat Sheet
Next
Sui Client PTB CLI
  * Check Sui CLI installation
  * Commands
  * JSON output
  * Examples
    * List available network environments
    * Create network environment
    * Set current environment
    * Get current active address
    * Request a SUI coin from faucet
    * Get objects owned by an address
    * Get complete object information
    * Get dynamic fields of an object
    * Send SUI or objects
    * Replay a transaction
    * Profile a transaction
  * Publish a Move package
  * Help


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
