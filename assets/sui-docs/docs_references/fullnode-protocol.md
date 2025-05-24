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
    * The Move Book
    * The Move Reference
  * Glossary
  * Contribute


  *   * Sui RPC
  * Sui Full Node gRPC


On this page
# Sui Full Node gRPC
⚙️Early-Stage Feature
This content describes an alpha/beta feature or service. These early stage features and services are in active development, so details are likely to change.
This feature or service is currently available in
  * Devnet
  * Testnet
  * Mainnet


Sui Full node gRPC API will replace the JSON-RPC on Full nodes, such that JSON-RPC will be deprecated when gRPC API is generally available.
Proto filessui/types/types.proto sui/types/signature_scheme.proto sui/node/v2/node_service.proto sui/rpc/v2beta/input.proto sui/rpc/v2beta/execution_status.proto sui/rpc/v2beta/checkpoint_summary.proto sui/rpc/v2beta/effects.proto sui/rpc/v2beta/transaction_execution_service.proto sui/rpc/v2beta/transaction.proto sui/rpc/v2beta/owner.proto sui/rpc/v2beta/object.proto sui/rpc/v2beta/object_reference.proto sui/rpc/v2beta/balance_change.proto sui/rpc/v2beta/epoch.proto sui/rpc/v2beta/ledger_service.proto sui/rpc/v2beta/executed_transaction.proto sui/rpc/v2beta/argument.proto sui/rpc/v2beta/checkpoint.proto sui/rpc/v2beta/gas_cost_summary.proto sui/rpc/v2beta/bcs.proto sui/rpc/v2beta/event.proto sui/rpc/v2beta/checkpoint_contents.proto sui/rpc/v2beta/protocol_config.proto sui/rpc/v2beta/signature_scheme.proto sui/rpc/v2beta/signature.proto sui/rpc/v2alpha/live_data_service.proto sui/rpc/v2alpha/subscription_service.proto google/rpc/status.proto google/rpc/error_details.proto google/protobuf/timestamp.proto google/protobuf/field_mask.proto google/protobuf/duration.proto google/protobuf/any.proto google/protobuf/empty.proto Scalar Value TypesMessagesJump to... ActiveJwk Address AddressDeniedForCoinError Argument AuthenticatorStateExpire AuthenticatorStateUpdate Bcs Bn254FieldElement CancelledTransaction CancelledTransactions ChangeEpoch ChangedObject CheckpointCommitment CheckpointContents V1 CheckpointSummary CheckpointedTransactionInfo CircomG1 CircomG2 Command CommandArgumentError CongestedObjectsError ConsensusCommitPrologue ConsensusDeterminedVersionAssignments Digest EndOfEpochData EndOfEpochTransaction EndOfEpochTransactionKind Event ExecutionStatus FailureStatus GasCostSummary GasPayment GenesisObject GenesisTransaction I128 Identifier Input Jwk JwkId MakeMoveVector MergeCoins ModifiedAtVersion MoveCall MoveError MoveField MoveLocation MoveModule MovePackage MoveStruct MoveStructValue MoveValue MoveVariant MoveVector MultisigAggregatedSignature MultisigCommittee MultisigMember MultisigMemberPublicKey MultisigMemberSignature NestedResult Object ObjectData ObjectExist ObjectId ObjectReference ObjectReferenceWithOwner ObjectWrite Owner PackageIdDoesNotMatch PackageUpgradeError PackageWrite PasskeyAuthenticator ProgrammableTransaction Publish RandomnessStateUpdate ReadOnlyRoot RoaringBitmap SharedObjectInput SimpleSignature SizeError SplitCoins StructTag SystemPackage Transaction TransactionV1 TransactionEffects TransactionEffectsV1 TransactionEffectsV2 TransactionEvents TransactionExpiration TransactionKind TransferObjects TypeArgumentError TypeOrigin TypeTag U128 U256 UnchangedSharedObject Upgrade UpgradeInfo UserSignature ValidatorAggregatedSignature ValidatorCommittee ValidatorCommitteeMember VersionAssignment ZkLoginAuthenticator ZkLoginClaim ZkLoginInputs ZkLoginProof ZkLoginPublicIdentifier
## sui/types/types.proto​
Protobuf definitions of public Sui core types.
This file contains a complete set of protobuf definitions for all of the public sui core types. All sui types are intended to have a 1:1 mapping to a protobuf message defined in this file and be able to roundtrip to/from their rust and protobuf definitions assuming a sufficiently up-to-date version of both these definitions.
For more information on the types these proto messages correspond with, see the documentation for their rust versions defined in the `sui-sdk-types` library.
### Use of `optional`​
These message definitions use protobuf version 3 (proto3). In proto3, fields that are primitives (that is, they are not a `message`) and are not present on the wire are zero-initialized. To gain the ability to detect field presence, these definitions follow the convention of having all fields marked `optional`, and wrapping `repeated` fields in a message as needed.
#### Messages
### ActiveJwk​
A new JWK.
Fields
epoch
uint64
Proto3 optional
Most recent epoch in which the JWK was validated.
id
JwkId
Proto3 optional
Identifier used to uniquely identify a JWK.
jwk
Jwk
Proto3 optional
The JWK.
### Address​
Unique identifier for an account on the Sui blockchain.
An `Address` is a 32-byte pseudonymous identifier used to uniquely identify an account and asset-ownership on the Sui blockchain. Often, human-readable addresses are encoded in hexadecimal with a `0x` prefix. For example, this is a valid Sui address: `0x02a212de6a9dfa3a69e22387acfbafbb1a9e591bd9d636e7895dcfc8de05f331`.
Fields
address
bytes
Proto3 optional
32-byte address.
### AddressDeniedForCoinError​
Address is denied for this coin type.
Fields
address
Address
Proto3 optional
Denied address.
coin_type
string
Proto3 optional
Coin type.
### Argument​
An argument to a programmable transaction command.
Fields
Union field **kind** can be only one of the following.
gas
Empty
The gas coin. The gas coin can only be used by-ref, except for with `TransferObjects`, which can use it by-value.
input
uint32
One of the input objects or primitive values (from `ProgrammableTransaction` inputs).
nested_result
NestedResult
Like a `Result` but it accesses a nested result. Currently, the only usage of this is to access a value from a Move call with multiple return values.
result
uint32
The result of another command (from `ProgrammableTransaction` commands).
### AuthenticatorStateExpire​
Expire old JWKs.
Fields
authenticator_object_initial_shared_version
uint64
Proto3 optional
The initial version of the authenticator object that it was shared at.
min_epoch
uint64
Proto3 optional
Expire JWKs that have a lower epoch than this.
### AuthenticatorStateUpdate​
Update the set of valid JWKs.
Fields
authenticator_object_initial_shared_version
uint64
Proto3 optional
The initial version of the authenticator object that it was shared at.
epoch
uint64
Proto3 optional
Epoch of the authenticator state update transaction.
new_active_jwks
ActiveJwk
Repeated []
Newly active JWKs.
round
uint64
Proto3 optional
Consensus round of the authenticator state update.
### Bcs​
Message that represents a type that is serialized and encoded using the BCS format.
Fields
bcs
bytes
Proto3 optional
Bytes of a BCS encoded value.
### Bn254FieldElement​
A point on the BN254 elliptic curve.
Fields
element
bytes
Proto3 optional
32-byte big-endian field element.
### CancelledTransaction​
A transaction that was cancelled.
Fields
digest
Digest
Proto3 optional
Digest of the cancelled transaction.
version_assignments
VersionAssignment
Repeated []
List of object version assignments.
### CancelledTransactions​
Set of cancelled transactions.
Fields
cancelled_transactions
CancelledTransaction
Repeated []
### ChangeEpoch​
System transaction used to change the epoch.
Fields
computation_charge
uint64
Proto3 optional
The total amount of gas charged for computation during the epoch.
epoch
uint64
Proto3 optional
The next (to become) epoch ID.
epoch_start_timestamp_ms
uint64
Proto3 optional
Unix timestamp when epoch started.
non_refundable_storage_fee
uint64
Proto3 optional
The non-refundable storage fee.
protocol_version
uint64
Proto3 optional
The protocol version in effect in the new epoch.
storage_charge
uint64
Proto3 optional
The total amount of gas charged for storage during the epoch.
storage_rebate
uint64
Proto3 optional
The amount of storage rebate refunded to the txn senders.
system_packages
SystemPackage
Repeated []
System packages (specifically framework and Move stdlib) that are written before the new epoch starts. This tracks framework upgrades on chain. When executing the `ChangeEpoch` txn, the validator must write out the following modules. Modules are provided with the version they will be upgraded to, their modules in serialized form (which include their package ID), and a list of their transitive dependencies.
### ChangedObject​
Input/output state of an object that was changed during execution.
Fields
object_id
ObjectId
Proto3 optional
ID of the object.
Union field **input_state** can be only one of the following.
exist
ObjectExist
Object existed prior to this transaction.
not_exist
Empty
Object did not exist prior to this transaction.
Union field **output_state** can be only one of the following.
object_write
ObjectWrite
Object was written, including all of mutated, created, unwrapped.
package_write
PackageWrite
Package was written.
removed
Empty
Object was removed from the store due to this transaction.
Union field **id_operation** can be only one of the following.
created
Empty
deleted
Empty
none
Empty
### CheckpointCommitment​
A commitment made by a checkpoint.
Fields
Union field **commitment** can be only one of the following.
ecmh_live_object_set
Digest
An elliptic curve multiset hash attesting to the set of objects that comprise the live state of the Sui blockchain.
### CheckpointContents​
The committed to contents of a checkpoint.
Fields
Union field **contents** can be only one of the following.
v1
V1
### V1​
Version 1 of `CheckpointContents`.
Fields
transactions
CheckpointedTransactionInfo
Repeated []
### CheckpointSummary​
A header for a checkpoint on the Sui blockchain.
On the Sui network, checkpoints define the history of the blockchain. They are quite similar to the concept of blocks used by other blockchains like Bitcoin or Ethereum. The Sui blockchain, however, forms checkpoints after transaction execution has already happened to provide a certified history of the chain, instead of being formed before execution.
Checkpoints commit to a variety of state, including but not limited to:
  * The hash of the previous checkpoint.
  * The set of transaction digests, their corresponding effects digests, as well as the set of user signatures that authorized its execution.
  * The objects produced by a transaction.
  * The set of live objects that make up the current state of the chain.
  * On epoch transitions, the next validator committee.


`CheckpointSummary`s themselves don't directly include all of the previous information but they are the top-level type by which all the information is committed to transitively via cryptographic hashes included in the summary. `CheckpointSummary`s are signed and certified by a quorum of the validator committee in a given epoch to allow verification of the chain's state.
Fields
commitments
CheckpointCommitment
Repeated []
Commitments to checkpoint-specific state.
content_digest
Digest
Proto3 optional
The hash of the `CheckpointContents` for this checkpoint.
end_of_epoch_data
EndOfEpochData
Proto3 optional
Extra data only present in the final checkpoint of an epoch.
epoch
uint64
Proto3 optional
Epoch that this checkpoint belongs to.
epoch_rolling_gas_cost_summary
GasCostSummary
Proto3 optional
The running total gas costs of all transactions included in the current epoch so far until this checkpoint.
previous_digest
Digest
Proto3 optional
The hash of the previous `CheckpointSummary`. This will be `None` only for the first, or genesis, checkpoint.
sequence_number
uint64
Proto3 optional
The height of this checkpoint.
timestamp_ms
uint64
Proto3 optional
Timestamp of the checkpoint - number of milliseconds from the Unix epoch Checkpoint timestamps are monotonic, but not strongly monotonic - subsequent checkpoints can have the same timestamp if they originate from the same underlining consensus commit.
total_network_transactions
uint64
Proto3 optional
Total number of transactions committed since genesis, including those in this checkpoint.
version_specific_data
bytes
Proto3 optional
`CheckpointSummary` is not an evolvable structure - it must be readable by any version of the code. Therefore, to allow extensions to be added to `CheckpointSummary`, opaque data can be added to checkpoints, which can be deserialized based on the current protocol version.
### CheckpointedTransactionInfo​
Transaction information committed to in a checkpoint.
Fields
effects
Digest
Proto3 optional
Digest of the effects.
signatures
UserSignature
Repeated []
Set of user signatures that authorized the transaction.
transaction
Digest
Proto3 optional
Digest of the transaction.
### CircomG1​
A G1 point.
Fields
e0
Bn254FieldElement
Proto3 optional
e1
Bn254FieldElement
Proto3 optional
e2
Bn254FieldElement
Proto3 optional
### CircomG2​
A G2 point.
Fields
e00
Bn254FieldElement
Proto3 optional
e01
Bn254FieldElement
Proto3 optional
e10
Bn254FieldElement
Proto3 optional
e11
Bn254FieldElement
Proto3 optional
e20
Bn254FieldElement
Proto3 optional
e21
Bn254FieldElement
Proto3 optional
### Command​
A single command in a programmable transaction.
Fields
Union field **command** can be only one of the following.
make_move_vector
MakeMoveVector
`forall T: Vec<T> -> vector<T>` Given n-values of the same type, it constructs a vector. For non-objects or an empty vector, the type tag must be specified.
merge_coins
MergeCoins
`(&mut Coin<T>, Vec<Coin<T>>)` It merges n-coins into the first coin.
move_call
MoveCall
A call to either an entry or a public Move function.
publish
Publish
Publishes a Move package. It takes the package bytes and a list of the package's transitive dependencies to link against on chain.
split_coins
SplitCoins
`(&mut Coin<T>, Vec<u64>)` -> `Vec<Coin<T>>` It splits off some amounts into new coins with those amounts.
transfer_objects
TransferObjects
`(Vec<forall T:key+store. T>, address)` It sends n-objects to the specified address. These objects must have store (public transfer) and either the previous owner must be an address or the object must be newly created.
upgrade
Upgrade
Upgrades a Move package. Takes (in order): 1. A vector of serialized modules for the package. 2. A vector of object ids for the transitive dependencies of the new package. 3. The object ID of the package being upgraded. 4. An argument holding the `UpgradeTicket` that must have been produced from an earlier command in the same programmable transaction.
### CommandArgumentError​
An error with an argument to a command.
Fields
argument
uint32
Proto3 optional
Position of the problematic argument.
Union field **kind** can be only one of the following.
index_out_of_bounds
uint32
Out of bounds access to input or results.
invalid_argument_to_private_entry_function
Empty
Invalid argument to private entry function. Private entry functions cannot take arguments from other Move functions.
invalid_bcs_bytes
Empty
The argument cannot be deserialized into a value of the specified type.
invalid_gas_coin_usage
Empty
Invalid usage of gas coin. The gas coin can only be used by-value with a `TransferObject` command.
invalid_object_by_mut_ref
Empty
Immutable objects cannot be passed by mutable reference, `&mut`.
invalid_object_by_value
Empty
Immutable objects cannot be passed by-value.
invalid_result_arity
uint32
Invalid usage of result. Expected a single result but found either no return value or multiple.
invalid_usage_of_pure_argument
Empty
The argument cannot be instantiated from raw bytes.
invalid_value_usage
Empty
Invalid usage of Move value. - Mutably borrowed values require unique usage. - Immutably borrowed values cannot be taken or borrowed mutably. - Taken values cannot be used again.
secondary_index_out_of_bounds
NestedResult
Out of bounds access to subresult.
shared_object_operation_not_allowed
Empty
Shared object operations such as wrapping, freezing, or converting to owned are not allowed.
type_mismatch
Empty
The type of the value does not match the expected type.
### CongestedObjectsError​
Set of objects that were congested, leading to the transaction's cancellation.
Fields
congested_objects
ObjectId
Repeated []
Set of congested objects.
### ConsensusCommitPrologue​
Consensus commit prologue system transaction.
This message can represent V1, V2, and V3 prologue types.
Fields
additional_state_digest
Digest
Proto3 optional
Digest of any additional state computed by the consensus handler. Used to detect forking bugs as early as possible. Present in V4.
commit_timestamp_ms
uint64
Proto3 optional
Unix timestamp from consensus. Present in V1, V2, V3, V4.
consensus_commit_digest
Digest
Proto3 optional
Digest of consensus output. Present in V2, V3, V4.
consensus_determined_version_assignments
ConsensusDeterminedVersionAssignments
Proto3 optional
Stores consensus handler determined shared object version assignments. Present in V3, V4.
epoch
uint64
Proto3 optional
Epoch of the commit prologue transaction. Present in V1, V2, V3, V4.
round
uint64
Proto3 optional
Consensus round of the commit. Present in V1, V2, V3, V4.
sub_dag_index
uint64
Proto3 optional
The sub DAG index of the consensus commit. This field is populated if there are multiple consensus commits per round. Present in V3, V4.
### ConsensusDeterminedVersionAssignments​
Version assignments performed by consensus.
Fields
Union field **kind** can be only one of the following.
cancelled_transactions
CancelledTransactions
Cancelled transaction version assignment.
### Digest​
32-byte output of hashing a Sui structure using the Blake2b256 hash function.
Fields
digest
bytes
Proto3 optional
32-byte hash.
### EndOfEpochData​
Data, which when included in a `CheckpointSummary`, signals the end of an `Epoch`.
Fields
epoch_commitments
CheckpointCommitment
Repeated []
Commitments to epoch specific state (live object set)
next_epoch_committee
ValidatorCommitteeMember
Repeated []
The set of validators that will be in the `ValidatorCommittee` for the next epoch.
next_epoch_protocol_version
uint64
Proto3 optional
The protocol version that is in effect during the next epoch.
### EndOfEpochTransaction​
Set of operations run at the end of the epoch to close out the current epoch and start the next one.
Fields
transactions
EndOfEpochTransactionKind
Repeated []
### EndOfEpochTransactionKind​
Operation run at the end of an epoch.
Fields
Union field **kind** can be only one of the following.
authenticator_state_create
Empty
Create and initialize the authenticator object used for zklogin.
authenticator_state_expire
AuthenticatorStateExpire
Expire JWKs used for zklogin.
bridge_committee_init
uint64
Initialize the bridge committee.
bridge_state_create
Digest
Create and initialize the bridge object.
change_epoch
ChangeEpoch
End the epoch and start the next one.
deny_list_state_create
Empty
Create and initialize the deny list object.
randomness_state_create
Empty
Create and initialize the randomness object.
### Event​
An event.
Fields
contents
bytes
Proto3 optional
BCS serialized bytes of the event.
event_type
StructTag
Proto3 optional
The type of the event emitted.
module
Identifier
Proto3 optional
Module name of the top-level function invoked by a `MoveCall` command that triggered this event to be emitted.
package_id
ObjectId
Proto3 optional
Package ID of the top-level function invoked by a `MoveCall` command that triggered this event to be emitted.
sender
Address
Proto3 optional
Address of the account that sent the transaction where this event was emitted.
### ExecutionStatus​
The status of an executed transaction.
Fields
status
FailureStatus
Proto3 optional
The error if `success` is false.
success
bool
Proto3 optional
Indicates if the transaction was successful or not.
### FailureStatus​
An error that can occur during the execution of a transaction.
Fields
command
uint64
Proto3 optional
The command, if any, during which the error occurred.
Union field **execution_error** can be only one of the following.
address_denied_for_coin
AddressDeniedForCoinError
Address is denied for this coin type.
arity_mismatch
Empty
Parity mismatch for Move function. The number of arguments does not match the number of parameters.
certificate_denied
Empty
Certificate is on the deny list.
circular_object_ownership
ObjectId
Circular object ownership.
coin_balance_overflow
Empty
Coin balance overflowed an u64.
coin_type_global_pause
string
Coin type is globally paused for use.
command_argument_error
CommandArgumentError
Invalid command argument.
effects_too_large
SizeError
Post-execution errors. Effects from the transaction are too large.
execution_cancelled_due_to_randomness_unavailable
Empty
Certificate is cancelled because randomness could not be generated this epoch.
execution_cancelled_due_to_shared_object_congestion
CongestedObjectsError
Certificate is cancelled due to congestion on shared objects.
feature_not_yet_supported
Empty
Attempted to use feature that is not supported yet.
function_not_found
Empty
Programmable transaction errors. Function not found.
input_object_deleted
Empty
Requested shared object has been deleted.
insufficient_coin_balance
Empty
Coin errors. Insufficient coin balance for requested operation.
insufficient_gas
Empty
Insufficient gas.
invalid_gas_object
Empty
Invalid `Gas` object.
invalid_public_function_return_type
uint32
Invalid public Move function signature. Unsupported return type for return value.
invalid_transfer_object
Empty
Invalid transfer object, object does not have public transfer.
invariant_violation
Empty
Invariant violation.
move_abort
MoveError
Move runtime abort.
move_primitive_runtime_error
MoveError
MoveVm errors. Error from a non-abort instruction. Possible causes: Arithmetic error, stack overflow, max value depth, or similar.
non_entry_function_invoked
Empty
Non-entry function invoked. Move Call must start with an entry function.
object_too_big
SizeError
Move object is larger than the maximum allowed size.
package_too_big
SizeError
Package is larger than the maximum allowed size.
package_upgrade_error
PackageUpgradeError
Invalid package upgrade.
publish_error_non_zero_address
Empty
Publish/Upgrade errors. Publish error, non-zero address. The modules in the package must have their self-addresses set to zero.
publish_upgrade_dependency_downgrade
Empty
Publish or upgrade dependency downgrade. Indirect (transitive) dependency of published or upgraded package has been assigned an on-chain version that is less than the version required by one of the package's transitive dependencies.
publish_upgrade_missing_dependency
Empty
Publish or Upgrade is missing dependency.
shared_object_operation_not_allowed
Empty
The requested shared object operation is not allowed.
sui_move_verification_error
Empty
Sui Move bytecode verification error.
sui_move_verification_timedout
Empty
Sui Move bytecode verification timed out.
type_argument_error
TypeArgumentError
Type argument error.
type_arity_mismatch
Empty
Type parity mismatch for Move function. Mismatch between the number of actual versus expected type arguments.
unused_value_without_drop
NestedResult
Unused result without the drop ability.
vm_invariant_violation
Empty
MoveVm invariant violation.
vm_verification_or_deserialization_error
Empty
Bytecode verification error.
written_objects_too_large
SizeError
Indicates the transaction tried to write objects too large to storage.
### GasCostSummary​
Summary of gas charges.
Storage is charged independently of computation. There are three parts to the storage charges:
  * `storage_cost`: the charge of storage at the time the transaction is executed. The cost of storage is the number of bytes of the objects being mutated multiplied by a variable storage cost per byte.
  * `storage_rebate`: the amount a user gets back when manipulating an object. The `storage_rebate` is the `storage_cost` for an object minus fees.
  * `non_refundable_storage_fee`: not all the value of the object storage cost is given back to user and there is a small fraction that is kept by the system. This value tracks that charge.


