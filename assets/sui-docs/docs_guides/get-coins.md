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
  * Get SUI Tokens


On this page
# Get SUI Tokens
Sui faucet is a helpful tool where Sui developers can get free test SUI tokens to deploy and interact with their programs on Sui's Devnet and Testnet networks. There is no faucet for Sui Mainnet...
## Prerequisites​
To request tokens from the faucet, you must own a wallet address that can receive the SUI tokens. See the Get Sui Address topic if you don't already have an address or need to create a new one.
## Request test tokens through the online faucet​
https://faucet.sui.io/: Visit the online faucet to request SUI tokens.
How to use:
  1. Connect your wallet or paste your wallet address in the address field.
  2. Use the network dropdown to select the correct network.
  3. Click the **Request SUI** button.


To request more SUI, refresh your browser and click the Request SUI button again. The requests are rate limited, however, so too many requests results in a waiting period before you are able to request more tokens.
### Return unused Testnet SUI​
The Testnet faucet drains from a finite pool of SUI. If the pool empties, it disrupts faucet service for the rest of the community. To help ensure this doesn't happen, you can use the online faucet to return your unused SUI to the pool.
There are two ways to return unused Testnet SUI:
  * Connect your wallet to the online faucet, and click the **Return tokens to faucet** button. Approve the transaction using your wallet and your Testnet SUI are returned to the pool.
  * If you prefer not to connect your wallet, click the **Copy** button to the right of the return address and send the tokens via a separate transaction.


## Request test tokens through the CLI​
If you are using the Devnet or Testnet networks, or you spun up a local network, you can use the Sui CLI to request tokens for your address. The `sui client faucet` uses the active network and active address that is currently set in the Sui CLI by default, but you can specify custom data through the following two arguments:
  * `--address` argument to provide a specific address (or its alias),
  * `--url` argument to provide a custom faucet endpoint.


## Request test tokens through Discord​
  1. Join Discord. If you try to join the Sui Discord channel using a newly created Discord account, you may need to wait a few days for validation.
  2. Request test SUI tokens in the Sui #devnet-faucet or #testnet-faucet Discord channels. Send the following message to the channel with your client address: `!faucet <Your client address>`


## Request test tokens through wallet​
You can request test tokens within Sui Wallet.
## Request test tokens through cURL​
Use the following cURL command to request tokens directly from the faucet server:
```
curl --location --request POST 'https://faucet.devnet.sui.io/v1/gas' \  
--header 'Content-Type: application/json' \  
--data-raw '{  
    "FixedAmountRequest": {  
        "recipient": "<YOUR SUI ADDRESS>"  
    }  
}'  

```

If you're working with a local network, replace `'https://faucet.devnet.sui.io/v1/gas'` with the appropriate value based on which package runs your network:
  * `sui-faucet`: `http://127.0.0.1:5003/gas`
  * `sui`: `http://127.0.0.1:9123/gas`


## Request test tokens through TypeScript SDK​
You can also access the faucet using the Sui TypeScript-SDK.
```
import{ getFaucetHost, requestSuiFromFaucetV0 }from'@mysten/sui/faucet';  
  
// get tokens from the Devnet faucet server  
awaitrequestSuiFromFaucetV0({  
// connect to Devnet  
	host:getFaucetHost('devnet'),  
	recipient:'<YOUR SUI ADDRESS>',  
});  

```

## Test tokens on a local network​
If you are running a local Sui network, you can get tokens from your local faucet. See the Connect to a Local Network topic for details.
Previous
Get Sui Address
Next
Access Sui Data
  * Prerequisites
  * Request test tokens through the online faucet
    * Return unused Testnet SUI
  * Request test tokens through the CLI
  * Request test tokens through Discord
  * Request test tokens through wallet
  * Request test tokens through cURL
  * Request test tokens through TypeScript SDK
  * Test tokens on a local network


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
