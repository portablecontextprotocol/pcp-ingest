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
      * Sui On-Chain Signatures Verification in Move
      * Groth16
      * Hashing
      * ECVRF
      * Multisig Authentication
      * zkLogin Integration Guide
        * Configure OpenID Providers
        * zkLogin Example
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Cryptography
  * zkLogin Integration Guide
  * zkLogin Example


On this page
# zkLogin Example
The Sui community created an example to facilitate a comprehensive understanding of each step involved in Sui zkLogin for developers.
  * Sui zkLogin Example


![ZKLogin Overview](https://docs.sui.io/assets/images/overview-92aed0a2680b21bb9d8d4b168aac8972.png) This example breaks down the complete process of Sui zkLogin into seven steps, as follows:
  1. Generate ephemeral key pair
  2. Fetch JWT
  3. Decode JWT
  4. Generate salt
  5. Generate user Sui address
  6. Fetch ZK proof
  7. Assemble zkLogin signature


Each step includes corresponding code snippets, providing instructions on how to obtain the required data for each step.
## Operating environment​
The example runs in Sui Devnet. All data the user generates is stored locally on the client-side (browser). The acquisition of the zero-knowledge proof (ZK proof) is done through a call to the Mysten Labs-maintained proving service. Therefore, running the example does not require an additional deployed backend server (or a Docker container).
## Storage locations for key data​
The following table lists the storage location for key data the example uses:
Data | Storage location  
---|---  
Ephemeral key pair | `window.sessionStorage`  
Randomness | `window.sessionStorage`  
User salt | `window.localStorage`  
Max epoch | `window.localStorage`  
The user salt is stored long-term in the browser's `localStorage`. Consequently, provided the `localStorage` is not cleared manually, you can use the same JWT (in this example, logging in with the same Google account) to access the corresponding zkLogin address generated from the current salt value at any time.
Changing browsers or devices results in the inability to access previously generated Sui zkLogin addresses, even when using the same JWT.
## Troubleshooting​
  * **ZK Proof request failure:**
    * This might occur because of inconsistencies in the creation of multiple randomness or user salts, causing request failures. Click the **Reset Button** in the top right corner of the UI to restart the entire process.
  * **Request test tokens failure:**
    * This is because you have surpassed the faucet server request frequency limitations.
    * You can go to Sui #devnet-faucet or #testnet-faucet Discord channels to claim test coins.
  * Any suggestions are welcome on the project's GitHub repo through raised issues, and of course, pull requests are highly appreciated.


## Related links​
  * zkLogin Integration Guide
  * zkLogin FAQ
  * Configure OpenID Providers


Previous
Configure OpenID Providers
Next
Advanced Topics
  * Operating environment
  * Storage locations for key data
  * Troubleshooting
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
