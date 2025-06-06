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
  * ECVRF


On this page
# Elliptic Curve Verifiable Random Function
A verifiable random function (VRF) is a cryptographic primitive that enables you to generate a random number and provide proof that the number used a secret key for generation. Anyone can verify the proof using the public key corresponding to the secret key, so you can use it as a random number generator (RNG) that generates outputs that anyone can verify. Applications that need verifiable randomness on chain can also benefit from its use.
## VRF construction​
The VRF used in the Move API in Sui is an elliptic curve VRF (ECVRF) following the CFRG VRF draft specifications version 15. It uses Ristretto255 elliptic curve group construction with the SHA-512 hash function. The nonce is generated according to RFC6979.
Any implementation following the same specifications with suite string `sui_vrf` (see section 5 in the VRF specs) can be used to compute VRF output and generate proofs.
The fastcrypto library provides a CLI tool for such an implementation and is used in the following example.
### Generate keys​
From the root of the `fastcrypto` repository, run the following command to generate a key pair:
```
$ cargo run --bin ecvrf-cli keygen  

```

This outputs a secret key and a public key in hex format. Both the secret and public keys are 32-byte strings:
```
Secret key: c0cbc5bf0b2f992fe14fee0327463c7b03d14cbbcb38ce2584d95ee0c112b40b  
Public key: 928744da5ffa614d65dd1d5659a8e9dd558e68f8565946ef3d54215d90cba015  

```

### Compute VRF output and proof​
To compute the VRF output and proof for the input string `Hello, world!`, which is `48656c6c6f2c20776f726c6421` in hexadecimal, with the key pair generated previously, run the following command:
```
$ cargo run --bin ecvrf-cli prove --input 48656c6c6f2c20776f726c6421 --secret-key c0cbc5bf0b2f992fe14fee0327463c7b03d14cbbcb38ce2584d95ee0c112b40b  

```

This should the 80-byte proof and VRF 64-byte output, both in hex format:
```
Proof:  18ccf8bf316f00b387fc6e7b26f2d3ddadbf5e9c66d3a30986f12b208108551f9c6da87793a857d79261338a50430074b1dbc7f8f05e492149c51313381248b4229ebdda367146dbbbf95809c7fb330d  
Output: 2b7e45821d80567761e8bb3fc519efe5ad80cdb4423227289f960319bbcf6eea1aef30c023617d73f589f98272b87563c6669f82b51dafbeb5b9cf3b17c73437  

```

### Verify proof​
You can verify the proof and output in a smart contract using `sui::ecvrf::ecvrf_verify` from the Sui Move framework:
```
module math::ecvrf_test {  
usesui::ecvrf;  
usesui::event;  
  
/// Event on whether the output is verified  
struct VerifiedEventhascopy, drop {  
is_verified: bool,  
    }  
  
publicfunverify_ecvrf_output(output: vector<u8>, alpha_string: vector<u8>, public_key: vector<u8>, proof: vector<u8>) {  
        event::emit(VerifiedEvent {is_verified: ecvrf::ecvrf_verify(&output, &alpha_string, &public_key, &proof)});  
    }  
}  

```

You can also use the CLI tool for verification:
```
$ cargo run --bin ecvrf-cli verify --output 2b7e45821d80567761e8bb3fc519efe5ad80cdb4423227289f960319bbcf6eea1aef30c023617d73f589f98272b87563c6669f82b51dafbeb5b9cf3b17c73437 --proof 18ccf8bf316f00b387fc6e7b26f2d3ddadbf5e9c66d3a30986f12b208108551f9c6da87793a857d79261338a50430074b1dbc7f8f05e492149c51313381248b4229ebdda367146dbbbf95809c7fb330d --input 48656c6c6f2c20776f726c6421 --public-key 928744da5ffa614d65dd1d5659a8e9dd558e68f8565946ef3d54215d90cba015  

```

The preceding command returns the verification:
```
Proof verified correctly!  

```

Previous
Hashing
Next
Multisig Authentication
  * VRF construction
    * Generate keys
    * Compute VRF output and proof
    * Verify proof


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
