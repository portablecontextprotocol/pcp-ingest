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
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Cryptography
  * Hashing


On this page
# Hashing
A cryptographic hash function is a widely used cryptographic primitive that maps an arbitrary length input to a fixed length output, the hash value. The hash function is designed to be a one-way function, which means that it is infeasible to invert the function to find the input data from a given hash value, and to be collision resistant, which means that it is infeasible to find two different inputs that map to the same hash value.
The Sui Move API supports the following cryptographic hash functions:
  * SHA2-256 as `std::hash::sha2_256`
  * SHA3-256 as `std::hash::sha3_256`
  * Keccak256 as `sui::hash::keccak256`
  * Blake2b-256 as `sui::hash::blake2b256`


## Usage​
The SHA2-256 and SHA3-256 hash functions are available in the Move Standard Library in the `std::hash` module. The following example shows how to use the SHA2-256 hash function in a smart contract:
```
module test::hashing_std {  
usestd::hash;  
usesui::object::{Self, UID};  
usesui::tx_context::TxContext;  
usesui::transfer;  
usestd::vector;  
  
/// Object that holds the output hash value.  
struct Outputhaskey, store {  
id: UID,  
value: vector<u8>  
    }  
  
publicfunhash_data(data: vector<u8>, recipient: address, ctx: &mut TxContext) {  
lethashed = Output {  
id: object::new(ctx),  
value: hash::sha2_256(data),  
        };  
// Transfer an output data object holding the hashed data to the recipient.  
        transfer::public_transfer(hashed, recipient)  
    }  
}  

```

The Keccak256 and Blake2b-256 hash functions are available through the `sui::hash` module in the Sui Move Library. An example of how to use the Keccak256 hash function in a smart contract is shown below. Notice that here, the input to the hash function is given as a reference. This is the case for both Keccak256 and Blake2b-256.
```
module test::hashing_sui {  
usesui::hash;  
usesui::object::{Self, UID};  
usesui::tx_context::TxContext;  
usesui::transfer;  
usestd::vector;  
  
/// Object that holds the output hash value.  
struct Outputhaskey, store {  
id: UID,  
value: vector<u8>  
    }  
  
publicfunhash_data(data: vector<u8>, recipient: address, ctx: &mut TxContext) {  
lethashed = Output {  
id: object::new(ctx),  
value: hash::keccak256(&data),  
        };  
// Transfer an output data object holding the hashed data to the recipient.  
        transfer::public_transfer(hashed, recipient)  
    }  
}  

```

Previous
Groth16
Next
ECVRF
  * Usage


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
