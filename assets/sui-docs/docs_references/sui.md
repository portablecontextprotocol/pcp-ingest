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
      * Bridge
      * Std
      * Sui
        * address
        * authenticator_state
        * bag
        * balance
        * bcs
        * bls12381
        * borrow
        * clock
        * coin
        * config
        * deny_list
        * display
        * dynamic_field
        * dynamic_object_field
        * ecdsa_k1
        * ecdsa_r1
        * ecvrf
        * ed25519
        * event
        * groth16
        * group_ops
        * hash
        * hex
        * hmac
        * kiosk
        * kiosk_extension
        * linked_table
        * math
        * nitro_attestation
        * object
        * object_bag
        * object_table
        * package
        * pay
        * poseidon
        * priority_queue
        * prover
        * random
        * sui
        * table
        * table_vec
        * token
        * transfer
        * transfer_policy
        * tx_context
        * types
        * url
        * vdf
        * vec_map
        * vec_set
        * versioned
        * zklogin_verified_id
        * zklogin_verified_issuer
      * Sui_system
    * The Move Book
    * The Move Reference
  * Glossary
  * Contribute


  *   * Move
  * Framework
  * Sui


# Sui
Documentation for the modules in the sui/crates/sui-framework/packages/sui crate. Select a module from the list to see its details.
## ⚙️ address
- Constants
## ⚙️ authenticator_state
- Struct AuthenticatorState
## ⚙️ bag
A bag is a heterogeneous map-like collection. The collection is similar to sui::table in that
## ⚙️ balance
A storable handler for Balances in general. Is used in the Coin
## ⚙️ bcs
This module implements BCS (de)serialization in Move.
## ⚙️ bls12381
Group operations of BLS12-381.
## ⚙️ borrow
A simple library that enables hot-potato-locked borrow mechanics.
## ⚙️ clock
APIs for accessing time from move calls, via the Clock: a unique
## ⚙️ coin
Defines the Coin type - platform wide representation of fungible
## ⚙️ config
- Struct Config
## ⚙️ deny_list
Defines the DenyList type. The DenyList shared object is used to restrict access to
## ⚙️ display
Defines a Display struct which defines the way an Object
## ⚙️ dynamic_field
In addition to the fields declared in its type definition, a Sui object can have dynamic fields
## ⚙️ dynamic_object_field
Similar to sui::dynamic_field, this module allows for the access of dynamic fields. But
## ⚙️ ecdsa_k1
- Constants
## ⚙️ ecdsa_r1
- Constants
## ⚙️ ecvrf
- Constants
## ⚙️ ed25519
- Function ed25519verify
## ⚙️ event
Events module. Defines the sui::emit function which
## ⚙️ groth16
- Struct Curve
## ⚙️ group_ops
Generic Move and native functions for group operations.
## ⚙️ hash
Module which defines hash functions. Note that Sha-256 and Sha3-256 is available in the std::hash module in the
## ⚙️ hex
HEX (Base16) encoding utility.
## ⚙️ hmac
- Function hmacsha3256
## ⚙️ kiosk
Kiosk is a primitive for building safe, decentralized and trustless trading
## ⚙️ kiosk_extension
This module implements the Kiosk Extensions functionality. It allows
## ⚙️ linked_table
Similar to sui::table but the values are linked together, allowing for ordered insertion and
## ⚙️ math
DEPRECATED, use the each integer type's individual module instead, e.g. std::u64
## ⚙️ nitro_attestation
- Struct PCREntry
## ⚙️ object
Sui object identifiers
## ⚙️ object_bag
Similar to sui::bag, an ObjectBag is a heterogeneous map-like collection. But unlike
## ⚙️ object_table
Similar to sui::table, an ObjectTable&lt;K, V&gt; is a map-like collection. But unlike
## ⚙️ package
Functions for operating on Move packages from within Move:
## ⚙️ pay
This module provides handy functionality for wallets and sui::Coin management.
## ⚙️ poseidon
Module which defines instances of the poseidon hash functions. Available in Devnet only.
## ⚙️ priority_queue
Priority queue implemented using a max heap.
## ⚙️ prover
## ⚙️ random
This module provides functionality for generating secure randomness.
## ⚙️ sui
Coin is the token used to pay for gas in Sui.
## ⚙️ table
A table is a map-like collection. But unlike a traditional collection, it's keys and values are
## ⚙️ table_vec
A basic scalable vector library implemented using Table.
## ⚙️ token
The Token module which implements a Closed Loop Token with a configurable
## ⚙️ transfer
- Struct Receiving
## ⚙️ transfer_policy
Defines the TransferPolicy type and the logic to approve TransferRequests.
## ⚙️ tx_context
- Struct TxContext
## ⚙️ types
Sui types helpers and utilities
## ⚙️ url
URL: standard Uniform Resource Locator string
## ⚙️ vdf
- Constants
## ⚙️ vec_map
- Struct VecMap
## ⚙️ vec_set
- Struct VecSet
## ⚙️ versioned
- Struct Versioned
## ⚙️ zklogin_verified_id
- Struct VerifiedID
## ⚙️ zklogin_verified_issuer
- Struct VerifiedIssuer
Previous
vector
Next
address
![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