When looking at a gas cost summary the amount charged to the user is `computation_cost + storage_cost - storage_rebate` and that is the amount that is deducted from the gas coins. `non_refundable_storage_fee` is collected from the objects being mutated/deleted and it is tracked by the system in storage funds.
Objects deleted, including the older versions of objects mutated, have the storage field on the objects added up to a pool of "potential rebate". This rebate then is reduced by the "nonrefundable rate" such that: `potential_rebate(storage cost of deleted/mutated objects) = storage_rebate + non_refundable_storage_fee`
Fields
computation_cost
uint64
Proto3 optional
Cost of computation/execution.
non_refundable_storage_fee
uint64
Proto3 optional
The fee for the rebate. The portion of the storage rebate kept by the system.
storage_cost
uint64
Proto3 optional
Storage cost, it's the sum of all storage cost for all objects created or mutated.
storage_rebate
uint64
Proto3 optional
The amount of storage cost refunded to the user for all objects deleted or mutated in the transaction.
### GasPayment​
Payment information for executing a transaction.
Fields
budget
uint64
Proto3 optional
Total budget willing to spend for the execution of a transaction.
objects
ObjectReference
Repeated []
Set of gas objects to use for payment.
owner
Address
Proto3 optional
Owner of the gas objects, either the transaction sender or a sponsor.
price
uint64
Proto3 optional
Gas unit price to use when charging for computation. Must be greater than or equal to the network's current RGP (reference gas price).
### GenesisObject​
An object part of the initial chain state.
Fields
object
ObjectData
Proto3 optional
object_id
ObjectId
Proto3 optional
owner
Owner
Proto3 optional
version
uint64
Proto3 optional
### GenesisTransaction​
The genesis transaction.
Fields
objects
GenesisObject
Repeated []
Set of genesis objects.
### I128​
A signed 128-bit integer encoded in little-endian using 16-bytes.
Fields
bytes
bytes
Proto3 optional
16-byte little-endian bytes.
### Identifier​
A Move identifier.
Identifiers are only valid if they conform to the following ABNF:
```
identifier = (ALPHA *127(ALPHA / DIGIT / UNDERSCORE)) /  
             (UNDERSCORE 1*127(ALPHA / DIGIT / UNDERSCORE))  
UNDERSCORE = %x95  

```

