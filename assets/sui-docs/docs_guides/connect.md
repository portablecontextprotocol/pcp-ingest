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
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Getting Started
  * Connect to a Sui Network


On this page
# Connect to a Sui Network
Sui has Mainnet, Devnet, and Testnet networks available. You can use one of the test networks, Devnet or Testnet, to experiment with the version of Sui running on that network. You can also spin up a local Sui network for local development.
The Sui Testnet and Devnet networks consist of several validator nodes to validate each network's transactions. Clients send transactions and read requests via this endpoint: `https://fullnode.<SUI-NETWORK-VERSION>.sui.io:443` using JSON-RPC.
You can request test SUI tokens through the Sui devnet-faucet and testnet-faucet Discord channels, depending on which version of the network you use. If connected to Localnet, use cURL to request tokens from your local faucet. The coins on these networks have no financial value. There is no faucet service for Mainnet.
See announcements about Sui in the #announcements Discord channel.
See the terms of service for using Sui networks.
Testnet and Devnet data persistence is not guaranteed. Devnet data is wiped regularly as part of scheduled software updates. The data on Testnet persists through the regular update process, but might be wiped when necessary. Testnet data wipes are announced ahead of time.
For more information about the release schedule of Sui networks, see Sui Network Release.
## Sui CLI​
Sui provides Sui command line interface (CLI) to interact with Sui networks:
  * Create and manage your private keys
  * Create example NFTs
  * Call and publish Move modules


## Environment set up​
First, Install Sui. After you install Sui, request SUI test tokens through Discord for the network you are using: Devnet or Testnet. If connected to Localnet, use cURL to request tokens from your local faucet.
To check whether Sui is already installed, run the following command:
```
$ which sui  

```

If Sui is installed, the command returns the path to the Sui binary. If Sui is not installed, it returns `sui not found`.
See the Sui Releases page to view the changes in each Sui release.
## Configure Sui client​
If you previously ran `sui genesis` to create a local network, it created a Sui client configuration file (client.yaml) that connects to `localhost` at `http://0.0.0.0:9000`. See Connect to a custom RPC endpoint to update the client.yaml file.
To connect the Sui client to a network, run the following command:
```
$ sui client  

```

If you receive the `sui-client` help output in the console, you already have a client.yaml file. See Connect to a custom RPC endpoint to add a new environment alias or to switch the currently active network.
The first time you start Sui client without having a client.yaml file, the console displays the following message:
```
Config file ["<PATH-TO-FILE>/client.yaml"] doesn't exist, do you want to connect to a Sui Full node server [y/N]?  

```

Press **y** and then press **Enter**. The process then requests the RPC server URL:
```
Sui Full node server URL (Defaults to Sui Testnet if not specified) :  

```

Press **Enter** to connect to Sui Testnet. To use a custom RPC server, Sui Devnet, or Sui Mainnet, enter the URL to the correct RPC endpoint and then press **Enter**.
If you enter a URL, the process prompts for an alias for the environment:
```
Environment alias for [<URL-ENTERED>] :  

```

Type an alias name and press **Enter**.
```
Select key scheme to generate keypair (0 for ed25519, 1 for secp256k1, 2 for secp256r1):  

```

Press **0** , **1** , or **2** to select a key scheme and the press **Enter**.
Sui returns a message similar to the following (depending on the key scheme you selected) that includes the address and 12-word recovery phrase for the address:
```
Generated new keypair for address with scheme "ed25519" [0xb9c83a8b40d3263c9ba40d551514fbac1f8c12e98a4005a0dac072d3549c2442]  
Secret Recovery Phrase : [cap wheat many line human lazy few solid bored proud speed grocery]  

```

### Connect to a custom RPC endpoint​
If you previously used `sui genesis` with the force option (`-f` or `--force`), your client.yaml file already includes two RPC endpoints: `localnet` at `http://0.0.0.0:9000` and `devnet` at `https://fullnode.devnet.sui.io:443`. You can view the defined environments with the `sui client envs` command, and switch between them with the `sui client switch` command.
If you previously installed a Sui client that connected to a Sui network, or created a local network, you can modify your existing client.yaml file to change the configured RPC endpoint. The `sui client` commands that relate to environments read from and write to the client.yaml file.
To check currently available environment aliases, run the following command:
```
$ sui client envs  

```

The command outputs the available environment aliases, with `(active)` denoting the currently active network.
```
localnet => http://0.0.0.0:9000 (active)  
devnet => https://fullnode.devnet.sui.io:443  

```

To add a new alias for a custom RPC endpoint, run the following command. Replace values in `<` `>` with values for your installation:
```
$ sui client new-env --alias <ALIAS> --rpc <RPC-SERVER-URL>  

```

To switch the active network, run the following command:
```
$ sui client switch --env <ALIAS>  

```

If you encounter an issue, delete the Sui configuration directory (`~/.sui/sui_config`) and reinstall the latest Sui binaries.
Previous
Install Sui
Next
Connect to a Local Network
  * Sui CLI
  * Environment set up
  * Configure Sui client
    * Connect to a custom RPC endpoint


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
