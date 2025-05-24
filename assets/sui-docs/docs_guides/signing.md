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
  * Sui On-Chain Signatures Verification in Move


On this page
# Sui On-Chain Signatures Verification in Move
Move contracts in Sui support verifications for several signature schemes on-chain. Not all signatures supported in on-chain verification are supported as user signature verification. See Sui Signatures for valid signature schemes for transaction authorization.
This topic covers:
  1. How to use fastcrypto's CLI tool to create a signature of a given scheme. For testing and debugging only, DO NOT use in production.
  2. Call the Move method on-chain to verification by submitting the signature, the message and the public key.


Signature schemes covered:
  * Ed25519 signature (64 bytes)
  * Secp256k1 non-recoverable signature (64 bytes)
  * Secp256k1 recoverable signature (65 bytes)
  * Secp256r1 non-recoverable signature (64 bytes)
  * Secp256r1 recoverable signature (65 bytes)
  * BLS G1 signature (minSig setting)
  * BLS G2 signature (minPk setting)


## Usage​
### Set up fastcrypto CLI binary​
```
git@github.com:MystenLabs/fastcrypto.git  
cd fastcrypto/  
cargo build --bin sigs-cli  

```

### Sign with CLI and submit to on-chain Move method​
#### Ed25519 signature (64 bytes)​
  1. Generate a key and sign a message.


```
target/debug/sigs-cli keygen --scheme ed25519 --seed 0000000000000000000000000000000000000000000000000000000000000000                  
Private key in hex: $SK  
Public key in hex: $PK  
  
target/debug/sigs-cli sign --scheme ed25519 --msg $MSG --secret-key  $SK  
  
Signature in hex: $SIG  
Public key in hex: $PK  

```

  1. Call the verify method in Move. All inputs are represented in bytes in hex format:


```
usesui::ed25519;  
  
letmsg = x"$MSG";  
letpk = x"$PK";  
letsig = x"$SIG";  
letverify = ed25519::ed25519_verify(&sig, &pk, &msg);  
assert!(verify == true, 0);  

```

#### Secp256k1 non-recoverable signature (64 bytes)​
  1. Generate a key and sign a message.


```
target/debug/sigs-cli keygen --scheme secp256k1 --seed 0000000000000000000000000000000000000000000000000000000000000000                  
Private key in hex: $SK  
Public key in hex: $PK  
  
target/debug/sigs-cli sign --scheme secp256k1 --msg $MSG --secret-key $SK  
  
Signature in hex: $SIG  
Public key in hex: $PK  

```

  1. Call the verify method in Move.


```
usesui::ecdsa_k1;  
  
letmsg = x"$MSG";  
letpk = x"$PK";  
letsig = x"$SIG";  
// The last param 1 represents the hash function used is SHA256, the default hash function used when signing in CLI.  
letverify = ecdsa_k1::secp256k1_verify(&sig, &pk, &msg, 1);  
assert!(verify == true, 0);  

```

#### Secp256k1 recoverable signature (65 bytes)​
  1. Generate a key and sign a message.


```
target/debug/sigs-cli keygen --scheme secp256k1-rec --seed 0000000000000000000000000000000000000000000000000000000000000000                  
Private key in hex: $SK  
Public key in hex: $PK  
  
target/debug/sigs-cli sign --scheme secp256k1-rec --msg $MSG --secret-key $SK  
  
Signature in hex: $SIG  
Public key in hex: $PK  

```

  1. Call the ecrecover method in Move and check equality.


```
usesui::ecdsa_k1;  
  
letmsg = x"$MSG";  
letpk = x"$PK";  
letsig = x"$SIG";  
// The last param 1 represents the hash function used is SHA256, the default hash function used when signing in CLI.  
letrecovered = ecdsa_k1::secp256k1_ecrecover(&sig, &msg, 1);  
assert!(pk == recovered, 0);  

```

#### Secp256r1 non-recoverable signature (64 bytes)​
  1. Generate a key and sign a message.


```
target/debug/sigs-cli keygen --scheme secp256r1 --seed 0000000000000000000000000000000000000000000000000000000000000000                  
Private key in hex: $SK  
Public key in hex: $PK  
  
target/debug/sigs-cli sign --scheme secp256r1 --msg $MSG --secret-key $SK  
  
Signature in hex: $SIG  
Public key in hex: $PK  

```

  1. Call the verify method in Move.


```
usesui::ecdsa_r1;  
  
letmsg = x"$MSG";  
letpk = x"$PK";  
letsig = x"$SIG";  
// The last param 1 represents the hash function used is SHA256, the default hash function used when signing in CLI.  
letverify = ecdsa_r1::secp256r1_verify(&sig, &pk, &msg, 1);  
assert!(verify == true, 0);  

```

#### Secp256r1 recoverable signature (65 bytes)​
  1. Generate a key and sign a message.


```
target/debug/sigs-cli keygen --scheme secp256r1-rec --seed 0000000000000000000000000000000000000000000000000000000000000000                  
Private key in hex: $SK  
Public key in hex: $PK  
  
target/debug/sigs-cli sign --scheme secp256r1-rec --msg $MSG --secret-key $SK  
  
Signature in hex: $SIG  
Public key in hex: $PK  

```

  1. Call the ecrecover method in Move and check equality.


```
usesui::ecdsa_r1;  
  
letmsg = x"$MSG";  
letpk = x"$PK";  
letsig = x"$SIG";  
// The last param 1 represents the hash function used is SHA256, the default hash function used when signing in CLI.  
letrecovered = ecdsa_r1::secp256r1_ecrecover(&sig, &msg, 1);  
assert!(pk == recovered, 0);  

```

#### BLS G1 signature (48 bytes, minSig setting)​
  1. Generate a key and sign a message.


```
target/debug/sigs-cli keygen --scheme bls12381-minsig --seed 0000000000000000000000000000000000000000000000000000000000000000                  
Private key in hex: $SK  
Public key in hex: $PK  
  
target/debug/sigs-cli sign --scheme bls12381-minsig --msg $MSG --secret-key $SK  
  
Signature in hex: $SIG  
Public key in hex: $PK  

```

  1. Call the verify method in Move.


```
usesui::bls12381;  
  
letmsg = x"$MSG";  
letpk = x"$PK";  
letsig = x"$SIG";  
letverified = bls12381::bls12381_min_sig_verify(&sig, &pk, &msg);  
assert!(verified == true, 0);  

```

#### BLS G1 signature (96 bytes, minPk setting)​
  1. Generate a key and sign a message.


```
target/debug/sigs-cli keygen --scheme bls12381-minpk --seed 0000000000000000000000000000000000000000000000000000000000000000                  
Private key in hex: $SK  
Public key in hex: $PK  
  
target/debug/sigs-cli sign --scheme bls12381-minpk --msg $MSG --secret-key $SK  
  
Signature in hex: $SIG  
Public key in hex: $PK  

```

  1. Call the verify method in Move.


```
usesui::bls12381;  
  
letmsg = x"$MSG";  
letpk = x"$PK";  
letsig = x"$SIG";  
letverified = bls12381::bls12381_min_pk_verify(&sig, &pk, &msg);  
assert!(verified == true, 0);  

```

Previous
Cryptography
Next
Groth16
  * Usage
    * Set up fastcrypto CLI binary
    * Sign with CLI and submit to on-chain Move method


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
