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
      * Write a Move Package
      * Build and Test Packages
      * Publish a Package
      * Debugging
      * Client App with Sui TypeScript SDK
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
  * Your First Sui dApp


On this page
# Your First Sui dApp
Before you can create your first dApp on the Sui network, you must have Sui installed.
dApp stands for "decentralized application", which is an application that runs on a blockchain or decentralized network instead of a centralized server. Typical dApps do not run solely on the blockchain, but instead are composed of different pieces, like a TypeScript frontend that interacts with code that lives on a blockchain. Sui needs code written in Move for the pieces of a dApp that live on chain. These pieces are referred to as packages, modules, or smart contracts.
The instructions in this section walk you through writing a basic package, debugging and testing your code, and publishing. You need to follow these instructions in the order they appear to complete the exercise.
You use the `move` Sui CLI command for some instructions. The Sui CLI installs with the binaries, so you have it on your system if you follow the install instructions. To verify you have it installed, run the following command in a terminal or console.
```
$ sui --version  

```

If the console does not respond with a version number similar to the following, see the instructions to install Sui.
```
$ sui 1.xx.x-abc123xyz  

```

## Connecting to a network​
After installing Sui, you can connect to a network. Sui has three public networks (Devnet, Testnet, Mainnet), and you can also run and connect to a local Sui network. For each network, you need an on-chain address specific to that network. The address is an object with a unique ID in the form `0x8bd4613c004aac53d06bb7ceb7f46832c9ae69bdc105dfc5fcac225d2061fcac`. In addition to that address, you need SUI to pay for the gas fees associated with your on-chain activity, like publishing packages and making Move calls to those packages. For all networks besides Mainnet, you can get free SUI coins for your account to facilitate package development. For the purposes of this example, connect to the Testnet network.
### Connect to Testnet​
If you already have a network config set up, switch your active environment to Testnet. The following instruction is for the initial set up.
  1. In your terminal or console, use the following command to begin the configuration:
```
$ sui client  

```

  2. At the prompt, type `y` and press `Enter` to connect to a Sui Full node server.
  3. At the following prompt, type the address of the Testnet server (`https://fullnode.testnet.sui.io:443`) and press `Enter`.
  4. At the following prompt, type `testnet` to give the network an alias and press `Enter`. You can use the alias in subsequent commands instead of typing the complete URL.
  5. At the following prompt, type `0` and press `Enter`. The selection creates an address in the `ed25519` signing scheme.
  6. The response provides an alias for your address, the actual address ID, and a secret recovery phrase. Be sure to save this information for later reference. Because this is on the Testnet network, the security of this information is not as important as if it were on Mainnet.
  7. In your terminal or console, use the following command to get SUI for your account.
```
$ sui client faucet  

```

  8. You can confirm that you received SUI by using the following command. There may be a delay in receiving coins depending on the activity of the network.
```
$ sui client gas  

```



You are now connected to the Sui Testnet network and should have an account with available SUI.
## Related links​
  * Write a Move Package: Continue this example by creating the necessary Move code for your package.
  * Connect to a Sui Network: Connect to an available Sui network.
  * Connect to a Local Network: Start and connect to a local Sui network.
  * Get Sui Address: Get an address for the current Sui network.
  * Get SUI Tokens: Get SUI for the active address on Devnet, Testnet, or a local network.


Previous
Access Sui Data
Next
Write a Move Package
  * Connecting to a network
    * Connect to Testnet
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
