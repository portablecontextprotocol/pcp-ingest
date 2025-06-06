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
  * Get Sui Address


On this page
# Get Sui Address
An address is a way to uniquely and anonymously identify an account that exists on the Sui blockchain network. In other words, an address is a way for a user to store and use tokens on the Sui network, without providing any personally identifying information (such as email address, phone number, and so on). For example, if you want to purchase a number of SUI tokens to play a game, you must specify an address where these tokens are to be deposited.
The Sui address is unique, similarly to the way a social security number or a personal identification number is unique to one person. However, in Sui you can create and own multiple addresses, all of which are unique.
In Sui, an address is 32 bytes and is often encoded in hexadecimal with a `0x` prefix. For example, this is a valid Sui address: `0x02a212de6a9dfa3a69e22387acfbafbb1a9e591bd9d636e7895dcfc8de05f331`. You can use a Sui network explorer to find more information about this address and the objects it owns.
If you'd like to understand how a Sui address is derived from private keys and other cryptography related topics, see the Keys and Addresses topic.
## How to obtain a Sui address​
Sui provides multiple ways to obtain a Sui address. The following are the two most common.
### Sui Wallet​
One of the most straightforward ways to obtain a Sui address for first-time users is through the Sui Wallet Chrome browser extension. After you install the extension, there are several ways to create an address.
Open the Chrome Sui Wallet browser extension and then:
  * Use your gmail/twitch/facebook account (ZkLogin) and follow the on-screen instructions
  * Click **More Options** → **Create a new passphrase account**. Then follow the on-screen instructions.


For more information on the Sui Wallet and how to keep it secure, see the Sui Wallet documentation.
### Command line interface​
If you are using the Sui command line interface (CLI) to interact with the Sui network, you can use the `sui client` command to generate a new address. By default, when the Sui CLI runs for the first time it will prompt you to set up your local wallet, and then it generates one Sui address and the associated secret recovery phrase. Make sure you write down the secret recovery phrase and store it in a safe place.
To generate a new Sui address use `sui client new-address ed25519`, which specifies the keypair scheme flag to be of type `ed25519`.
For more information, see the Sui Client CLI documentation.
To see all the generated addresses in the local wallet on your machine, run `sui keytool list`. For more information about the keytool options, see the Sui Keytool CLI documentation.
The private keys associated with the Sui addresses are stored locally on the machine where the CLI is installed, in the `~/.sui/sui_config/sui.keystore` file. Make sure you do not expose this to anyone, as they can use it to get access to your account.
Previous
Connect to a Local Network
Next
Get SUI Tokens
  * How to obtain a Sui address
    * Sui Wallet
    * Command line interface


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