Fields
identifier
string
Proto3 optional
### Input​
An input to a user transaction.
Fields
Union field **kind** can be only one of the following.
immutable_or_owned
ObjectReference
A Move object that is either immutable or address owned.
pure
bytes
A move value serialized as BCS. For normal operations this is required to be a move primitive type and not contain structs or objects.
receiving
ObjectReference
A Move object that is attempted to be received in this transaction.
shared
SharedObjectInput
A Move object whose owner is "Shared".
### Jwk​
A JSON web key.
Struct that contains info for a JWK. A list of them for different kinds can be retrieved from the JWK endpoint (for example, &#lt;https://www.googleapis.com/oauth2/v3/certs>). The JWK is used to verify the JWT token.
Fields
alg
string
Proto3 optional
Algorithm parameter, https://datatracker.ietf.org/doc/html/rfc7517#section-4.4.
e
string
Proto3 optional
RSA public exponent, https://datatracker.ietf.org/doc/html/rfc7517#section-9.3.
kty
string
Proto3 optional
Key type parameter, https://datatracker.ietf.org/doc/html/rfc7517#section-4.1.
n
string
Proto3 optional
RSA modulus, https://datatracker.ietf.org/doc/html/rfc7517#section-9.3.
### JwkId​
Key to uniquely identify a JWK.
Fields
iss
string
Proto3 optional
The issuer or identity of the OIDC provider.
kid
string
Proto3 optional
A key ID used to uniquely identify a key from an OIDC provider.
### MakeMoveVector​
Command to build a Move vector out of a set of individual elements.
Fields
element_type
TypeTag
Proto3 optional
Type of the individual elements. This is required to be set when the type can't be inferred, for example when the set of provided arguments are all pure input values.
elements
Argument
Repeated []
The set individual elements to build the vector with.
### MergeCoins​
Command to merge multiple coins of the same type into a single coin.
Fields
coin
Argument
Proto3 optional
Coin to merge coins into.
coins_to_merge
Argument
Repeated []
Set of coins to merge into `coin`. All listed coins must be of the same type and be the same type as `coin`
### ModifiedAtVersion​
Indicates that an object was modified at a specific version.
Fields
object_id
ObjectId
Proto3 optional
`ObjectId` of the object.
version
uint64
Proto3 optional
Version of the object prior to this transaction.
### MoveCall​
Command to call a Move function.
Functions that can be called by a `MoveCall` command are those that have a function signature that is either `entry` or `public` (which don't have a reference return type).
Fields
arguments
Argument
Repeated []
The arguments to the function.
function
Identifier
Proto3 optional
The function to be called.
module
Identifier
Proto3 optional
The specific module in the package containing the function.
package
ObjectId
Proto3 optional
The package containing the module and function.
type_arguments
TypeTag
Repeated []
The type arguments to the function.
### MoveError​
Error that occurred in Move.
Fields
abort_code
uint64
Proto3 optional
Abort code from Move.
location
MoveLocation
Proto3 optional
Location in Move where the error occurred.
### MoveField​
Fields
name
Identifier
Proto3 optional
value
MoveValue
Proto3 optional
### MoveLocation​
Location in Move bytecode where an error occurred.s
Fields
function
uint32
Proto3 optional
The function index.
function_name
Identifier
Proto3 optional
The name of the function, if available.
instruction
uint32
Proto3 optional
Offset of the instruction where the error occurred.
module
Identifier
Proto3 optional
The module name.
package
ObjectId
Proto3 optional
The package ID.
### MoveModule​
Module defined by a package.
Fields
contents
bytes
Proto3 optional
Serialized bytecode of the module.
name
Identifier
Proto3 optional
Name of the module.
### MovePackage​
A Move package.
Fields
id
ObjectId
Proto3 optional
Address or ID of this package.
linkage_table
UpgradeInfo
Repeated []
For each dependency, maps original package ID to the info about the (upgraded) dependency version that this package is using.
modules
MoveModule
Repeated []
Set of modules defined by this package.
type_origin_table
TypeOrigin
Repeated []
Maps struct/module to a package version where it was first defined, stored as a vector for simple serialization and deserialization.
version
uint64
Proto3 optional
Version of the package.
### MoveStruct​
A Move struct.
Fields
contents
bytes
Proto3 optional
BCS bytes of a Move struct value.
has_public_transfer
bool
Proto3 optional
DEPRECATED this field is no longer used to determine whether a tx can transfer this object. Instead, it is always calculated from the objects type when loaded in execution.
object_id
ObjectId
Proto3 optional
`ObjectId` for this object.
object_type
StructTag
Proto3 optional
The type of this object.
version
uint64
Proto3 optional
Version of the object.
### MoveStructValue​
Fields
fields
MoveField
Repeated []
struct_type
StructTag
Proto3 optional
### MoveValue​
Fields
Union field **kind** can be only one of the following.
address
Address
bool
bool
signer
Address
struct
MoveStructValue
u128
U128
u16
uint32
u256
U256
u32
uint32
u64
uint64
u8
uint32
variant
MoveVariant
vector
MoveVector
### MoveVariant​
Fields
enum_type
StructTag
Proto3 optional
fields
MoveField
Repeated []
tag
uint32
Proto3 optional
variant_name
Identifier
Proto3 optional
### MoveVector​
Fields
values
MoveValue
Repeated []
### MultisigAggregatedSignature​
Aggregated signature from members of a multisig committee.
Fields
bitmap
uint32
Proto3 optional
Bitmap indicating which committee members contributed to the signature.
committee
MultisigCommittee
Proto3 optional
The committee to use to validate this signature.
legacy_bitmap
RoaringBitmap
Proto3 optional
If present, means this signature's on-chain format uses the old legacy multisig format.
signatures
MultisigMemberSignature
Repeated []
The plain signatures encoded with signature scheme. The signatures must be in the same order as they are listed in the committee.
### MultisigCommittee​
A multisig committee.
Fields
members
MultisigMember
Repeated []
A list of committee members and their corresponding weight.
threshold
uint32
Proto3 optional
The threshold of signatures needed to validate a signature from this committee.
### MultisigMember​
A member in a multisig committee.
Fields
public_key
MultisigMemberPublicKey
Proto3 optional
The public key of the committee member.
weight
uint32
Proto3 optional
The weight of this member's signature.
### MultisigMemberPublicKey​
Set of valid public keys for multisig committee members.
Fields
Union field **scheme** can be only one of the following.
ed25519
bytes
An ed25519 public key
secp256k1
bytes
A secp256k1 public key
secp256r1
bytes
A secp256r1 public key
zklogin
ZkLoginPublicIdentifier
A zklogin public identifier
### MultisigMemberSignature​
A signature from a member of a multisig committee.
Fields
Union field **signature** can be only one of the following.
ed25519
bytes
An ed25519 signature.
secp256k1
bytes
A secp256k1 signature.
secp256r1
bytes
A secp256r1 signature.
zklogin
ZkLoginAuthenticator
A zklogin signature.
### NestedResult​
An argument type for a nested result.
Fields
result
uint32
Proto3 optional
The command index.
subresult
uint32
Proto3 optional
The index into the command's output.
### Object​
An object on the Sui blockchain.
Fields
object
ObjectData
Proto3 optional
object_id
ObjectId
Proto3 optional
`ObjectId` for this object.
owner
Owner
Proto3 optional
Owner of the object.
previous_transaction
Digest
Proto3 optional
The digest of the transaction that created or last mutated this object
storage_rebate
uint64
Proto3 optional
The amount of SUI to rebate if this object gets deleted. This number is re-calculated each time the object is mutated based on the present storage gas price.
version
uint64
Proto3 optional
Version of the object.
### ObjectData​
Object data, either a package or struct.
Fields
Union field **kind** can be only one of the following.
package
MovePackage
struct
MoveStruct
### ObjectExist​
Information about the old version of the object.
Fields
digest
Digest
Proto3 optional
Digest of the object.
owner
Owner
Proto3 optional
Owner of the object.
version
uint64
Proto3 optional
Version of the object.
### ObjectId​
Unique identifier for an object on the Sui blockchain.
An `ObjectId` is a 32-byte identifier used to uniquely identify an object on the Sui blockchain.
Fields
object_id
bytes
Proto3 optional
32-byte object-id.
### ObjectReference​
Reference to an object.
Fields
digest
Digest
Proto3 optional
The digest of this object.
object_id
ObjectId
Proto3 optional
The object ID of this object.
version
uint64
Proto3 optional
The version of this object.
### ObjectReferenceWithOwner​
An object reference with owner information.
Fields
owner
Owner
Proto3 optional
`Owner`.
reference
ObjectReference
Proto3 optional
`ObjectReference`.
### ObjectWrite​
Object write, including all of mutated, created, unwrapped.
Fields
digest
Digest
Proto3 optional
Digest of the new version of the object.
owner
Owner
Proto3 optional
Owner of the new version of the object.
### Owner​
Enum of different types of ownership for an object.
Fields
Union field **kind** can be only one of the following.
address
Address
Object is exclusively owned by a single address, and is mutable.
immutable
Empty
Object is immutable, and hence ownership doesn't matter.
object
ObjectId
Object is exclusively owned by a single object, and is mutable.
shared
uint64
Object is shared, can be used by any address, and is mutable.
### PackageIdDoesNotMatch​
Package ID does not match `PackageId` in upgrade ticket.
Fields
package_id
ObjectId
Proto3 optional
The package ID.
ticket_id
ObjectId
Proto3 optional
The ticket ID.
### PackageUpgradeError​
An error with a upgrading a package.
Fields
Union field **kind** can be only one of the following.
digets_does_not_match
Digest
Digest in upgrade ticket and computed digest differ.
incompatible_upgrade
Empty
Package upgrade is incompatible with previous version.
not_a_package
ObjectId
Object is not a package.
package_id_does_not_match
PackageIdDoesNotMatch
Package ID does not match `PackageId` in upgrade ticket.
unable_to_fetch_package
ObjectId
Unable to fetch package.
unknown_upgrade_policy
uint32
Upgrade policy is not valid.
### PackageWrite​
Package write.
Fields
digest
Digest
Proto3 optional
Digest of the new package.
version
uint64
Proto3 optional
Version of the new package.
### PasskeyAuthenticator​
A passkey authenticator.
See struct.PasskeyAuthenticator for more information on the requirements on the shape of the `client_data_json` field.
Fields
authenticator_data
bytes
Proto3 optional
Opaque authenticator data for this passkey signature. See Authenticator Data for more information on this field.
client_data_json
string
Proto3 optional
Structured, unparsed, JSON for this passkey signature. See CollectedClientData for more information on this field.
signature
SimpleSignature
Proto3 optional
A secp256r1 signature.
### ProgrammableTransaction​
A user transaction.
Contains a series of native commands and Move calls where the results of one command can be used in future commands.
Fields
commands
Command
Repeated []
The commands to be executed sequentially. A failure in any command results in the failure of the entire transaction.
inputs
Input
Repeated []
Input objects or primitive values.
### Publish​
Command to publish a new Move package.
Fields
dependencies
ObjectId
Repeated []
Set of packages that the to-be published package depends on.
modules
bytes
Repeated []
The serialized Move modules.
### RandomnessStateUpdate​
Randomness update.
Fields
epoch
uint64
Proto3 optional
Epoch of the randomness state update transaction.
random_bytes
bytes
Proto3 optional
Updated random bytes.
randomness_object_initial_shared_version
uint64
Proto3 optional
The initial version of the randomness object that it was shared at.
randomness_round
uint64
Proto3 optional
Randomness round of the update.
### ReadOnlyRoot​
Read-only shared object from the input.
Fields
digest
Digest
Proto3 optional
Digest of the shared object.
version
uint64
Proto3 optional
Version of the shared object.
### RoaringBitmap​
A RoaringBitmap. See RoaringFormatSpec for the specification for the serialized format of `RoaringBitmap`s.
Fields
bitmap
bytes
Proto3 optional
Serialized `RoaringBitmap`.
### SharedObjectInput​
A shared object input.
Fields
initial_shared_version
uint64
Proto3 optional
Initial version of the object when it was shared.
mutable
bool
Proto3 optional
Controls whether the caller asks for a mutable reference to the shared object.
object_id
ObjectId
Proto3 optional
`ObjectId` of the shared object.
### SimpleSignature​
A basic signature.
Can either be an ed25519, secp256k1, or secp256r1 signature with corresponding public key.
Fields
public_key
bytes
Proto3 optional
Public key bytes.
scheme
int32
Proto3 optional
The signature scheme of the signautre and public key, which should be an enum value of [sui.types.SignatureScheme][sui.types.SignatureScheme]
signature
bytes
Proto3 optional
Signature bytes.
### SizeError​
A size error.
Fields
max_size
uint64
Proto3 optional
The maximum allowable size.
size
uint64
Proto3 optional
The offending size.
### SplitCoins​
Command to split a single coin object into multiple coins.
Fields
amounts
Argument
Repeated []
The amounts to split off.
coin
Argument
Proto3 optional
The coin to split.
### StructTag​
Type information for a Move struct.
Fields
address
Address
Proto3 optional
Address of the package where this type was defined.
module
Identifier
Proto3 optional
Name of the module where this type was defined.
name
Identifier
Proto3 optional
Name of the type itself.
type_parameters
TypeTag
Repeated []
List of type parameters, if any.
### SystemPackage​
System package.
Fields
dependencies
ObjectId
Repeated []
Package dependencies.
modules
bytes
Repeated []
Move modules.
version
uint64
Proto3 optional
Version of the package.
### Transaction​
A transaction.
Fields
Union field **version** can be only one of the following.
v1
TransactionV1
### TransactionV1​
Version 1 of `Transaction`.
Fields
expiration
TransactionExpiration
Proto3 optional
gas_payment
GasPayment
Proto3 optional
kind
TransactionKind
Proto3 optional
sender
Address
Proto3 optional
### TransactionEffects​
The output or effects of executing a transaction.
Fields
Union field **version** can be only one of the following.
v1
TransactionEffectsV1
v2
TransactionEffectsV2
### TransactionEffectsV1​
Version 1 of `TransactionEffects`.
Fields
created
ObjectReferenceWithOwner
Repeated []
`ObjectReference` and owner of new objects created.
deleted
ObjectReference
Repeated []
Object refs of objects now deleted (the new refs).
dependencies
Digest
Repeated []
The set of transaction digests this transaction depends on.
epoch
uint64
Proto3 optional
The epoch when this transaction was executed.
events_digest
Digest
Proto3 optional
The digest of the events emitted during execution, can be `None` if the transaction does not emit any event.
gas_object
ObjectReferenceWithOwner
Proto3 optional
The updated gas object reference. Have a dedicated field for convenient access. It's also included in mutated.
gas_used
GasCostSummary
Proto3 optional
The gas used by this transaction.
modified_at_versions
ModifiedAtVersion
Repeated []
The version that every modified (mutated or deleted) object had before it was modified by this transaction.
mutated
ObjectReferenceWithOwner
Repeated []
`ObjectReference` and owner of mutated objects, including gas object.
shared_objects
ObjectReference
Repeated []
The object references of the shared objects used in this transaction. Empty if no shared objects were used.
status
ExecutionStatus
Proto3 optional
The status of the execution.
transaction_digest
Digest
Proto3 optional
The transaction digest.
unwrapped
ObjectReferenceWithOwner
Repeated []
`ObjectReference` and owner of objects that are unwrapped in this transaction. Unwrapped objects are objects that were wrapped into other objects in the past, and just got extracted out.
unwrapped_then_deleted
ObjectReference
Repeated []
Object refs of objects previously wrapped in other objects but now deleted.
wrapped
ObjectReference
Repeated []
Object refs of objects now wrapped in other objects.
### TransactionEffectsV2​
Version 2 of `TransactionEffects`.
Fields
auxiliary_data_digest
Digest
Proto3 optional
Auxiliary data that are not protocol-critical, generated as part of the effects but are stored separately. Storing it separately allows us to avoid bloating the effects with data that are not critical. It also provides more flexibility on the format and type of the data.
changed_objects
ChangedObject
Repeated []
Objects whose state are changed in the object store.
dependencies
Digest
Repeated []
The set of transaction digests this transaction depends on.
epoch
uint64
Proto3 optional
The epoch when this transaction was executed.
events_digest
Digest
Proto3 optional
The digest of the events emitted during execution, can be `None` if the transaction does not emit any event.
gas_object_index
uint32
Proto3 optional
The updated gas object reference, as an index into the `changed_objects` vector. Having a dedicated field for convenient access. System transaction that don't require gas will leave this as `None`.
gas_used
GasCostSummary
Proto3 optional
The gas used by this transaction.
lamport_version
uint64
Proto3 optional
The version number of all the written Move objects by this transaction.
status
ExecutionStatus
Proto3 optional
The status of the execution.
transaction_digest
Digest
Proto3 optional
The transaction digest.
unchanged_shared_objects
UnchangedSharedObject
Repeated []
Shared objects that are not mutated in this transaction. Unlike owned objects, read-only shared objects' version are not committed in the transaction, and in order for a node to catch up and execute it without consensus sequencing, the version needs to be committed in the effects.
### TransactionEvents​
Events emitted during the successful execution of a transaction.
Fields
events
Event
Repeated []
### TransactionExpiration​
A TTL for a transaction.
Fields
Union field **expiration** can be only one of the following.
epoch
uint64
Validators won't sign and execute transaction unless the expiration epoch is greater than or equal to the current epoch.
none
Empty
The transaction has no expiration.
### TransactionKind​
Transaction type.
Fields
Union field **kind** can be only one of the following.
authenticator_state_update
AuthenticatorStateUpdate
Update set of valid JWKs used for zklogin.
change_epoch
ChangeEpoch
System transaction used to end an epoch. The `ChangeEpoch` variant is now deprecated (but the `ChangeEpoch` struct is still used by `EndOfEpochTransaction`).
consensus_commit_prologue_v1
ConsensusCommitPrologue
V1 consensus commit update.
consensus_commit_prologue_v2
ConsensusCommitPrologue
V2 consensus commit update.
consensus_commit_prologue_v3
ConsensusCommitPrologue
V3 consensus commit update.
consensus_commit_prologue_v4
ConsensusCommitPrologue
V4 consensus commit update.
end_of_epoch
EndOfEpochTransaction
Set of operations to run at the end of the epoch to close out the current epoch and start the next one.
genesis
GenesisTransaction
Transaction used to initialize the chain state. Only valid if in the genesis checkpoint (0) and if this is the very first transaction ever executed on the chain.
programmable_transaction
ProgrammableTransaction
A user transaction comprised of a list of native commands and Move calls.
randomness_state_update
RandomnessStateUpdate
Randomness update.
### TransferObjects​
Command to transfer ownership of a set of objects to an address.
Fields
address
Argument
Proto3 optional
The address to transfer ownership to.
objects
Argument
Repeated []
Set of objects to transfer.
### TypeArgumentError​
Type argument error.
Fields
type_argument
uint32
Proto3 optional
Index of the problematic type argument.
Union field **kind** can be only one of the following.
constraint_not_satisfied
Empty
A type provided did not match the specified constraint.
type_not_found
Empty
A type was not found in the module specified.
### TypeOrigin​
Identifies a struct and the module it was defined in.
Fields
module_name
Identifier
Proto3 optional
package_id
ObjectId
Proto3 optional
struct_name
Identifier
Proto3 optional
### TypeTag​
Type of a Move value.
Fields
Union field **tag** can be only one of the following.
address
Empty
bool
Empty
signer
Empty
struct
StructTag
u128
Empty
u16
Empty
u256
Empty
u32
Empty
u64
Empty
u8
Empty
vector
TypeTag
### U128​
An unsigned 128-bit integer encoded in little-endian using 16-bytes.
Fields
bytes
bytes
Proto3 optional
16-byte little-endian bytes.
### U256​
An unsigned 256-bit integer encoded in little-endian using 32-bytes.
Fields
bytes
bytes
Proto3 optional
16-byte little-endian bytes.
### UnchangedSharedObject​
A shared object that wasn't changed during execution.
Fields
object_id
ObjectId
Proto3 optional
ObjectId of the shared object.
Union field **kind** can be only one of the following.
cancelled
uint64
Shared objects that was congested and resulted in this transaction being cancelled.
mutate_deleted
uint64
Deleted shared objects that appear mutably/owned in the input.
per_epoch_config
Empty
Read of a per-epoch config object that should remain the same during an epoch.
read_deleted
uint64
Deleted shared objects that appear as read-only in the input.
read_only_root
ReadOnlyRoot
Read-only shared object from the input.
### Upgrade​
Command to upgrade an already published package.
Fields
dependencies
ObjectId
Repeated []
Set of packages that the to-be published package depends on.
modules
bytes
Repeated []
The serialized Move modules.
package
ObjectId
Proto3 optional
Package ID of the package to upgrade.
ticket
Argument
Proto3 optional
Ticket authorizing the upgrade.
### UpgradeInfo​
Upgraded package info for the linkage table.
Fields
original_id
ObjectId
Proto3 optional
ID of the original package.
upgraded_id
ObjectId
Proto3 optional
ID of the upgraded package.
upgraded_version
uint64
Proto3 optional
Version of the upgraded package.
### UserSignature​
A signature from a user.
Fields
Union field **signature** can be only one of the following.
multisig
MultisigAggregatedSignature
passkey
PasskeyAuthenticator
simple
SimpleSignature
zklogin
ZkLoginAuthenticator
### ValidatorAggregatedSignature​
An aggregated signature from multiple validators.
Fields
bitmap
RoaringBitmap
Proto3 optional
Bitmap indicating which members of the committee contributed to this signature.
epoch
uint64
Proto3 optional
The epoch when this signature was produced. This can be used to lookup the `ValidatorCommittee` from this epoch to verify this signature.
signature
bytes
Proto3 optional
The 48-byte Bls12381 aggregated signature.
### ValidatorCommittee​
The validator set for a particular epoch.
Fields
epoch
uint64
Proto3 optional
The epoch where this committee governs.
members
ValidatorCommitteeMember
Repeated []
The committee members.
### ValidatorCommitteeMember​
A member of a validator committee.
Fields
public_key
bytes
Proto3 optional
The 96-byte Bls12381 public key for this validator.
stake
uint64
Proto3 optional
Stake weight this validator possesses.
### VersionAssignment​
Object version assignment from consensus.
Fields
object_id
ObjectId
Proto3 optional
`ObjectId` of the object.
version
uint64
Proto3 optional
Assigned version.
### ZkLoginAuthenticator​
A zklogin authenticator.
Fields
inputs
ZkLoginInputs
Proto3 optional
Zklogin proof and inputs required to perform proof verification.
max_epoch
uint64
Proto3 optional
Maximum epoch for which the proof is valid.
signature
SimpleSignature
Proto3 optional
User signature with the public key attested to by the provided proof.
### ZkLoginClaim​
A claim of the iss in a zklogin proof.
Fields
index_mod_4
uint32
Proto3 optional
value
string
Proto3 optional
### ZkLoginInputs​
A zklogin groth16 proof and the required inputs to perform proof verification.
Fields
address_seed
Bn254FieldElement
Proto3 optional
header_base64
string
Proto3 optional
iss_base64_details
ZkLoginClaim
Proto3 optional
proof_points
ZkLoginProof
Proto3 optional
### ZkLoginProof​
A zklogin groth16 proof.
Fields
a
CircomG1
Proto3 optional
b
CircomG2
Proto3 optional
c
CircomG1
Proto3 optional
### ZkLoginPublicIdentifier​
Public key equivalent for zklogin authenticators.
Fields
address_seed
Bn254FieldElement
Proto3 optional
iss
string
Proto3 optional
## sui/types/signature_scheme.proto​
#### Enums
#### SignatureScheme
Flag use to disambiguate the signature schemes supported by Sui. Note: the enum values defined by this proto message exactly match their expected BCS serialized values when serialized as a u8. See enum.SignatureScheme for more information about signature schemes.
Enums
`ED25519`
`SECP256K1`
`SECP256R1`
`MULTISIG`
`BLS12381`
`ZKLOGIN`
`PASSKEY`
## sui/node/v2/node_service.proto​
The sui.node.v2 package contains API definitions for services that are expected to run on Fullnodes.
#### Messages
### BalanceChange​
The delta, or change, in balance for an address for a particular `Coin` type.
Fields
address
Address
Proto3 optional
The account address that is affected by this balance change event.
amount
I128
Proto3 optional
The amount or change in balance.
coin_type
TypeTag
Proto3 optional
The `Coin` type of this balance change event.
### EffectsFinality​
Indicates the finality of the executed transaction.
Fields
Union field **finality** can be only one of the following.
certified
ValidatorAggregatedSignature
A quorum certificate certifying that a transaction is final but might not be included in a checkpoint yet.
checkpointed
uint64
Sequence number of the checkpoint that includes the transaction.
quorum_executed
Empty
Indicates that a quorum of validators has executed the transaction but that it might not be included in a checkpoint yet.
### ExecuteTransactionRequest​
Request message for `NodeService.ExecuteTransaction`.
Note: You must provide only one of `transaction` or `transaction_bcs`.
Fields
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `effects,events,finality`.
signatures
UserSignature
Repeated []
Set of `UserSiganture`s authorizing the execution of the provided transaction.
signatures_bytes
bytes
Repeated []
Set of `UserSiganture`s authorizing the execution of the provided transaction, encoded as bytes.
transaction
Transaction
Proto3 optional
The transaction to execute.
transaction_bcs
Bcs
Proto3 optional
The transaction to execute, encoded as BCS bytes.
### ExecuteTransactionResponse​
Response message for `NodeService.ExecuteTransaction`.
Fields
balance_changes
BalanceChange
Repeated []
Set of balance change events as a result of this transaction. This set of events are calculated by analyzing all input and output `Coin` type objects.
effects
TransactionEffects
Proto3 optional
The `TransactionEffects` for this transaction.
effects_bcs
Bcs
Proto3 optional
The TransactionEffects for this transaction encoded as BCS bytes.
events
TransactionEvents
Proto3 optional
The `TransactionEvents` for this transaction. This field might be empty, even if it was explicitly requested, if the transaction didn't produce any events. `sui.types.TransactionEffects.events_digest` is populated if the transaction produced any events.
events_bcs
Bcs
Proto3 optional
The TransactionEvents for this transaction encoded as BCS bytes.
finality
EffectsFinality
Proto3 optional
Indicates the finality of the executed transaction.
### FullCheckpointObject​
An object used by or produced from a transaction.
Fields
digest
Digest
Proto3 optional
The digest of this object.
object
Object
Proto3 optional
The object itself.
object_bcs
Bcs
Proto3 optional
The object encoded as BCS bytes.
object_id
ObjectId
Proto3 optional
The `ObjectId` of this object.
version
uint64
Proto3 optional
The version of this object.
### FullCheckpointTransaction​
A transaction, with all of its inputs and outputs.
Fields
digest
Digest
Proto3 optional
The digest of this transaction.
effects
TransactionEffects
Proto3 optional
The `TransactionEffects` for this transaction.
effects_bcs
Bcs
Proto3 optional
The TransactionEffects for this transaction encoded as BCS bytes.
events
TransactionEvents
Proto3 optional
The `TransactionEvents` for this transaction. This field might be empty, even if it was explicitly requested, if the transaction didn't produce any events. `sui.types.TransactionEffects.events_digest` is populated if the transaction produced any events.
events_bcs
Bcs
Proto3 optional
The TransactionEvents for this transaction encoded as BCS bytes.
input_objects
FullCheckpointObject
Repeated []
Set of input objects used during the execution of this transaction.
output_objects
FullCheckpointObject
Repeated []
Set of output objects produced from the execution of this transaction.
transaction
Transaction
Proto3 optional
The transaction itself.
transaction_bcs
Bcs
Proto3 optional
The Transaction encoded as BCS bytes.
### GetCheckpointRequest​
Request message for `NodeService.GetCheckpoint`.
At most, provide one of `sequence_number` or `digest`. An error is returned if you attempt to provide both. If you provide neither, the service returns the latest executed checkpoint.
Fields
digest
Digest
Proto3 optional
The digest of the requested checkpoint.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `sequence_number,digest`.
sequence_number
uint64
Proto3 optional
The sequence number of the requested checkpoint.
### GetCheckpointResponse​
Response message for `NodeService.GetCheckpoint`.
Fields
contents
CheckpointContents
Proto3 optional
The `CheckpointContents` for this checkpoint.
contents_bcs
Bcs
Proto3 optional
The CheckpointContents for this checkpoint encoded as BCS bytes.
digest
Digest
Proto3 optional
The digest of this checkpoint's `CheckpointSummary`.
sequence_number
uint64
Proto3 optional
The sequence number of this checkpoint.
signature
ValidatorAggregatedSignature
Proto3 optional
An aggregated quorum signature from the validator committee that certifies this checkpoint.
summary
CheckpointSummary
Proto3 optional
The `CheckpointSummary` for this checkpoint.
summary_bcs
Bcs
Proto3 optional
The CheckpointSummary for this checkpoint encoded as BCS bytes.
### GetCommitteeRequest​
Request message for NodeService.GetCommittee.
Fields
epoch
uint64
Proto3 optional
Request the sui.types.ValidatorCommittee corresponding to the provided epoch. If no epoch is provided the committee for the current epoch will be returned.
### GetCommitteeResponse​
Response message for `NodeService.GetCommittee`.
Fields
committee
ValidatorCommittee
Proto3 optional
The committee of either the requested epoch or the current epoch.
### GetFullCheckpointRequest​
Request message for `NodeService.GetFullCheckpoint`.
At most, provide one of `sequence_number` or `digest`. An error is returned if you provide both. If you provide neither, the service returns the latest executed checkpoint.
Fields
digest
Digest
Proto3 optional
The digest of the requested checkpoint.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `sequence_number,digest`.
sequence_number
uint64
Proto3 optional
The sequence number of the requested checkpoint.
### GetFullCheckpointResponse​
Response message for `NodeService.GetFullCheckpoint`.
Fields
contents
CheckpointContents
Proto3 optional
The `CheckpointContents` for this checkpoint.
contents_bcs
Bcs
Proto3 optional
The CheckpointContents for this checkpoint encoded as BCS bytes.
digest
Digest
Proto3 optional
The digest of this checkpoint's `CheckpointSummary`.
sequence_number
uint64
Proto3 optional
The sequence number of this checkpoint.
signature
ValidatorAggregatedSignature
Proto3 optional
An aggregated quorum signature from the validator committee that certifies this checkpoint.
summary
CheckpointSummary
Proto3 optional
The `CheckpointSummary` for this checkpoint.
summary_bcs
Bcs
Proto3 optional
The CheckpointSummary for this checkpoint encoded as BCS bytes.
transactions
FullCheckpointTransaction
Repeated []
List of transactions included in this checkpoint.
### GetNodeInfoRequest​
Request message for `NodeService.GetNodeInfo`.
### GetNodeInfoResponse​
Response message for `NodeService.GetNodeInfo`.
Fields
chain
string
Proto3 optional
Human-readable name of the chain that this node is on. This is intended to be a human-readable name like `mainnet`, `testnet`, and so on.
chain_id
Digest
Proto3 optional
The chain identifier of the chain that this node is on. The chain identifier is the digest of the genesis checkpoint, the checkpoint with sequence number 0.
checkpoint_height
uint64
Proto3 optional
Checkpoint height of the most recently executed checkpoint.
epoch
uint64
Proto3 optional
Current epoch of the node based on its highest executed checkpoint.
lowest_available_checkpoint
uint64
Proto3 optional
The lowest checkpoint for which checkpoints and transaction data are available.
lowest_available_checkpoint_objects
uint64
Proto3 optional
The lowest checkpoint for which object data is available.
software_version
string
Proto3 optional
Software version of the `sui-node` binary.
timestamp
Timestamp
Proto3 optional
Unix timestamp of the most recently executed checkpoint.
### GetObjectRequest​
Request message for `NodeService.GetObject`.
Fields
object_id
ObjectId
Proto3 optional
Required. The `ObjectId` of the requested object.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `object_id,version,digest`.
version
uint64
Proto3 optional
Request a specific version of the object. If no version is specified, and the object is live, then the latest version of the object is returned.
### GetObjectResponse​
Response message for `NodeService.GetObject`.
Fields
digest
Digest
Proto3 optional
The digest of this object.
object
Object
Proto3 optional
The object itself.
object_bcs
Bcs
Proto3 optional
The Object encoded as BCS bytes.
object_id
ObjectId
Proto3 optional
The `ObjectId` of this object.
version
uint64
Proto3 optional
The version of this object.
### GetTransactionRequest​
Request message for `NodeService.GetTransaction`.
Fields
digest
Digest
Proto3 optional
Required. The digest of the requested transaction.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `digest`.
### GetTransactionResponse​
Response message for `NodeService.GetTransactio`n.
Fields
checkpoint
uint64
Proto3 optional
The sequence number for the checkpoint that includes this transaction.
digest
Digest
Proto3 optional
The digest of this Transaction.
effects
TransactionEffects
Proto3 optional
The `TransactionEffects` for this transaction.
effects_bcs
Bcs
Proto3 optional
The TransactionEffects for this transaction encoded as BCS bytes.
events
TransactionEvents
Proto3 optional
The `TransactionEvents` for this transaction. This field might be empty, even if it was explicitly requested, if the transaction didn't produce any events. `sui.types.TransactionEffects.events_digest` is populated if the transaction produced any events.
events_bcs
Bcs
Proto3 optional
The TransactionEvents for this transaction encoded as BCS bytes.
signatures
UserSignature
Repeated []
List of user signatures that are used to authorize the execution of this transaction.
signatures_bytes
bytes
Repeated []
List of UserSignatures encoded as bytes.
timestamp
Timestamp
Proto3 optional
The Unix timestamp of the checkpoint that includes this transaction.
transaction
Transaction
Proto3 optional
The transaction itself.
transaction_bcs
Bcs
Proto3 optional
The Transaction encoded as BCS bytes.
### Services (node_service.proto)​
#### NodeService
Service for reading data from a Sui Fullnode.
Methods
GetNodeInfoRequest -> GetNodeInfoResponse
Query a node for information about its current state.
GetCommitteeRequest -> GetCommitteeResponse
Request the validator committee for a particular epoch or for the current epoch.
GetObjectRequest -> GetObjectResponse
Request information for the specified object. Use this API to request an object by its `ObjectId`. The version of the object returned is dependent on if you request a specific version. If you do not request a specific version (GetObjectRequest.version is `None`), then the most recent version (if the object is live) is returned. If you do request a version, that version is returned if it historically existed, is available, and has not been pruned. Due to storage limitations, implementers of this service might prune older historical data, which can limit the data availability of this API. To determine the data availability range for historical objects, clients can look at `GetNodeInfoResponse.lowest_available_checkpoint_objects` to see the lowest checkpoint for which historical object data is available.
GetTransactionRequest -> GetTransactionResponse
Request information for the specified transaction. Use this API to request information about a transaction by its digest. Due to storage limitations, implementers of this service might prune older historical data, which can limit the data availability of this API. To determine the data availability range for historical transactions, clients can look at `GetNodeInfoResponse.lowest_available_checkpoint` to see the lowest checkpoint for which historical transaction data is available.
GetCheckpointRequest -> GetCheckpointResponse
Request information for the specified checkpoint. Use this API to request information about a checkpoint either by its digest or its sequence number (height). Due to storage limitations, implementers of this service might prune older historical data, which can limit the data availability of this API. To determine the data availability range for historical checkpoints, clients can look at `GetNodeInfoResponse.lowest_available_checkpoint` to see the lowest checkpoint for which historical checkpoint data is available.
GetFullCheckpointRequest -> GetFullCheckpointResponse
Request information for the entirety of the specified checkpoint. Use this API to request information about a checkpoint either by its digest or its sequence number (height). In particular, you can use this API to request information about all the transactions included in a checkpoint, as well as their input and output objects. Due to storage limitations, implementers of this service might prune older historical data, which can limit the data availability of this API. To determine the data availability range for historical checkpoints, clients can look at `GetNodeInfoResponse.lowest_available_checkpoint` to see the lowest checkpoint for which historical checkpoint/transaction data is available and `GetNodeInfoResponse.lowest_available_checkpoint_objects` for which historical object data is available.
ExecuteTransactionRequest -> ExecuteTransactionResponse
Request that the provided transaction be relayed to the validator set for execution and inclusion in the blockchain.
## sui/rpc/v2beta/input.proto​
#### Messages
### Input​
An input to a user transaction.
Fields
digest
string
Proto3 optional
The digest of this object.
kind
InputKind
Proto3 optional
mutable
bool
Proto3 optional
Controls whether the caller asks for a mutable reference to the shared object.
object_id
string
Proto3 optional
`ObjectId` of the object input.
pure
bytes
Proto3 optional
A move value serialized as BCS. For normal operations this is required to be a move primitive type and not contain structs or objects.
version
uint64
Proto3 optional
Requested version of the input object when `kind` is `IMMUTABLE_OR_OWNED` or `RECEIVING` or if `kind` is `SHARED` this is the initial version of the object when it was shared
#### Enums
#### InputKind
Enums
`INPUT_KIND_UNKNOWN`
`PURE`
A move value serialized as BCS.
`IMMUTABLE_OR_OWNED`
A Move object that is either immutable or address owned.
`SHARED`
A Move object whose owner is "Shared".
`RECEIVING`
A Move object that is attempted to be received in this transaction.
## sui/rpc/v2beta/execution_status.proto​
#### Messages
### CommandArgumentError​
An error with an argument to a command.
Fields
argument
uint32
Proto3 optional
Position of the problematic argument.
index
uint32
Proto3 optional
Index of an input or result.
kind
CommandArgumentErrorKind
Proto3 optional
subresult
uint32
Proto3 optional
Index of a subresult.
### ExecutionError​
An error that can occur during the execution of a transaction.
Fields
abort_code
uint64
Proto3 optional
Abort code from Move.
address
string
Proto3 optional
Denied address.
coin_type
string
Proto3 optional
Coin type.
command
uint64
Proto3 optional
The command, if any, during which the error occurred.
command_argument_error
CommandArgumentError
Proto3 optional
congested_objects
string
Repeated []
Set of objects that were congested, leading to the transaction's cancellation.
index
uint32
Proto3 optional
Index of an input or result.
kind
ExecutionErrorKind
Proto3 optional
location
MoveLocation
Proto3 optional
Location in Move where the error occurred.
object_id
string
Proto3 optional
package_upgrade_error
PackageUpgradeError
Proto3 optional
size_error
SizeError
Proto3 optional
subresult
uint32
Proto3 optional
Index of a subresult.
type_argument_error
TypeArgumentError
Proto3 optional
### ExecutionStatus​
The status of an executed transaction.
Fields
error
ExecutionError
Proto3 optional
The error if `success` is false.
success
bool
Proto3 optional
Indicates if the transaction was successful or not.
### MoveLocation​
Location in Move bytecode where an error occurred.
Fields
function
uint32
Proto3 optional
The function index.
function_name
string
Proto3 optional
The name of the function, if available.
instruction
uint32
Proto3 optional
Offset of the instruction where the error occurred.
module
string
Proto3 optional
The module name.
package
string
Proto3 optional
The package ID.
### PackageUpgradeError​
An error with upgrading a package.
Fields
digest
string
Proto3 optional
A digest.
kind
PackageUpgradeErrorKind
Proto3 optional
package_id
string
Proto3 optional
The Package Id.
policy
uint32
Proto3 optional
The policy.
ticket_id
string
Proto3 optional
The ticket Id.
### SizeError​
A size error.
Fields
max_size
uint64
Proto3 optional
The maximum allowable size.
size
uint64
Proto3 optional
The offending size.
### TypeArgumentError​
Type argument error.
Fields
kind
TypeArgumentErrorKind
Proto3 optional
type_argument
uint32
Proto3 optional
Index of the problematic type argument.
#### Enums
#### CommandArgumentErrorKind
Enums
`COMMAND_ARGUMENT_ERROR_KIND_UNKNOWN`
`TYPE_MISMATCH`
The type of the value does not match the expected type.
`INVALID_BCS_BYTES`
The argument cannot be deserialized into a value of the specified type.
`INVALID_USAGE_OF_PURE_ARGUMENT`
The argument cannot be instantiated from raw bytes.
`INVALID_ARGUMENT_TO_PRIVATE_ENTRY_FUNCTION`
Invalid argument to private entry function. Private entry functions cannot take arguments from other Move functions.
`INDEX_OUT_OF_BOUNDS`
Out of bounds access to input or results. `index` field will be set indicating the invalid index value.
`SECONDARY_INDEX_OUT_OF_BOUNDS`
Out of bounds access to subresult. `index` and `subresult` fields will be set indicating the invalid index value.
`INVALID_RESULT_ARITY`
Invalid usage of result. Expected a single result but found either no return value or multiple. `index` field will be set indicating the invalid index value.
`INVALID_GAS_COIN_USAGE`
Invalid usage of gas coin. The gas coin can only be used by-value with a `TransferObject` command.
`INVALID_VALUE_USAGE`
Invalid usage of Move value. - Mutably borrowed values require unique usage. - Immutably borrowed values cannot be taken or borrowed mutably. - Taken values cannot be used again.
`INVALID_OBJECT_BY_VALUE`
Immutable objects cannot be passed by-value.
`INVALID_OBJECT_BY_MUT_REF`
Immutable objects cannot be passed by mutable reference, `&mut`.
`SHARED_OBJECT_OPERATION_NOT_ALLOWED`
Shared object operations such as wrapping, freezing, or converting to owned are not allowed.
#### ExecutionErrorKind
Enums
`EXECUTION_ERROR_KIND_UNKNOWN`
`INSUFFICIENT_GAS`
Insufficient gas.
`INVALID_GAS_OBJECT`
Invalid `Gas` object.
`INVARIANT_VIOLATION`
Invariant violation.
`FEATURE_NOT_YET_SUPPORTED`
Attempted to use feature that is not supported yet.
`OBJECT_TOO_BIG`
Move object is larger than the maximum allowed size.
`PACKAGE_TOO_BIG`
Package is larger than the maximum allowed size.
`CIRCULAR_OBJECT_OWNERSHIP`
Circular object ownership.
`INSUFFICIENT_COIN_BALANCE`
Insufficient coin balance for requested operation.
`COIN_BALANCE_OVERFLOW`
Coin balance overflowed an u64.
`PUBLISH_ERROR_NON_ZERO_ADDRESS`
Publish error, non-zero address. The modules in the package must have their self-addresses set to zero.
`SUI_MOVE_VERIFICATION_ERROR`
Sui Move bytecode verification error.
`MOVE_PRIMITIVE_RUNTIME_ERROR`
Error from a non-abort instruction. Possible causes: Arithmetic error, stack overflow, max value depth, or similar.
`MOVE_ABORT`
Move runtime abort.
`VM_VERIFICATION_OR_DESERIALIZATION_ERROR`
Bytecode verification error.
`VM_INVARIANT_VIOLATION`
MoveVm invariant violation.
`FUNCTION_NOT_FOUND`
Function not found.
`ARITY_MISMATCH`
Parity mismatch for Move function. The number of arguments does not match the number of parameters.
`TYPE_ARITY_MISMATCH`
Type parity mismatch for Move function. Mismatch between the number of actual versus expected type arguments.
`NON_ENTRY_FUNCTION_INVOKED`
Non-entry function invoked. Move Call must start with an entry function.
`COMMAND_ARGUMENT_ERROR`
Invalid command argument.
`TYPE_ARGUMENT_ERROR`
Type argument error.
`UNUSED_VALUE_WITHOUT_DROP`
Unused result without the drop ability.
`INVALID_PUBLIC_FUNCTION_RETURN_TYPE`
Invalid public Move function signature. Unsupported return type for return value.
`INVALID_TRANSFER_OBJECT`
Invalid transfer object, object does not have public transfer.
`EFFECTS_TOO_LARGE`
Effects from the transaction are too large.
`PUBLISH_UPGRADE_MISSING_DEPENDENCY`
Publish or Upgrade is missing dependency.
`PUBLISH_UPGRADE_DEPENDENCY_DOWNGRADE`
Publish or upgrade dependency downgrade. Indirect (transitive) dependency of published or upgraded package has been assigned an on-chain version that is less than the version required by one of the package's transitive dependencies.
`PACKAGE_UPGRADE_ERROR`
Invalid package upgrade.
`WRITTEN_OBJECTS_TOO_LARGE`
Indicates the transaction tried to write objects too large to storage.
`CERTIFICATE_DENIED`
Certificate is on the deny list.
`SUI_MOVE_VERIFICATION_TIMEDOUT`
Sui Move bytecode verification timed out.
`SHARED_OBJECT_OPERATION_NOT_ALLOWED`
The requested shared object operation is not allowed.
`INPUT_OBJECT_DELETED`
Requested shared object has been deleted.
`EXECUTION_CANCELED_DUE_TO_SHARED_OBJECT_CONGESTION`
Certificate is canceled due to congestion on shared objects.
`ADDRESS_DENIED_FOR_COIN`
Address is denied for this coin type.
`COIN_TYPE_GLOBAL_PAUSE`
Coin type is globally paused for use.
`EXECUTION_CANCELED_DUE_TO_RANDOMNESS_UNAVAILABLE`
Certificate is canceled because randomness could not be generated this epoch.
#### PackageUpgradeErrorKind
Enums
`PACKAGE_UPGRADE_ERROR_KIND_UNKNOWN`
`UNABLE_TO_FETCH_PACKAGE`
Unable to fetch package.
`NOT_A_PACKAGE`
Object is not a package.
`INCOMPATIBLE_UPGRADE`
Package upgrade is incompatible with previous version.
`DIGETS_DOES_NOT_MATCH`
Digest in upgrade ticket and computed digest differ.
`UNKNOWN_UPGRADE_POLICY`
Upgrade policy is not valid.
`PACKAGE_ID_DOES_NOT_MATCH`
Package ID does not match `PackageId` in upgrade ticket.
#### TypeArgumentErrorKind
Enums
`TYPE_ARGUMENT_ERROR_KIND_UNKNOWN`
`TYPE_NOT_FOUND`
A type was not found in the module specified.
`CONSTRAINT_NOT_SATISFIED`
A type provided did not match the specified constraint.
## sui/rpc/v2beta/checkpoint_summary.proto​
#### Messages
### CheckpointCommitment​
A commitment made by a checkpoint.
Fields
digest
string
Proto3 optional
kind
CheckpointCommitmentKind
Proto3 optional
### CheckpointSummary​
A header for a checkpoint on the Sui blockchain.
On the Sui network, checkpoints define the history of the blockchain. They are quite similar to the concept of blocks used by other blockchains like Bitcoin or Ethereum. The Sui blockchain, however, forms checkpoints after transaction execution has already happened to provide a certified history of the chain, instead of being formed before execution.
Checkpoints commit to a variety of state, including but not limited to:
  * The hash of the previous checkpoint.
  * The set of transaction digests, their corresponding effects digests, as well as the set of user signatures that authorized its execution.
  * The objects produced by a transaction.
  * The set of live objects that make up the current state of the chain.
  * On epoch transitions, the next validator committee.


`CheckpointSummary`s themselves don't directly include all of the previous information but they are the top-level type by which all the information is committed to transitively via cryptographic hashes included in the summary. `CheckpointSummary`s are signed and certified by a quorum of the validator committee in a given epoch to allow verification of the chain's state.
Fields
bcs
Bcs
Proto3 optional
This CheckpointSummary serialized as BCS.
commitments
CheckpointCommitment
Repeated []
Commitments to checkpoint-specific state.
content_digest
string
Proto3 optional
The hash of the `CheckpointContents` for this checkpoint.
digest
string
Proto3 optional
The digest of this CheckpointSummary.
end_of_epoch_data
EndOfEpochData
Proto3 optional
Extra data only present in the final checkpoint of an epoch.
epoch
uint64
Proto3 optional
Epoch that this checkpoint belongs to.
epoch_rolling_gas_cost_summary
GasCostSummary
Proto3 optional
The running total gas costs of all transactions included in the current epoch so far until this checkpoint.
previous_digest
string
Proto3 optional
The hash of the previous `CheckpointSummary`. This will be `None` only for the first, or genesis, checkpoint.
sequence_number
uint64
Proto3 optional
The height of this checkpoint.
timestamp
Timestamp
Proto3 optional
Timestamp of the checkpoint - number of milliseconds from the Unix epoch Checkpoint timestamps are monotonic, but not strongly monotonic - subsequent checkpoints can have the same timestamp if they originate from the same underlining consensus commit.
total_network_transactions
uint64
Proto3 optional
Total number of transactions committed since genesis, including those in this checkpoint.
version_specific_data
bytes
Proto3 optional
`CheckpointSummary` is not an evolvable structure - it must be readable by any version of the code. Therefore, to allow extensions to be added to `CheckpointSummary`, opaque data can be added to checkpoints, which can be deserialized based on the current protocol version.
### EndOfEpochData​
Data, which when included in a `CheckpointSummary`, signals the end of an `Epoch`.
Fields
epoch_commitments
CheckpointCommitment
Repeated []
Commitments to epoch specific state (live object set)
next_epoch_committee
ValidatorCommitteeMember
Repeated []
The set of validators that will be in the `ValidatorCommittee` for the next epoch.
next_epoch_protocol_version
uint64
Proto3 optional
The protocol version that is in effect during the next epoch.
#### Enums
#### CheckpointCommitmentKind
Enums
`CHECKPOINT_COMMITMENT_KIND_UNKNOWN`
`ECMH_LIVE_OBJECT_SET`
An elliptic curve multiset hash attesting to the set of objects that comprise the live state of the Sui blockchain.
## sui/rpc/v2beta/effects.proto​
#### Messages
### ChangedObject​
Input/output state of an object that was changed during execution.
Fields
id_operation
IdOperation
Proto3 optional
What happened to an `ObjectId` during execution.
input_digest
string
Proto3 optional
Digest of the object before this transaction executed.
input_owner
Owner
Proto3 optional
Owner of the object before this transaction executed.
input_state
InputObjectState
Proto3 optional
input_version
uint64
Proto3 optional
Version of the object before this transaction executed.
object_id
string
Proto3 optional
ID of the object.
object_type
string
Proto3 optional
Type information is not provided by the effects structure but is instead provided by an indexing layer
output_digest
string
Proto3 optional
Digest of the object after this transaction executed.
output_owner
Owner
Proto3 optional
Owner of the object after this transaction executed.
output_state
OutputObjectState
Proto3 optional
output_version
uint64
Proto3 optional
Version of the object after this transaction executed.
### TransactionEffects​
The effects of executing a transaction.
Fields
auxiliary_data_digest
string
Proto3 optional
Auxiliary data that are not protocol-critical, generated as part of the effects but are stored separately. Storing it separately allows us to avoid bloating the effects with data that are not critical. It also provides more flexibility on the format and type of the data.
bcs
Bcs
Proto3 optional
This TransactionEffects serialized as BCS.
changed_objects
ChangedObject
Repeated []
Objects whose state are changed by this transaction.
dependencies
string
Repeated []
The set of transaction digests this transaction depends on.
digest
string
Proto3 optional
The digest of this TransactionEffects.
epoch
uint64
Proto3 optional
The epoch when this transaction was executed.
events_digest
string
Proto3 optional
The digest of the events emitted during execution, can be `None` if the transaction does not emit any event.
gas_object
ChangedObject
Proto3 optional
Information about the gas object. Also present in the `changed_objects` vector. System transaction that don't require gas will leave this as `None`.
gas_used
GasCostSummary
Proto3 optional
The gas used by this transaction.
lamport_version
uint64
Proto3 optional
The version number of all the written objects (excluding packages) by this transaction.
status
ExecutionStatus
Proto3 optional
The status of the execution.
transaction_digest
string
Proto3 optional
The transaction digest.
unchanged_shared_objects
UnchangedSharedObject
Repeated []
Shared objects that are not mutated in this transaction. Unlike owned objects, read-only shared objects' version are not committed in the transaction, and in order for a node to catch up and execute it without consensus sequencing, the version needs to be committed in the effects.
version
int32
Proto3 optional
Version of this TransactionEffects.
### UnchangedSharedObject​
A shared object that wasn't changed during execution.
Fields
digest
string
Proto3 optional
Digest of the shared object.
kind
UnchangedSharedObjectKind
Proto3 optional
object_id
string
Proto3 optional
ObjectId of the shared object.
object_type
string
Proto3 optional
Type information is not provided by the effects structure but is instead provided by an indexing layer
version
uint64
Proto3 optional
Version of the shared object.
#### Enums
#### IdOperation
Enums
`ID_OPERATION_UNKNOWN`
`NONE`
`CREATED`
`DELETED`
#### InputObjectState
Enums
`INPUT_OBJECT_STATE_UNKNOWN`
`INPUT_OBJECT_STATE_DOES_NOT_EXIST`
`INPUT_OBJECT_STATE_EXISTS`
#### OutputObjectState
Enums
`OUTPUT_OBJECT_STATE_UNKNOWN`
`OUTPUT_OBJECT_STATE_DOES_NOT_EXIST`
`OUTPUT_OBJECT_STATE_OBJECT_WRITE`
`OUTPUT_OBJECT_STATE_PACKAGE_WRITE`
#### UnchangedSharedObjectKind
Enums
`UNCHANGED_SHARED_OBJECT_KIND_UNKNOWN`
`READ_ONLY_ROOT`
Read-only shared object from the input.
`MUTATE_DELETED`
Deleted shared objects that appear mutably/owned in the input.
`READ_DELETED`
Deleted shared objects that appear as read-only in the input.
`CANCELED`
Shared objects that was congested and resulted in this transaction being canceled.
`PER_EPOCH_CONFIG`
Read of a per-epoch config object that should remain the same during an epoch.
## sui/rpc/v2beta/transaction_execution_service.proto​
#### Messages
### ExecuteTransactionRequest​
Fields
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `finality`.
signatures
UserSignature
Repeated []
Set of `UserSiganture`s authorizing the execution of the provided transaction.
transaction
Transaction
Proto3 optional
The transaction to execute.
### ExecuteTransactionResponse​
Response message for `NodeService.ExecuteTransaction`.
Fields
finality
TransactionFinality
Proto3 optional
Indicates the finality of the executed transaction.
transaction
ExecutedTransaction
Proto3 optional
### TransactionFinality​
Indicates the finality of the executed transaction.
Fields
Union field **finality** can be only one of the following.
certified
ValidatorAggregatedSignature
A quorum certificate certifying that a transaction is final but might not be included in a checkpoint yet.
checkpointed
uint64
Sequence number of the checkpoint that includes the transaction.
quorum_executed
Empty
Indicates that a quorum of validators has executed the transaction but that it might not be included in a checkpoint yet.
### Services (transaction_execution_service.proto)​
#### TransactionExecutionService
Methods
ExecuteTransactionRequest -> ExecuteTransactionResponse
## sui/rpc/v2beta/transaction.proto​
#### Messages
### ActiveJwk​
A new JWK.
Fields
epoch
uint64
Proto3 optional
Most recent epoch in which the JWK was validated.
id
JwkId
Proto3 optional
Identifier used to uniquely identify a JWK.
jwk
Jwk
Proto3 optional
The JWK.
### AuthenticatorStateExpire​
Expire old JWKs.
Fields
authenticator_object_initial_shared_version
uint64
Proto3 optional
The initial version of the authenticator object that it was shared at.
min_epoch
uint64
Proto3 optional
Expire JWKs that have a lower epoch than this.
### AuthenticatorStateUpdate​
Update the set of valid JWKs.
Fields
authenticator_object_initial_shared_version
uint64
Proto3 optional
The initial version of the authenticator object that it was shared at.
epoch
uint64
Proto3 optional
Epoch of the authenticator state update transaction.
new_active_jwks
ActiveJwk
Repeated []
Newly active JWKs.
round
uint64
Proto3 optional
Consensus round of the authenticator state update.
### CanceledTransaction​
A transaction that was canceled.
Fields
digest
string
Proto3 optional
Digest of the canceled transaction.
version_assignments
VersionAssignment
Repeated []
List of object version assignments.
### CanceledTransactions​
Set of canceled transactions.
Fields
canceled_transactions
CanceledTransaction
Repeated []
### ChangeEpoch​
System transaction used to change the epoch.
Fields
computation_charge
uint64
Proto3 optional
The total amount of gas charged for computation during the epoch.
epoch
uint64
Proto3 optional
The next (to become) epoch ID.
epoch_start_timestamp
Timestamp
Proto3 optional
Unix timestamp when epoch started.
non_refundable_storage_fee
uint64
Proto3 optional
The non-refundable storage fee.
protocol_version
uint64
Proto3 optional
The protocol version in effect in the new epoch.
storage_charge
uint64
Proto3 optional
The total amount of gas charged for storage during the epoch.
storage_rebate
uint64
Proto3 optional
The amount of storage rebate refunded to the txn senders.
system_packages
SystemPackage
Repeated []
System packages (specifically framework and Move stdlib) that are written before the new epoch starts. This tracks framework upgrades on chain. When executing the `ChangeEpoch` txn, the validator must write out the following modules. Modules are provided with the version they will be upgraded to, their modules in serialized form (which include their package ID), and a list of their transitive dependencies.
### Command​
A single command in a programmable transaction.
Fields
Union field **command** can be only one of the following.
make_move_vector
MakeMoveVector
`forall T: Vec<T> -> vector<T>` Given n-values of the same type, it constructs a vector. For non-objects or an empty vector, the type tag must be specified.
merge_coins
MergeCoins
`(&mut Coin<T>, Vec<Coin<T>>)` It merges n-coins into the first coin.
move_call
MoveCall
A call to either an entry or a public Move function.
publish
Publish
Publishes a Move package. It takes the package bytes and a list of the package's transitive dependencies to link against on chain.
split_coins
SplitCoins
`(&mut Coin<T>, Vec<u64>)` -> `Vec<Coin<T>>` It splits off some amounts into new coins with those amounts.
transfer_objects
TransferObjects
`(Vec<forall T:key+store. T>, address)` It sends n-objects to the specified address. These objects must have store (public transfer) and either the previous owner must be an address or the object must be newly created.
upgrade
Upgrade
Upgrades a Move package. Takes (in order): 1. A vector of serialized modules for the package. 2. A vector of object ids for the transitive dependencies of the new package. 3. The object ID of the package being upgraded. 4. An argument holding the `UpgradeTicket` that must have been produced from an earlier command in the same programmable transaction.
### ConsensusCommitPrologue​
Consensus commit prologue system transaction.
This message can represent V1, V2, and V3 prologue types.
Fields
additional_state_digest
string
Proto3 optional
Digest of any additional state computed by the consensus handler. Used to detect forking bugs as early as possible. Present in V4.
commit_timestamp
Timestamp
Proto3 optional
Unix timestamp from consensus. Present in V1, V2, V3, V4.
consensus_commit_digest
string
Proto3 optional
Digest of consensus output. Present in V2, V3, V4.
consensus_determined_version_assignments
ConsensusDeterminedVersionAssignments
Proto3 optional
Stores consensus handler determined shared object version assignments. Present in V3, V4.
epoch
uint64
Proto3 optional
Epoch of the commit prologue transaction. Present in V1, V2, V3, V4.
round
uint64
Proto3 optional
Consensus round of the commit. Present in V1, V2, V3, V4.
sub_dag_index
uint64
Proto3 optional
The sub DAG index of the consensus commit. This field is populated if there are multiple consensus commits per round. Present in V3, V4.
### ConsensusDeterminedVersionAssignments​
Version assignments performed by consensus.
Fields
Union field **kind** can be only one of the following.
canceled_transactions
CanceledTransactions
Canceled transaction version assignment.
### EndOfEpochTransaction​
Set of operations run at the end of the epoch to close out the current epoch and start the next one.
Fields
transactions
EndOfEpochTransactionKind
Repeated []
### EndOfEpochTransactionKind​
Operation run at the end of an epoch.
Fields
Union field **kind** can be only one of the following.
authenticator_state_create
Empty
Create and initialize the authenticator object used for zklogin.
authenticator_state_expire
AuthenticatorStateExpire
Expire JWKs used for zklogin.
bridge_committee_init
uint64
Initialize the bridge committee.
bridge_state_create
string
Create and initialize the bridge object.
change_epoch
ChangeEpoch
End the epoch and start the next one.
deny_list_state_create
Empty
Create and initialize the deny list object.
randomness_state_create
Empty
Create and initialize the randomness object.
### GasPayment​
Payment information for executing a transaction.
Fields
budget
uint64
Proto3 optional
Total budget willing to spend for the execution of a transaction.
objects
ObjectReference
Repeated []
Set of gas objects to use for payment.
owner
string
Proto3 optional
Owner of the gas objects, either the transaction sender or a sponsor.
price
uint64
Proto3 optional
Gas unit price to use when charging for computation. Must be greater than or equal to the network's current RGP (reference gas price).
### GenesisTransaction​
The genesis transaction.
Fields
objects
Object
Repeated []
Set of genesis objects.
### Jwk​
A JSON web key.
Struct that contains info for a JWK. A list of them for different kinds can be retrieved from the JWK endpoint (for example, &#lt;https://www.googleapis.com/oauth2/v3/certs>). The JWK is used to verify the JWT token.
Fields
alg
string
Proto3 optional
Algorithm parameter, https://datatracker.ietf.org/doc/html/rfc7517#section-4.4.
e
string
Proto3 optional
RSA public exponent, https://datatracker.ietf.org/doc/html/rfc7517#section-9.3.
kty
string
Proto3 optional
Key type parameter, https://datatracker.ietf.org/doc/html/rfc7517#section-4.1.
n
string
Proto3 optional
RSA modulus, https://datatracker.ietf.org/doc/html/rfc7517#section-9.3.
### JwkId​
Key to uniquely identify a JWK.
Fields
iss
string
Proto3 optional
The issuer or identity of the OIDC provider.
kid
string
Proto3 optional
A key ID used to uniquely identify a key from an OIDC provider.
### MakeMoveVector​
Command to build a Move vector out of a set of individual elements.
Fields
element_type
string
Proto3 optional
Type of the individual elements. This is required to be set when the type can't be inferred, for example when the set of provided arguments are all pure input values.
elements
Argument
Repeated []
The set individual elements to build the vector with.
### MergeCoins​
Command to merge multiple coins of the same type into a single coin.
Fields
coin
Argument
Proto3 optional
Coin to merge coins into.
coins_to_merge
Argument
Repeated []
Set of coins to merge into `coin`. All listed coins must be of the same type and be the same type as `coin`
### MoveCall​
Command to call a Move function.
Functions that can be called by a `MoveCall` command are those that have a function signature that is either `entry` or `public` (which don't have a reference return type).
Fields
arguments
Argument
Repeated []
The arguments to the function.
function
string
Proto3 optional
The function to be called.
module
string
Proto3 optional
The specific module in the package containing the function.
package
string
Proto3 optional
The package containing the module and function.
type_arguments
string
Repeated []
The type arguments to the function.
### ProgrammableTransaction​
A user transaction.
Contains a series of native commands and Move calls where the results of one command can be used in future commands.
Fields
commands
Command
Repeated []
The commands to be executed sequentially. A failure in any command results in the failure of the entire transaction.
inputs
Input
Repeated []
Input objects or primitive values.
### Publish​
Command to publish a new Move package.
Fields
dependencies
string
Repeated []
Set of packages that the to-be published package depends on.
modules
bytes
Repeated []
The serialized Move modules.
### RandomnessStateUpdate​
Randomness update.
Fields
epoch
uint64
Proto3 optional
Epoch of the randomness state update transaction.
random_bytes
bytes
Proto3 optional
Updated random bytes.
randomness_object_initial_shared_version
uint64
Proto3 optional
The initial version of the randomness object that it was shared at.
randomness_round
uint64
Proto3 optional
Randomness round of the update.
### SplitCoins​
Command to split a single coin object into multiple coins.
Fields
amounts
Argument
Repeated []
The amounts to split off.
coin
Argument
Proto3 optional
The coin to split.
### SystemPackage​
System package.
Fields
dependencies
string
Repeated []
Package dependencies.
modules
bytes
Repeated []
Move modules.
version
uint64
Proto3 optional
Version of the package.
### Transaction​
A transaction.
Fields
bcs
Bcs
Proto3 optional
This Transaction serialized as BCS.
digest
string
Proto3 optional
The digest of this Transaction.
expiration
TransactionExpiration
Proto3 optional
gas_payment
GasPayment
Proto3 optional
kind
TransactionKind
Proto3 optional
sender
string
Proto3 optional
version
int32
Proto3 optional
Version of this Transaction.
### TransactionExpiration​
A TTL for a transaction.
Fields
epoch
uint64
Proto3 optional
kind
TransactionExpirationKind
Proto3 optional
### TransactionKind​
Transaction type.
Fields
Union field **kind** can be only one of the following.
authenticator_state_update
AuthenticatorStateUpdate
Update set of valid JWKs used for zklogin.
change_epoch
ChangeEpoch
System transaction used to end an epoch. The `ChangeEpoch` variant is now deprecated (but the `ChangeEpoch` struct is still used by `EndOfEpochTransaction`).
consensus_commit_prologue_v1
ConsensusCommitPrologue
V1 consensus commit update.
consensus_commit_prologue_v2
ConsensusCommitPrologue
V2 consensus commit update.
consensus_commit_prologue_v3
ConsensusCommitPrologue
V3 consensus commit update.
consensus_commit_prologue_v4
ConsensusCommitPrologue
V4 consensus commit update.
end_of_epoch
EndOfEpochTransaction
Set of operations to run at the end of the epoch to close out the current epoch and start the next one.
genesis
GenesisTransaction
Transaction used to initialize the chain state. Only valid if in the genesis checkpoint (0) and if this is the very first transaction ever executed on the chain.
programmable_transaction
ProgrammableTransaction
A user transaction comprised of a list of native commands and Move calls.
randomness_state_update
RandomnessStateUpdate
Randomness update.
### TransferObjects​
Command to transfer ownership of a set of objects to an address.
Fields
address
Argument
Proto3 optional
The address to transfer ownership to.
objects
Argument
Repeated []
Set of objects to transfer.
### Upgrade​
Command to upgrade an already published package.
Fields
dependencies
string
Repeated []
Set of packages that the to-be published package depends on.
modules
bytes
Repeated []
The serialized Move modules.
package
string
Proto3 optional
Package ID of the package to upgrade.
ticket
Argument
Proto3 optional
Ticket authorizing the upgrade.
### VersionAssignment​
Object version assignment from consensus.
Fields
object_id
string
Proto3 optional
`ObjectId` of the object.
version
uint64
Proto3 optional
Assigned version.
#### Enums
#### TransactionExpirationKind
Enums
`TRANSACTION_EXPIRATION_KIND_UNKNOWN`
`NONE`
The transaction has no expiration.
`EPOCH`
Validators won't sign and execute transaction unless the expiration epoch is greater than or equal to the current epoch.
## sui/rpc/v2beta/owner.proto​
#### Messages
### Owner​
Enum of different types of ownership for an object.
Fields
address
string
Proto3 optional
Address or ObjectId of the owner
kind
OwnerKind
Proto3 optional
version
uint64
Proto3 optional
#### Enums
#### OwnerKind
Enums
`OWNER_KIND_UNKNOWN`
`ADDRESS`
`OBJECT`
`SHARED`
`IMMUTABLE`
## sui/rpc/v2beta/object.proto​
#### Messages
### MoveModule​
Module defined by a package.
Fields
contents
bytes
Proto3 optional
Serialized bytecode of the module.
name
string
Proto3 optional
Name of the module.
### Object​
An object on the Sui blockchain.
Fields
bcs
Bcs
Proto3 optional
This Object serialized as BCS.
contents
Bcs
Proto3 optional
BCS bytes of a Move struct value. Only set for Move structs
digest
string
Proto3 optional
The digest of this Object.
has_public_transfer
bool
Proto3 optional
DEPRECATED this field is no longer used to determine whether a tx can transfer this object. Instead, it is always calculated from the objects type when loaded in execution. Only set for Move structs
linkage_table
UpgradeInfo
Repeated []
For each dependency, maps original package ID to the info about the (upgraded) dependency version that this package is using. Only set for Packages
modules
MoveModule
Repeated []
Set of modules defined by this package. Only set for Packages
object_id
string
Proto3 optional
`ObjectId` for this object.
object_type
string
Proto3 optional
The type of this object. This will be 'package' for packages and a StructTag for move structs.
owner
Owner
Proto3 optional
Owner of the object.
previous_transaction
string
Proto3 optional
The digest of the transaction that created or last mutated this object
storage_rebate
uint64
Proto3 optional
The amount of SUI to rebate if this object gets deleted. This number is re-calculated each time the object is mutated based on the present storage gas price.
type_origin_table
TypeOrigin
Repeated []
Maps struct/module to a package version where it was first defined, stored as a vector for simple serialization and deserialization. Only set for Packages
version
uint64
Proto3 optional
Version of the object.
### TypeOrigin​
Identifies a struct and the module it was defined in.
Fields
module_name
string
Proto3 optional
package_id
string
Proto3 optional
struct_name
string
Proto3 optional
### UpgradeInfo​
Upgraded package info for the linkage table.
Fields
original_id
string
Proto3 optional
ID of the original package.
upgraded_id
string
Proto3 optional
ID of the upgraded package.
upgraded_version
uint64
Proto3 optional
Version of the upgraded package.
## sui/rpc/v2beta/object_reference.proto​
#### Messages
### ObjectReference​
Reference to an object.
Fields
digest
string
Proto3 optional
The digest of this object.
object_id
string
Proto3 optional
The object ID of this object.
version
uint64
Proto3 optional
The version of this object.
## sui/rpc/v2beta/balance_change.proto​
#### Messages
### BalanceChange​
The delta, or change, in balance for an address for a particular `Coin` type.
Fields
address
string
Proto3 optional
The account address that is affected by this balance change event.
amount
string
Proto3 optional
The amount or change in balance.
coin_type
string
Proto3 optional
The `Coin` type of this balance change event.
## sui/rpc/v2beta/epoch.proto​
#### Messages
### Epoch​
Fields
committee
ValidatorCommittee
Proto3 optional
The committee governing this epoch.
epoch
uint64
Proto3 optional
protocol_config
ProtocolConfig
Proto3 optional
reference_gas_price
uint64
Proto3 optional
Reference gas price denominated in MIST
## sui/rpc/v2beta/ledger_service.proto​
#### Messages
### BatchGetObjectsRequest​
Fields
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `object_id,version,digest`.
requests
GetObjectRequest
Repeated []
### BatchGetObjectsResponse​
Fields
objects
Object
Repeated []
### BatchGetTransactionsRequest​
Fields
digests
string
Repeated []
Required. The digests of the requested transactions.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `object_id,version,digest`.
### BatchGetTransactionsResponse​
Fields
transactions
ExecutedTransaction
Repeated []
### GetCheckpointRequest​
Fields
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `object_id,version,digest`.
Union field **checkpoint_id** can be only one of the following.
digest
string
The digest of the requested checkpoint.
sequence_number
uint64
The sequence number of the requested checkpoint.
### GetEpochRequest​
Fields
epoch
uint64
Proto3 optional
The requested epoch. If no epoch is provided the current epoch will be returned.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `epoch`.
### GetObjectRequest​
Fields
object_id
string
Proto3 optional
Required. The `ObjectId` of the requested object.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `object_id,version,digest`.
version
uint64
Proto3 optional
Request a specific version of the object. If no version is specified, and the object is live, then the latest version of the object is returned.
### GetServiceInfoRequest​
### GetServiceInfoResponse​
Fields
chain
string
Proto3 optional
Human-readable name of the chain that this node is on. This is intended to be a human-readable name like `mainnet`, `testnet`, and so on.
chain_id
string
Proto3 optional
The chain identifier of the chain that this node is on. The chain identifier is the digest of the genesis checkpoint, the checkpoint with sequence number 0.
checkpoint_height
uint64
Proto3 optional
Checkpoint height of the most recently executed checkpoint.
epoch
uint64
Proto3 optional
Current epoch of the node based on its highest executed checkpoint.
lowest_available_checkpoint
uint64
Proto3 optional
The lowest checkpoint for which checkpoints and transaction data are available.
lowest_available_checkpoint_objects
uint64
Proto3 optional
The lowest checkpoint for which object data is available.
server_version
string
Proto3 optional
Software version of the service. Similar to the `server` http header.
timestamp
Timestamp
Proto3 optional
Unix timestamp of the most recently executed checkpoint.
### GetTransactionRequest​
Fields
digest
string
Proto3 optional
Required. The digest of the requested transaction.
read_mask
FieldMask
Proto3 optional
Mask specifying which fields to read. If no mask is specified, defaults to `digest`.
### Services (ledger_service.proto)​
#### LedgerService
Methods
GetServiceInfoRequest -> GetServiceInfoResponse
Query the service for general information about its current state.
GetObjectRequest -> Object
BatchGetObjectsRequest -> BatchGetObjectsResponse
GetTransactionRequest -> ExecutedTransaction
BatchGetTransactionsRequest -> BatchGetTransactionsResponse
GetCheckpointRequest -> Checkpoint
GetEpochRequest -> Epoch
## sui/rpc/v2beta/executed_transaction.proto​
#### Messages
### ExecutedTransaction​
Fields
balance_changes
BalanceChange
Repeated []
checkpoint
uint64
Proto3 optional
The sequence number for the checkpoint that includes this transaction.
digest
string
Proto3 optional
The digest of this Transaction.
effects
TransactionEffects
Proto3 optional
The `TransactionEffects` for this transaction.
events
TransactionEvents
Proto3 optional
The `TransactionEvents` for this transaction. This field might be empty, even if it was explicitly requested, if the transaction didn't produce any events. `sui.types.TransactionEffects.events_digest` is populated if the transaction produced any events.
input_objects
Object
Repeated []
Set of input objects used during the execution of this transaction.
output_objects
Object
Repeated []
Set of output objects produced from the execution of this transaction.
signatures
UserSignature
Repeated []
List of user signatures that are used to authorize the execution of this transaction.
timestamp
Timestamp
Proto3 optional
The Unix timestamp of the checkpoint that includes this transaction.
transaction
Transaction
Proto3 optional
The transaction itself.
## sui/rpc/v2beta/argument.proto​
#### Messages
### Argument​
An argument to a programmable transaction command.
Fields
index
uint32
Proto3 optional
Index of an input or the result of another command based on `kind`.
kind
ArgumentKind
Proto3 optional
subresult
uint32
Proto3 optional
Used to access a nested result when `kind` is `RESULT`.
#### Enums
#### ArgumentKind
Enums
`ARGUMENT_KIND_UNKNOWN`
`GAS`
The gas coin.
`INPUT`
One of the input objects or primitive values (from `ProgrammableTransaction` inputs).
`RESULT`
The result of another command (from `ProgrammableTransaction` commands).
## sui/rpc/v2beta/checkpoint.proto​
#### Messages
### Checkpoint​
Fields
contents
CheckpointContents
Proto3 optional
The `CheckpointContents` for this checkpoint.
digest
string
Proto3 optional
The digest of this Checkpoint's CheckpointSummary.
sequence_number
uint64
Proto3 optional
The height of this checkpoint.
signature
ValidatorAggregatedSignature
Proto3 optional
An aggregated quorum signature from the validator committee that certified this checkpoint.
summary
CheckpointSummary
Proto3 optional
The `CheckpointSummary` for this checkpoint.
transactions
ExecutedTransaction
Repeated []
List of transactions included in this checkpoint.
## sui/rpc/v2beta/gas_cost_summary.proto​
#### Messages
### GasCostSummary​
Summary of gas charges.
Fields
computation_cost
uint64
Proto3 optional
Cost of computation/execution.
non_refundable_storage_fee
uint64
Proto3 optional
The fee for the rebate. The portion of the storage rebate kept by the system.
storage_cost
uint64
Proto3 optional
Storage cost, it's the sum of all storage cost for all objects created or mutated.
storage_rebate
uint64
Proto3 optional
The amount of storage cost refunded to the user for all objects deleted or mutated in the transaction.
## sui/rpc/v2beta/bcs.proto​
#### Messages
### Bcs​
`Bcs` contains an arbitrary type that is serialized using the BCS format as well as a name that identifies the type of the serialized value.
Fields
name
string
Proto3 optional
Name that identifies the type of the serialized value.
value
bytes
Proto3 optional
Bytes of a BCS serialized value.
## sui/rpc/v2beta/event.proto​
#### Messages
### Event​
An event.
Fields
contents
Bcs
Proto3 optional
BCS serialized bytes of the event.
event_type
string
Proto3 optional
The type of the event emitted.
module
string
Proto3 optional
Module name of the top-level function invoked by a `MoveCall` command that triggered this event to be emitted.
package_id
string
Proto3 optional
Package ID of the top-level function invoked by a `MoveCall` command that triggered this event to be emitted.
sender
string
Proto3 optional
Address of the account that sent the transaction where this event was emitted.
### TransactionEvents​
Events emitted during the successful execution of a transaction.
Fields
bcs
Bcs
Proto3 optional
This TransactionEvents serialized as BCS.
digest
string
Proto3 optional
The digest of this TransactionEvents.
events
Event
Repeated []
Set of events emitted by a transaction.
## sui/rpc/v2beta/checkpoint_contents.proto​
#### Messages
### CheckpointContents​
The committed to contents of a checkpoint.
Fields
bcs
Bcs
Proto3 optional
This CheckpointContents serialized as BCS.
digest
string
Proto3 optional
The digest of this CheckpointContents.
transactions
CheckpointedTransactionInfo
Repeated []
Set of transactions committed to in this checkpoint.
version
int32
Proto3 optional
Version of this CheckpointContents
### CheckpointedTransactionInfo​
Transaction information committed to in a checkpoint.
Fields
effects
string
Proto3 optional
Digest of the effects.
signatures
UserSignature
Repeated []
Set of user signatures that authorized the transaction.
transaction
string
Proto3 optional
Digest of the transaction.
## sui/rpc/v2beta/protocol_config.proto​
#### Messages
### ProtocolConfig​
Fields
attributes
AttributesEntry
Repeated []
feature_flags
FeatureFlagsEntry
Repeated []
protocol_version
uint64
Proto3 optional
### AttributesEntry​
Fields
key
string
value
string
### FeatureFlagsEntry​
Fields
key
string
value
bool
## sui/rpc/v2beta/signature_scheme.proto​
#### Enums
#### SignatureScheme
Flag use to disambiguate the signature schemes supported by Sui. Note: the enum values defined by this proto message exactly match their expected BCS serialized values when serialized as a u8. See enum.SignatureScheme for more information about signature schemes.
Enums
`ED25519`
`SECP256K1`
`SECP256R1`
`MULTISIG`
`BLS12381`
`ZKLOGIN`
`PASSKEY`
## sui/rpc/v2beta/signature.proto​
#### Messages
### CircomG1​
A G1 point.
Fields
e0
string
Proto3 optional
base10 encoded Bn254FieldElement
e1
string
Proto3 optional
base10 encoded Bn254FieldElement
e2
string
Proto3 optional
base10 encoded Bn254FieldElement
### CircomG2​
A G2 point.
Fields
e00
string
Proto3 optional
base10 encoded Bn254FieldElement
e01
string
Proto3 optional
base10 encoded Bn254FieldElement
e10
string
Proto3 optional
base10 encoded Bn254FieldElement
e11
string
Proto3 optional
base10 encoded Bn254FieldElement
e20
string
Proto3 optional
base10 encoded Bn254FieldElement
e21
string
Proto3 optional
base10 encoded Bn254FieldElement
### MultisigAggregatedSignature​
Aggregated signature from members of a multisig committee.
Fields
bitmap
uint32
Proto3 optional
Bitmap indicating which committee members contributed to the signature.
committee
MultisigCommittee
Proto3 optional
The committee to use to validate this signature.
legacy_bitmap
uint32
Repeated []
If present, means this signature's on-chain format uses the old legacy multisig format.
signatures
MultisigMemberSignature
Repeated []
The plain signatures encoded with signature scheme. The signatures must be in the same order as they are listed in the committee.
### MultisigCommittee​
A multisig committee.
Fields
members
MultisigMember
Repeated []
A list of committee members and their corresponding weight.
threshold
uint32
Proto3 optional
The threshold of signatures needed to validate a signature from this committee.
### MultisigMember​
A member in a multisig committee.
Fields
public_key
MultisigMemberPublicKey
Proto3 optional
The public key of the committee member.
weight
uint32
Proto3 optional
The weight of this member's signature.
### MultisigMemberPublicKey​
Set of valid public keys for multisig committee members.
Fields
public_key
bytes
Proto3 optional
Public key bytes if scheme is ed25519 | secp256k1 | secp256r1.
scheme
SignatureScheme
Proto3 optional
The signature scheme of this public key.
zklogin
ZkLoginPublicIdentifier
Proto3 optional
A zklogin public identifier if scheme is zklogin.
### MultisigMemberSignature​
A signature from a member of a multisig committee.
Fields
scheme
SignatureScheme
Proto3 optional
The signature scheme of this signature.
signature
bytes
Proto3 optional
Signature bytes if scheme is ed25519 | secp256k1 | secp256r1.
zklogin
ZkLoginAuthenticator
Proto3 optional
The zklogin authenticator if scheme is `ZKLOGIN`.
### PasskeyAuthenticator​
A passkey authenticator.
See struct.PasskeyAuthenticator for more information on the requirements on the shape of the `client_data_json` field.
Fields
authenticator_data
bytes
Proto3 optional
Opaque authenticator data for this passkey signature. See Authenticator Data for more information on this field.
client_data_json
string
Proto3 optional
Structured, unparsed, JSON for this passkey signature. See CollectedClientData for more information on this field.
signature
UserSignature
Proto3 optional
A secp256r1 signature.
### UserSignature​
A signature from a user.
Fields
bcs
Bcs
Proto3 optional
This signature serialized as as BCS. When provided as input this will support both the form that is length prefixed as well as not length prefixed.
multisig
MultisigAggregatedSignature
Proto3 optional
The multisig aggregated signature if scheme is `MULTISIG`.
passkey
PasskeyAuthenticator
Proto3 optional
The passkey authenticator if scheme is `PASSKEY`.
public_key
bytes
Proto3 optional
Public key bytes if scheme is ed25519 | secp256k1 | secp256r1.
scheme
SignatureScheme
Proto3 optional
The signature scheme of this signature.
signature
bytes
Proto3 optional
Signature bytes if scheme is ed25519 | secp256k1 | secp256r1.
zklogin
ZkLoginAuthenticator
Proto3 optional
The zklogin authenticator if scheme is `ZKLOGIN`.
### ValidatorAggregatedSignature​
An aggregated signature from multiple validators.
Fields
bitmap
uint32
Repeated []
Bitmap indicating which members of the committee contributed to this signature.
epoch
uint64
Proto3 optional
The epoch when this signature was produced. This can be used to lookup the `ValidatorCommittee` from this epoch to verify this signature.
signature
bytes
Proto3 optional
The 48-byte Bls12381 aggregated signature.
### ValidatorCommittee​
The validator set for a particular epoch.
Fields
epoch
uint64
Proto3 optional
The epoch where this committee governs.
members
ValidatorCommitteeMember
Repeated []
The committee members.
### ValidatorCommitteeMember​
A member of a validator committee.
Fields
public_key
bytes
Proto3 optional
The 96-byte Bls12381 public key for this validator.
stake
uint64
Proto3 optional
Stake weight this validator possesses.
### ZkLoginAuthenticator​
A zklogin authenticator.
Fields
inputs
ZkLoginInputs
Proto3 optional
Zklogin proof and inputs required to perform proof verification.
max_epoch
uint64
Proto3 optional
Maximum epoch for which the proof is valid.
signature
UserSignature
Proto3 optional
User signature with the public key attested to by the provided proof.
### ZkLoginClaim​
A claim of the iss in a zklogin proof.
Fields
index_mod_4
uint32
Proto3 optional
value
string
Proto3 optional
### ZkLoginInputs​
A zklogin groth16 proof and the required inputs to perform proof verification.
Fields
address_seed
string
Proto3 optional
base10 encoded Bn254FieldElement
header_base64
string
Proto3 optional
iss_base64_details
ZkLoginClaim
Proto3 optional
proof_points
ZkLoginProof
Proto3 optional
### ZkLoginProof​
A zklogin groth16 proof.
Fields
a
CircomG1
Proto3 optional
b
CircomG2
Proto3 optional
c
CircomG1
Proto3 optional
### ZkLoginPublicIdentifier​
Public key equivalent for zklogin authenticators.
Fields
address_seed
string
Proto3 optional
base10 encoded Bn254FieldElement
iss
string
Proto3 optional
## sui/rpc/v2alpha/live_data_service.proto​
#### Messages
### CoinMetadata​
Metadata for a coin type
Fields
decimals
uint32
Proto3 optional
Number of decimal places to coin uses.
description
string
Proto3 optional
Description of the token
icon_url
string
Proto3 optional
URL for the token logo
id
string
Proto3 optional
ObjectId of the `0x2::coin::CoinMetadata` object.
name
string
Proto3 optional
Name for the token
symbol
string
Proto3 optional
Symbol for the token
### CoinTreasury​
Information about a coin type's `0x2::coin::TreasuryCap` and its total available supply
Fields
id
string
Proto3 optional
ObjectId of the `0x2::coin::TreasuryCap` object.
total_supply
uint64
Proto3 optional
Total available supply for this coin type.
### DynamicField​
Fields
dynamic_object_id
string
Proto3 optional
The ObjectId of the child object when a child is a dynamic object field. The presence or absence of this field can be used to determine if a child is a dynamic field or a dynamic child object
field_id
string
Proto3 optional
Required. ObjectId of this dynamic field.
name_type
string
Proto3 optional
Required. The type of the dynamic field "name"
name_value
bytes
Proto3 optional
Required. The serialized move value of "name"
parent
string
Proto3 optional
Required. ObjectId of this dynamic field's parent.
### GetCoinInfoRequest​
Request message for `NodeService.GetCoinInfo`.
Fields
coin_type
string
Proto3 optional
The coin type to request information about
### GetCoinInfoResponse​
Response message for `NodeService.GetCoinInfo`.
Fields
coin_type
string
Proto3 optional
Required. The coin type.
metadata
CoinMetadata
Proto3 optional
This field will be populated with information about this coin type's `0x2::coin::CoinMetadata` if it exists and has not been wrapped.
treasury
CoinTreasury
Proto3 optional
This field will be populated with information about this coin type's `0x2::coin::TreasuryCap` if it exists and has not been wrapped.
### ListDynamicFieldsRequest​
Request message for `NodeService.ListDynamicFields`
Fields
page_size
uint32
Proto3 optional
The maximum number of dynamic fields to return. The service may return fewer than this value. If unspecified, at most `50` entries will be returned. The maximum value is `1000`; values above `1000` will be coerced to `1000`.
page_token
bytes
Proto3 optional
A page token, received from a previous `ListDynamicFields` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListDynamicFields` must match the call that provided the page token.
parent
string
Proto3 optional
Required. The `UID` of the parent, which owns the collections of dynamic fields.
### ListDynamicFieldsResponse​
Response message for `NodeService.ListDynamicFields`
Fields
dynamic_fields
DynamicField
Repeated []
Page of dynamic fields owned by the specified parent.
next_page_token
bytes
Proto3 optional
A token, which can be sent as `page_token` to retrieve the next page. If this field is omitted, there are no subsequent pages.
### ListOwnedObjectsRequest​
Fields
owner
string
Proto3 optional
Required. The address of the account that owns the objects.
page_size
uint32
Proto3 optional
The maximum number of entries return. The service may return fewer than this value. If unspecified, at most `50` entries will be returned. The maximum value is `1000`; values above `1000` will be coerced to `1000`.
page_token
bytes
Proto3 optional
A page token, received from a previous `ListOwnedObjects` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListOwnedObjects` must match the call that provided the page token.
### ListOwnedObjectsResponse​
Fields
next_page_token
bytes
Proto3 optional
A token, which can be sent as `page_token` to retrieve the next page. If this field is omitted, there are no subsequent pages.
objects
OwnedObject
Repeated []
Page of dynamic fields owned by the specified parent.
### OwnedObject​
Fields
object_id
string
Proto3 optional
object_type
string
Proto3 optional
owner
string
Proto3 optional
version
uint64
Proto3 optional
### RegulatedCoinMetadata​
Information about a regulated coin, which indicates that it makes use of the transfer deny list.
Fields
coin_metadata_object
string
Proto3 optional
The ID of the coin's `CoinMetadata` object.
deny_cap_object
string
Proto3 optional
The ID of the coin's `DenyCap` object.
id
string
Proto3 optional
ObjectId of the `0x2::coin::RegulatedCoinMetadata` object.
### ResolveTransactionRequest​
Fields
read_mask
FieldMask
Proto3 optional
unresolved_transaction
string
Proto3 optional
optional sui.rpc.v2beta.Transaction unresolved_transaction = 1; TODO FIX TYPE Json unresolved transaction type
### ResolveTransactionResponse​
Fields
simulation
SimulateTransactionResponse
Proto3 optional
transaction
Transaction
Proto3 optional
### SimulateTransactionRequest​
Fields
read_mask
FieldMask
Proto3 optional
transaction
Transaction
Proto3 optional
### SimulateTransactionResponse​
Fields
transaction
ExecutedTransaction
Proto3 optional
### Services (live_data_service.proto)​
#### LiveDataService
Methods
ListDynamicFieldsRequest -> ListDynamicFieldsResponse
ListOwnedObjectsRequest -> ListOwnedObjectsResponse
GetCoinInfoRequest -> GetCoinInfoResponse
get balance? list balance?
SimulateTransactionRequest -> SimulateTransactionResponse
ResolveTransactionRequest -> ResolveTransactionResponse
ViewFunction?
## sui/rpc/v2alpha/subscription_service.proto​
#### Messages
### SubscribeCheckpointsRequest​
Request message for SubscriptionService.SubscribeCheckpoints
Fields
read_mask
FieldMask
Proto3 optional
Optional. Mask for specifiying which parts of the SubscribeCheckpointsResponse should be returned.
### SubscribeCheckpointsResponse​
Response message for SubscriptionService.SubscribeCheckpoints
Fields
checkpoint
Checkpoint
Proto3 optional
The requested data for this checkpoint
cursor
uint64
Proto3 optional
Required. The checkpoint sequence number and value of the current cursor into the checkpoint stream
### Services (subscription_service.proto)​
#### SubscriptionService
Methods
SubscribeCheckpointsRequest -> SubscribeCheckpointsResponse
Subscribe to the stream of checkpoints. This API provides a subscription to the checkpoint stream for the Sui blockchain. When a subscription is initialized the stream will begin with the latest executed checkpoint as seen by the server. Responses are gaurenteed to return checkpoints in-order and without gaps. This enables clients to know exactly the last checkpoint they have processed and in the event the subscription terminates (either by the client/server or by the connection breaking), clients will be able to reinitailize a subscription and then leverage other APIs in order to request data for the checkpoints they missed.
## google/rpc/status.proto​
#### Messages
### Status​
The `Status` type defines a logical error model that is suitable for different programming environments, including REST APIs and RPC APIs. It is used by gRPC. Each `Status` message contains three pieces of data: error code, error message, and error details.
You can find out more about this error model and how to work with it in the API Design Guide.
Fields
code
int32
The status code, which should be an enum value of [google.rpc.Code][google.rpc.Code].
details
Any
Repeated []
A list of messages that carry the error details. There is a common set of message types for APIs to use.
message
string
A developer-facing error message, which should be in English. Any user-facing error message should be localized and sent in the [google.rpc.Status.details][google.rpc.Status.details] field, or localized by the client.
## google/rpc/error_details.proto​
#### Messages
### BadRequest​
Describes violations in a client request. This error type focuses on the syntactic aspects of the request.
Fields
field_violations
FieldViolation
Repeated []
Describes all violations in a client request.
### FieldViolation​
A message type used to describe a single bad request field.
Fields
description
string
A description of why the request element is bad.
field
string
A path that leads to a field in the request body. The value will be a sequence of dot-separated identifiers that identify a protocol buffer field. Consider the following: `text,json message CreateContactRequest {   message EmailAddress {     enum Type {       TYPE_UNSPECIFIED = 0;       HOME = 1;       WORK = 2;     }      optional string email = 1;     repeated EmailType type = 2;   }    string full_name = 1;   repeated EmailAddress email_addresses = 2; } ` In this example, in proto `field` could take one of the following values: * `full_name` for a violation in the `full_name` value * `email_addresses[1].email` for a violation in the `email` field of the first `email_addresses` message * `email_addresses[3].type[2]` for a violation in the second `type` value in the third `email_addresses` message. In JSON, the same values are represented as: * `fullName` for a violation in the `fullName` value * `emailAddresses[1].email` for a violation in the `email` field of the first `emailAddresses` message * `emailAddresses[3].type[2]` for a violation in the second `type` value in the third `emailAddresses` message.
localized_message
LocalizedMessage
Provides a localized error message for field-level errors that is safe to return to the API consumer.
reason
string
The reason of the field-level error. This is a constant value that identifies the proximate cause of the field-level error. It should uniquely identify the type of the FieldViolation within the scope of the google.rpc.ErrorInfo.domain. This should be at most 63 characters and match a regular expression of `[A-Z][A-Z0-9_]+[A-Z0-9]`, which represents UPPER_SNAKE_CASE.
### DebugInfo​
Describes additional debugging info.
Fields
detail
string
Additional debugging information provided by the server.
stack_entries
string
Repeated []
The stack trace entries indicating where the error occurred.
### ErrorInfo​
Describes the cause of the error with structured details.
Example of an error when contacting the "pubsub.googleapis.com" API when it is not enabled:
```
{ "reason": "API_DISABLED"  
  "domain": "googleapis.com"  
  "metadata": {  
    "resource": "projects/123",  
    "service": "pubsub.googleapis.com"  
  }  
}  

```

This response indicates that the pubsub.googleapis.com API is not enabled.
Example of an error that is returned when attempting to create a Spanner instance in a region that is out of stock:
```
{ "reason": "STOCKOUT"  
  "domain": "spanner.googleapis.com",  
  "metadata": {  
    "availableRegions": "us-central1,us-east2"  
  }  
}  

```

Fields
domain
string
The logical grouping to which the "reason" belongs. The error domain is typically the registered service name of the tool or product that generates the error. Example: "pubsub.googleapis.com". If the error is generated by some common infrastructure, the error domain must be a globally unique value that identifies the infrastructure. For Google API infrastructure, the error domain is "googleapis.com".
metadata
MetadataEntry
Repeated []
Additional structured details about this error. Keys must match a regular expression of `[a-z][a-zA-Z0-9-_]+` but should ideally be lowerCamelCase. Also, they must be limited to 64 characters in length. When identifying the current value of an exceeded limit, the units should be contained in the key, not the value. For example, rather than `{"instanceLimit": "100/request"}`, should be returned as, `{"instanceLimitPerRequest": "100"}`, if the client exceeds the number of instances that can be created in a single (batch) request.
reason
string
The reason of the error. This is a constant value that identifies the proximate cause of the error. Error reasons are unique within a particular domain of errors. This should be at most 63 characters and match a regular expression of `[A-Z][A-Z0-9_]+[A-Z0-9]`, which represents UPPER_SNAKE_CASE.
### MetadataEntry​
Fields
key
string
value
string
### Help​
Provides links to documentation or for performing an out of band action.
For example, if a quota check failed with an error indicating the calling project hasn't enabled the accessed service, this can contain a URL pointing directly to the right place in the developer console to flip the bit.
Fields
links
Link
Repeated []
URL(s) pointing to additional information on handling the current error.
### Link​
Describes a URL link.
Fields
description
string
Describes what the link offers.
url
string
The URL of the link.
### LocalizedMessage​
Provides a localized error message that is safe to return to the user which can be attached to an RPC error.
Fields
locale
string
The locale used following the specification defined at https://www.rfc-editor.org/rfc/bcp/bcp47.txt. Examples are: "en-US", "fr-CH", "es-MX"
message
string
The localized error message in the above locale.
### PreconditionFailure​
Describes what preconditions have failed.
For example, if an RPC failed because it required the Terms of Service to be acknowledged, it could list the terms of service violation in the PreconditionFailure message.
Fields
violations
Violation
Repeated []
Describes all precondition violations.
### Violation​
A message type used to describe a single precondition failure.
Fields
description
string
A description of how the precondition failed. Developers can use this description to understand how to fix the failure. For example: "Terms of service not accepted".
subject
string
The subject, relative to the type, that failed. For example, "google.com/cloud" relative to the "TOS" type would indicate which terms of service is being referenced.
type
string
The type of PreconditionFailure. We recommend using a service-specific enum type to define the supported precondition violation subjects. For example, "TOS" for "Terms of Service violation".
### QuotaFailure​
Describes how a quota check failed.
For example if a daily limit was exceeded for the calling project, a service could respond with a QuotaFailure detail containing the project id and the description of the quota limit that was exceeded. If the calling project hasn't enabled the service in the developer console, then a service could respond with the project id and set `service_disabled` to true.
Also see RetryInfo and Help types for other details about handling a quota failure.
Fields
violations
Violation
Repeated []
Describes all quota violations.
### Violation​
A message type used to describe a single quota violation. For example, a daily quota or a custom quota that was exceeded.
Fields
description
string
A description of how the quota check failed. Clients can use this description to find more about the quota configuration in the service's public documentation, or find the relevant quota limit to adjust through developer console. For example: "Service disabled" or "Daily Limit for read operations exceeded".
subject
string
The subject on which the quota check failed. For example, `clientip:<ip address of client>` or `project:<Google developer project id>`.
### RequestInfo​
Contains metadata about the request that clients can attach when filing a bug or providing other forms of feedback.
Fields
request_id
string
An opaque string that should only be interpreted by the service generating it. For example, it can be used to identify requests in the service's logs.
serving_data
string
Any data that was used to serve this request. For example, an encrypted stack trace that can be sent back to the service provider for debugging.
### ResourceInfo​
Describes the resource that is being accessed.
Fields
description
string
Describes what error is encountered when accessing this resource. For example, updating a cloud project may require the `writer` permission on the developer console project.
owner
string
The owner of the resource (optional). For example, `user:<owner email>` or `project:<Google developer project id>`.
resource_name
string
The name of the resource being accessed. For example, a shared calendar name: "example.com_4fghdhgsrgh@group.calendar.google.com", if the current error is [google.rpc.Code.PERMISSION_DENIED][google.rpc.Code.PERMISSION_DENIED].
resource_type
string
A name for the type of resource being accessed, e.g. "sql table", "cloud storage bucket", "file", "Google calendar"; or the type URL of the resource: e.g. "type.googleapis.com/google.pubsub.v1.Topic".
### RetryInfo​
Describes when the clients can retry a failed request. Clients could ignore the recommendation here or retry when this information is missing from error responses.
It's always recommended that clients should use exponential backoff when retrying.
Clients should wait until `retry_delay` amount of time has passed since receiving the error response before retrying. If retrying requests also fail, clients should use an exponential backoff scheme to gradually increase the delay between retries based on `retry_delay`, until either a maximum number of retries have been reached or a maximum retry delay cap has been reached.
Fields
retry_delay
Duration
Clients should wait at least this long between retrying the same request.
## google/protobuf/timestamp.proto​
#### Messages
### Timestamp​
A Timestamp represents a point in time independent of any time zone or calendar, represented as seconds and fractions of seconds at nanosecond resolution in UTC Epoch time. It is encoded using the Proleptic Gregorian Calendar which extends the Gregorian calendar backwards to year one. It is encoded assuming all minutes are 60 seconds long, i.e. leap seconds are "smeared" so that no leap second table is needed for interpretation. Range is from `0001-01-01T00:00:00Z` to `9999-12-31T23:59:59.999999999Z`. Restricting to that range ensures that conversion to and from RFC 3339 date strings is possible. See https://www.ietf.org/rfc/rfc3339.txt.
### Examples​
Example 1: Compute Timestamp from POSIX `time()`.
```
Timestamp timestamp;  
timestamp.set_seconds(time(NULL));  
timestamp.set_nanos(0);  

```

Example 2: Compute Timestamp from POSIX `gettimeofday()`.
```
struct timeval tv;  
gettimeofday(&tv, NULL);  
  
Timestamp timestamp;  
timestamp.set_seconds(tv.tv_sec);  
timestamp.set_nanos(tv.tv_usec * 1000);  

```

Example 3: Compute Timestamp from Win32 `GetSystemTimeAsFileTime()`.
```
FILETIME ft;  
GetSystemTimeAsFileTime(&ft);  
UINT64 ticks = (((UINT64)ft.dwHighDateTime) &#lt;&#lt; 32) | ft.dwLowDateTime;  
  
// A Windows tick is 100 nanoseconds. Windows epoch 1601-01-01T00:00:00Z  
// is 11644473600 seconds before Unix epoch 1970-01-01T00:00:00Z.  
Timestamp timestamp;  
timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL));  
timestamp.set_nanos((INT32) ((ticks % 10000000) * 100)); //  

```

Example 4: Compute Timestamp from Java `System.currentTimeMillis()`.
```
long millis = System.currentTimeMillis();  
  
Timestamp timestamp = Timestamp.newBuilder().setSeconds(millis / 1000)  
    .setNanos((int) ((millis % 1000) * 1000000)).build();  
  

```

Example 5: Compute Timestamp from current time in Python.
```
timestamp = Timestamp()  
timestamp.GetCurrentTime()  

```

### JSON Mapping​
In JSON format, the `Timestamp` type is encoded as a string in the RFC 3339 format. That is, the format is `{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z` where `{year}` is always expressed using four digits while `{month}`, `{day}`, `{hour}`, `{min}`, and `{sec}` are zero-padded to two digits each. The fractional seconds, which can go up to 9 digits (so up to 1 nanosecond resolution), are optional. The "Z" suffix indicates the timezone ("UTC"); the timezone is required, though only UTC (as indicated by "Z") is presently supported.
For example, `2017-01-15T01:30:15.01Z` encodes 15.01 seconds past 01:30 UTC on January 15, 2017.
In JavaScript, you can convert a `Date` object to this format using the standard toISOString() method. In Python, you can convert a standard `datetime.datetime` object to this format using `strftime` with the time format spec `%Y-%m-%dT%H:%M:%S.%fZ`. Likewise, in Java, you can use the Joda Time's `ISODateTimeFormat.dateTime()` to obtain a formatter capable of generating timestamps in this format.
Fields
nanos
int32
Non-negative fractions of a second at nanosecond resolution. Negative second values with fractions must still have non-negative nano values that count forward in time. Must be from 0 to 999,999,999 inclusive.
seconds
int64
Represents seconds of UTC time since Unix epoch `1970-01-01T00:00:00Z`. Must be from `0001-01-01T00:00:00Z` to `9999-12-31T23:59:59Z` inclusive.
## google/protobuf/field_mask.proto​
#### Messages
### FieldMask​
`FieldMask` represents a set of symbolic field paths, for example:
paths: "f.a" paths: "f.b.d"
Here `f` represents a field in some root message, `a` and `b` fields in the message found in `f`, and `d` a field found in the message in `f.b`.
Field masks are used to specify a subset of fields that should be returned by a get operation or modified by an update operation. Field masks also have a custom JSON encoding (see below).
### Field Masks in Projections​
When used in the context of a projection, a response message or sub-message is filtered by the API to only contain those fields as specified in the mask. For example, if the mask in the previous example is applied to a response message as follows:
f { a : 22 b { d : 1 x : 2 } y : 13 } z: 8
The result will not contain specific values for fields x,y and z (their value will be set to the default, and omitted in proto text output):
f { a : 22 b { d : 1 } }
A repeated field is not allowed except at the last position of a paths string.
If a FieldMask object is not present in a get operation, the operation applies to all fields (as if a FieldMask of all fields had been specified).
Note that a field mask does not necessarily apply to the top-level response message. In case of a REST get operation, the field mask applies directly to the response, but in case of a REST list operation, the mask instead applies to each individual message in the returned resource list. In case of a REST custom method, other definitions may be used. Where the mask applies will be clearly documented together with its declaration in the API. In any case, the effect on the returned resource/resources is required behavior for APIs.
### Field Masks in Update Operations​
A field mask in update operations specifies which fields of the targeted resource are going to be updated. The API is required to only change the values of the fields as specified in the mask and leave the others untouched. If a resource is passed in to describe the updated values, the API ignores the values of all fields not covered by the mask.
If a repeated field is specified for an update operation, new values will be appended to the existing repeated field in the target resource. Note that a repeated field is only allowed in the last position of a `paths` string.
If a sub-message is specified in the last position of the field mask for an update operation, then new value will be merged into the existing sub-message in the target resource.
For example, given the target message:
f { b { d: 1 x: 2 } c: [1] }
And an update message:
f { b { d: 10 } c: [2] }
then if the field mask is:
paths: ["f.b", "f.c"]
then the result will be:
f { b { d: 10 x: 2 } c: [1, 2] }
An implementation may provide options to override this default behavior for repeated and message fields.
In order to reset a field's value to the default, the field must be in the mask and set to the default value in the provided resource. Hence, in order to reset all fields of a resource, provide a default instance of the resource and set all fields in the mask, or do not provide a mask as described below.
If a field mask is not present on update, the operation applies to all fields (as if a field mask of all fields has been specified). Note that in the presence of schema evolution, this may mean that fields the client does not know and has therefore not filled into the request will be reset to their default. If this is unwanted behavior, a specific service may require a client to always specify a field mask, producing an error if not.
As with get operations, the location of the resource which describes the updated values in the request message depends on the operation kind. In any case, the effect of the field mask is required to be honored by the API.
### Considerations for HTTP REST​
The HTTP kind of an update operation which uses a field mask must be set to PATCH instead of PUT in order to satisfy HTTP semantics (PUT must only be used for full updates).
### JSON Encoding of Field Masks​
In JSON, a field mask is encoded as a single string where paths are separated by a comma. Fields name in each path are converted to/from lower-camel naming conventions.
As an example, consider the following message declarations:
message Profile { User user = 1; Photo photo = 2; } message User { string display_name = 1; string address = 2; }
In proto a field mask for `Profile` may look as such:
mask { paths: "user.display_name" paths: "photo" }
In JSON, the same mask is represented as below:
{ mask: "user.displayName,photo" }
### Field Masks and Oneof Fields​
Field masks treat fields in oneofs just as regular fields. Consider the following message:
message SampleMessage { oneof test_oneof { string name = 4; SubMessage sub_message = 9; } }
The field mask can be:
mask { paths: "name" }
Or:
mask { paths: "sub_message" }
Note that oneof type names ("test_oneof" in this case) cannot be used in paths.
### Field Mask Verification​
The implementation of any API method which has a FieldMask type field in the request should verify the included field paths, and return an `INVALID_ARGUMENT` error if any path is unmappable.
Fields
paths
string
Repeated []
The set of field mask paths.
## google/protobuf/duration.proto​
#### Messages
### Duration​
A Duration represents a signed, fixed-length span of time represented as a count of seconds and fractions of seconds at nanosecond resolution. It is independent of any calendar and concepts like "day" or "month". It is related to Timestamp in that the difference between two Timestamp values is a Duration and it can be added or subtracted from a Timestamp. Range is approximately +-10,000 years.
### Examples​
Example 1: Compute Duration from two Timestamps in pseudo code.
Timestamp start = ...; Timestamp end = ...; Duration duration = ...;
duration.seconds = end.seconds - start.seconds; duration.nanos = end.nanos - start.nanos;
if (duration.seconds &#lt; 0 && duration.nanos > 0) { duration.seconds += 1; duration.nanos -= 1000000000; } else if (duration.seconds > 0 && duration.nanos &#lt; 0) { duration.seconds -= 1; duration.nanos += 1000000000; }
Example 2: Compute Timestamp from Timestamp + Duration in pseudo code.
Timestamp start = ...; Duration duration = ...; Timestamp end = ...;
end.seconds = start.seconds + duration.seconds; end.nanos = start.nanos + duration.nanos;
if (end.nanos &#lt; 0) { end.seconds -= 1; end.nanos += 1000000000; } else if (end.nanos >= 1000000000) { end.seconds += 1; end.nanos -= 1000000000; }
Example 3: Compute Duration from datetime.timedelta in Python.
td = datetime.timedelta(days=3, minutes=10) duration = Duration() duration.FromTimedelta(td)
### JSON Mapping​
In JSON format, the Duration type is encoded as a string rather than an object, where the string ends in the suffix "s" (indicating seconds) and is preceded by the number of seconds, with nanoseconds expressed as fractional seconds. For example, 3 seconds with 0 nanoseconds should be encoded in JSON format as "3s", while 3 seconds and 1 nanosecond should be expressed in JSON format as "3.000000001s", and 3 seconds and 1 microsecond should be expressed in JSON format as "3.000001s".
Fields
nanos
int32
Signed fractions of a second at nanosecond resolution of the span of time. Durations less than one second are represented with a 0 `seconds` field and a positive or negative `nanos` field. For durations of one second or more, a non-zero value for the `nanos` field must be of the same sign as the `seconds` field. Must be from -999,999,999 to +999,999,999 inclusive.
seconds
int64
Signed seconds of the span of time. Must be from -315,576,000,000 to +315,576,000,000 inclusive. Note: these bounds are computed from: 60 sec/min * 60 min/hr * 24 hr/day * 365.25 days/year * 10000 years
## google/protobuf/any.proto​
#### Messages
### Any​
`Any` contains an arbitrary serialized protocol buffer message along with a URL that describes the type of the serialized message.
Protobuf library provides support to pack/unpack Any values in the form of utility functions or additional generated methods of the Any type.
Example 1: Pack and unpack a message in C++.
Foo foo = ...; Any any; any.PackFrom(foo); ... if (any.UnpackTo(&foo)) { ... }
Example 2: Pack and unpack a message in Java.
Foo foo = ...; Any any = Any.pack(foo); ... if (any.is(Foo.class)) { foo = any.unpack(Foo.class); } // or ... if (any.isSameTypeAs(Foo.getDefaultInstance())) { foo = any.unpack(Foo.getDefaultInstance()); }
Example 3: Pack and unpack a message in Python.
foo = Foo(...) any = Any() any.Pack(foo) ... if any.Is(Foo.DESCRIPTOR): any.Unpack(foo) ...
Example 4: Pack and unpack a message in Go
foo := &pb.Foo{...} any, err := anypb.New(foo) if err != nil { ... } ... foo := &pb.Foo{} if err := any.UnmarshalTo(foo); err != nil { ... }
The pack methods provided by protobuf library will by default use 'type.googleapis.com/full.type.name' as the type URL and the unpack methods only use the fully qualified type name after the last '/' in the type URL, for example "foo.bar.com/x/y.z" will yield type name "y.z".
# JSON
The JSON representation of an `Any` value uses the regular representation of the deserialized, embedded message, with an additional field `@type` which contains the type URL. Example:
package google.profile; message Person { string first_name = 1; string last_name = 2; }
{ "@type": "type.googleapis.com/google.profile.Person", "firstName": &#lt;string>, "lastName": &#lt;string> }
If the embedded message type is well-known and has a custom JSON representation, that representation will be embedded adding a field `value` which holds the custom JSON in addition to the `@type` field. Example (for message [google.protobuf.Duration][]):
{ "@type": "type.googleapis.com/google.protobuf.Duration", "value": "1.212s" }
Fields
type_url
string
A URL/resource name that uniquely identifies the type of the serialized protocol buffer message. This string must contain at least one "/" character. The last segment of the URL's path must represent the fully qualified name of the type (as in `path/google.protobuf.Duration`). The name should be in a canonical form (e.g., leading "." is not accepted). In practice, teams usually precompile into the binary all types that they expect it to use in the context of Any. However, for URLs which use the scheme `http`, `https`, or no scheme, one can optionally set up a type server that maps type URLs to message definitions as follows: * If no scheme is provided, `https` is assumed. * An HTTP GET on the URL must yield a [google.protobuf.Type][] value in binary format, or produce an error. * Applications are allowed to cache lookup results based on the URL, or have them precompiled into a binary to avoid any lookup. Therefore, binary compatibility needs to be preserved on changes to types. (Use versioned type names to manage breaking changes.) Note: this functionality is not currently available in the official protobuf release, and it is not used for type URLs beginning with type.googleapis.com. As of May 2023, there are no widely used type server implementations and no plans to implement one. Schemes other than `http`, `https` (or the empty scheme) might be used with implementation specific semantics.
value
bytes
Must be a valid serialized protocol buffer of the above specified type.
## google/protobuf/empty.proto​
#### Messages
### Empty​
A generic empty message that you can re-use to avoid defining duplicated empty messages in your APIs. A typical example is to use it as the request or the response type of an API method. For instance:
```
service Foo {  
  rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);  
}  

```

## Scalar Value Types​
### double​
C++
double
C#
double
Go
float64
Java
double
PHP
float
Python
float
Ruby
Float
### float​
C++
float
C#
float
Go
float32
Java
float
PHP
float
Python
float
Ruby
Float
### int32​
Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead.
C++
int32
C#
int
Go
int32
Java
int
PHP
integer
Python
int
Ruby
Bignum or Fixnum (as required)
### int64​
Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead.
C++
int64
C#
long
Go
int64
Java
long
PHP
integer/string
Python
int/long
Ruby
Bignum
### uint32​
Uses variable-length encoding.
C++
uint32
C#
uint
Go
uint32
Java
int
PHP
integer
Python
int/long
Ruby
Bignum or Fixnum (as required)
### uint64​
Uses variable-length encoding.
C++
uint64
C#
ulong
Go
uint64
Java
long
PHP
integer/string
Python
int/long
Ruby
Bignum or Fixnum (as required)
### sint32​
Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s.
C++
int32
C#
int
Go
int32
Java
int
PHP
integer
Python
int
Ruby
Bignum or Fixnum (as required)
### sint64​
Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s.
C++
int64
C#
long
Go
int64
Java
long
PHP
integer/string
Python
int/long
Ruby
Bignum
### fixed32​
Always four bytes. More efficient than uint32 if values are often greater than 2^28.
C++
uint32
C#
uint
Go
uint32
Java
int
PHP
integer
Python
int
Ruby
Bignum or Fixnum (as required)
### fixed64​
Always eight bytes. More efficient than uint64 if values are often greater than 2^56.
C++
uint64
C#
ulong
Go
uint64
Java
long
PHP
integer/string
Python
int/long
Ruby
Bignum
### sfixed32​
Always four bytes.
C++
int32
C#
int
Go
int32
Java
int
PHP
integer
Python
int
Ruby
Bignum or Fixnum (as required)
### sfixed64​
Always eight bytes.
C++
int64
C#
long
Go
int64
Java
long
PHP
integer/string
Python
int/long
Ruby
Bignum
### bool​
C++
bool
C#
bool
Go
bool
Java
boolean
PHP
boolean
Python
boolean
Ruby
TrueClass/FalseClass
### string​
A string must always contain UTF-8 encoded or 7-bit ASCII text.
C++
string
C#
string
Go
string
Java
String
PHP
string
Python
str/unicode
Ruby
String (UTF-8)
### bytes​
May contain any arbitrary sequence of bytes.
C++
string
C#
ByteString
Go
[]byte
Java
ByteString
PHP
string
Python
str
Ruby
String (ASCII-8BIT)
Previous
UnchangedSharedObject
Next
RPC Best Practices
  * sui/types/types.proto
    * Use of `optional`
    * ActiveJwk
    * Address
    * AddressDeniedForCoinError
    * Argument
    * AuthenticatorStateExpire
    * AuthenticatorStateUpdate
    * Bcs
    * Bn254FieldElement
    * CancelledTransaction
    * CancelledTransactions
    * ChangeEpoch
    * ChangedObject
    * CheckpointCommitment
    * CheckpointContents
    * V1
    * CheckpointSummary
    * CheckpointedTransactionInfo
    * CircomG1
    * CircomG2
    * Command
    * CommandArgumentError
    * CongestedObjectsError
    * ConsensusCommitPrologue
    * ConsensusDeterminedVersionAssignments
    * Digest
    * EndOfEpochData
    * EndOfEpochTransaction
    * EndOfEpochTransactionKind
    * Event
    * ExecutionStatus
    * FailureStatus
    * GasCostSummary
    * GasPayment
    * GenesisObject
    * GenesisTransaction
    * I128
    * Identifier
    * Input
    * Jwk
    * JwkId
    * MakeMoveVector
    * MergeCoins
    * ModifiedAtVersion
    * MoveCall
    * MoveError
    * MoveField
    * MoveLocation
    * MoveModule
    * MovePackage
    * MoveStruct
    * MoveStructValue
    * MoveValue
    * MoveVariant
    * MoveVector
    * MultisigAggregatedSignature
    * MultisigCommittee
    * MultisigMember
    * MultisigMemberPublicKey
    * MultisigMemberSignature
    * NestedResult
    * Object
    * ObjectData
    * ObjectExist
    * ObjectId
    * ObjectReference
    * ObjectReferenceWithOwner
    * ObjectWrite
    * Owner
    * PackageIdDoesNotMatch
    * PackageUpgradeError
    * PackageWrite
    * PasskeyAuthenticator
    * ProgrammableTransaction
    * Publish
    * RandomnessStateUpdate
    * ReadOnlyRoot
    * RoaringBitmap
    * SharedObjectInput
    * SimpleSignature
    * SizeError
    * SplitCoins
    * StructTag
    * SystemPackage
    * Transaction
    * TransactionV1
    * TransactionEffects
    * TransactionEffectsV1
    * TransactionEffectsV2
    * TransactionEvents
    * TransactionExpiration
    * TransactionKind
    * TransferObjects
    * TypeArgumentError
    * TypeOrigin
    * TypeTag
    * U128
    * U256
    * UnchangedSharedObject
    * Upgrade
    * UpgradeInfo
    * UserSignature
    * ValidatorAggregatedSignature
    * ValidatorCommittee
    * ValidatorCommitteeMember
    * VersionAssignment
    * ZkLoginAuthenticator
    * ZkLoginClaim
    * ZkLoginInputs
    * ZkLoginProof
    * ZkLoginPublicIdentifier
  * sui/types/signature_scheme.proto
  * sui/node/v2/node_service.proto
    * BalanceChange
    * EffectsFinality
    * ExecuteTransactionRequest
    * ExecuteTransactionResponse
    * FullCheckpointObject
    * FullCheckpointTransaction
    * GetCheckpointRequest
    * GetCheckpointResponse
    * GetCommitteeRequest
    * GetCommitteeResponse
    * GetFullCheckpointRequest
    * GetFullCheckpointResponse
    * GetNodeInfoRequest
    * GetNodeInfoResponse
    * GetObjectRequest
    * GetObjectResponse
    * GetTransactionRequest
    * GetTransactionResponse
    * Services (node_service.proto)
  * sui/rpc/v2beta/input.proto
    * Input
  * sui/rpc/v2beta/execution_status.proto
    * CommandArgumentError
    * ExecutionError
    * ExecutionStatus
    * MoveLocation
    * PackageUpgradeError
    * SizeError
    * TypeArgumentError
  * sui/rpc/v2beta/checkpoint_summary.proto
    * CheckpointCommitment
    * CheckpointSummary
    * EndOfEpochData
  * sui/rpc/v2beta/effects.proto
    * ChangedObject
    * TransactionEffects
    * UnchangedSharedObject
  * sui/rpc/v2beta/transaction_execution_service.proto
    * ExecuteTransactionRequest
    * ExecuteTransactionResponse
    * TransactionFinality
    * Services (transaction_execution_service.proto)
  * sui/rpc/v2beta/transaction.proto
    * ActiveJwk
    * AuthenticatorStateExpire
    * AuthenticatorStateUpdate
    * CanceledTransaction
    * CanceledTransactions
    * ChangeEpoch
    * Command
    * ConsensusCommitPrologue
    * ConsensusDeterminedVersionAssignments
    * EndOfEpochTransaction
    * EndOfEpochTransactionKind
    * GasPayment
    * GenesisTransaction
    * Jwk
    * JwkId
    * MakeMoveVector
    * MergeCoins
    * MoveCall
    * ProgrammableTransaction
    * Publish
    * RandomnessStateUpdate
    * SplitCoins
    * SystemPackage
    * Transaction
    * TransactionExpiration
    * TransactionKind
    * TransferObjects
    * Upgrade
    * VersionAssignment
  * sui/rpc/v2beta/owner.proto
    * Owner
  * sui/rpc/v2beta/object.proto
    * MoveModule
    * Object
    * TypeOrigin
    * UpgradeInfo
  * sui/rpc/v2beta/object_reference.proto
    * ObjectReference
  * sui/rpc/v2beta/balance_change.proto
    * BalanceChange
  * sui/rpc/v2beta/epoch.proto
    * Epoch
  * sui/rpc/v2beta/ledger_service.proto
    * BatchGetObjectsRequest
    * BatchGetObjectsResponse
    * BatchGetTransactionsRequest
    * BatchGetTransactionsResponse
    * GetCheckpointRequest
    * GetEpochRequest
    * GetObjectRequest
    * GetServiceInfoRequest
    * GetServiceInfoResponse
    * GetTransactionRequest
    * Services (ledger_service.proto)
  * sui/rpc/v2beta/executed_transaction.proto
    * ExecutedTransaction
  * sui/rpc/v2beta/argument.proto
    * Argument
  * sui/rpc/v2beta/checkpoint.proto
    * Checkpoint
  * sui/rpc/v2beta/gas_cost_summary.proto
    * GasCostSummary
  * sui/rpc/v2beta/bcs.proto
    * Bcs
  * sui/rpc/v2beta/event.proto
    * Event
    * TransactionEvents
  * sui/rpc/v2beta/checkpoint_contents.proto
    * CheckpointContents
    * CheckpointedTransactionInfo
  * sui/rpc/v2beta/protocol_config.proto
    * ProtocolConfig
    * AttributesEntry
    * FeatureFlagsEntry
  * sui/rpc/v2beta/signature_scheme.proto
  * sui/rpc/v2beta/signature.proto
    * CircomG1
    * CircomG2
    * MultisigAggregatedSignature
    * MultisigCommittee
    * MultisigMember
    * MultisigMemberPublicKey
    * MultisigMemberSignature
    * PasskeyAuthenticator
    * UserSignature
    * ValidatorAggregatedSignature
    * ValidatorCommittee
    * ValidatorCommitteeMember
    * ZkLoginAuthenticator
    * ZkLoginClaim
    * ZkLoginInputs
    * ZkLoginProof
    * ZkLoginPublicIdentifier
  * sui/rpc/v2alpha/live_data_service.proto
    * CoinMetadata
    * CoinTreasury
    * DynamicField
    * GetCoinInfoRequest
    * GetCoinInfoResponse
    * ListDynamicFieldsRequest
    * ListDynamicFieldsResponse
    * ListOwnedObjectsRequest
    * ListOwnedObjectsResponse
    * OwnedObject
    * RegulatedCoinMetadata
    * ResolveTransactionRequest
    * ResolveTransactionResponse
    * SimulateTransactionRequest
    * SimulateTransactionResponse
    * Services (live_data_service.proto)
  * sui/rpc/v2alpha/subscription_service.proto
    * SubscribeCheckpointsRequest
    * SubscribeCheckpointsResponse
    * Services (subscription_service.proto)
  * google/rpc/status.proto
    * Status
  * google/rpc/error_details.proto
    * BadRequest
    * FieldViolation
    * DebugInfo
    * ErrorInfo
    * MetadataEntry
    * Help
    * Link
    * LocalizedMessage
    * PreconditionFailure
    * Violation
    * QuotaFailure
    * Violation
    * RequestInfo
    * ResourceInfo
    * RetryInfo
  * google/protobuf/timestamp.proto
    * Timestamp
    * Examples
    * JSON Mapping
  * google/protobuf/field_mask.proto
    * FieldMask
    * Field Masks in Projections
    * Field Masks in Update Operations
    * Considerations for HTTP REST
    * JSON Encoding of Field Masks
    * Field Masks and Oneof Fields
    * Field Mask Verification
  * google/protobuf/duration.proto
    * Duration
    * Examples
    * JSON Mapping
  * google/protobuf/any.proto
    * Any
  * google/protobuf/empty.proto
    * Empty
  * Scalar Value Types
    * double
    * float
    * int32
    * int64
    * uint32
    * uint64
    * sint32
    * sint64
    * fixed32
    * fixed64
    * sfixed32
    * sfixed64
    * bool
    * string
    * bytes


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
