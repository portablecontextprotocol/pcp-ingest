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
      * Distributed Counter
      * Trustless Swap
      * Coin Flip
      * Review Rating
      * Blackjack
      * Plinko
      * Tic-Tac-Toe
      * Oracles
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * App Examples


On this page
# App Examples
The ever-growing number of examples in this section showcase packages for the Sui blockchain. Extract techniques used in these examples to apply to your own Sui projects as they are written by Sui and Move experts.
Use dedicated nodes/shared services rather than public endpoints for production apps. The public endpoints maintained by Mysten Labs (`fullnode.<NETWORK>.sui.io:443`) are rate-limited, and support only 100 requests per 30 seconds. Do not use public endpoints in production applications with high traffic volume.
You can either run your own Full nodes, or outsource this to a professional infrastructure provider (preferred for apps that have high traffic). You can find a list of reliable RPC endpoint providers for Sui on the Sui Dev Portal using the **Node Service** tag.
## Examples​
Sui is dedicated to providing a wide range of examples to guide you in proper programming techniques for the Sui blockchain. This list will continue to grow, so check back often.
The projects are grouped by stack type and are sorted by complexity.
### Full-stack apps​
  * Distributed Counter: An end-to-end example that creates a basic decentralized counter that anyone can increment, but only the object owner can reset it. The example includes Move code to create the package and leverages the Sui TypeScript SDK to provide a basic frontend.
  * Trustless Swap: This example demonstrates trustless swaps on the Sui blockchain using a shared object as an escrow account.
  * Coin Flip: The Coin Flip app demonstrates on-chain randomness.
  * Reviews Rating: This example demonstrates implementing a reviews-rating platform for the food service industry on Sui.
  * Blackjack: This example demonstrates the logic behind an on-chain version of the popular casino card game, Blackjack.
  * Plinko: This example puts the classic Plinko game on chain, demonstrating use of cryptography-based strategies to create a fair and transparent game of chance.


### Smart contracts​
  * Tic-tac-toe: Three implementations of the classic tic-tac-toe game on the Sui network to demonstrate different approaches to user interaction.


### Smart contracts & Backend​
  * Weather Oracle: The Sui Weather Oracle demonstrates how to create a basic weather oracle that provides real-time weather data.


Previous
Object-Based Local Fee Markets
Next
Distributed Counter
  * Examples
    * Full-stack apps
    * Smart contracts
    * Smart contracts & Backend


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
