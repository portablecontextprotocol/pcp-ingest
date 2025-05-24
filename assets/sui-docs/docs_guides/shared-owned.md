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
      * Shared versus Owned Objects
      * Using Events
      * Access On-Chain Time
      * Signing and Sending Transactions
      * Sponsored Transactions
      * Avoiding Equivocation
      * Working with PTBs
    * Coins and Tokens
    * Stablecoins
    * NFTs
    * Cryptography
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Sui 101
  * Shared versus Owned Objects


On this page
# Shared versus Owned Objects
Objects on Sui can be shared (accessible for reads and writes by any transaction) or owned (accessible for reads and writes by transactions signed by their owner). Many applications can be built using a solution that either uses shared objects or only owned objects, with trade-offs for each that need to be weighed.
Transactions that use only owned objects benefit from very low latency to finality, because they do not need to go through consensus. On the other hand, the fact that only the owner of the object can access it complicates processes that need to work with objects owned by multiple parties, and access to very hot objects needs to be coordinated off-chain.
Transactions that access one or more shared objects require consensus to sequence reads and writes to those objects, resulting in a slightly higher gas cost and increased latency.
Transactions that access multiple shared objects, or particularly popular objects, might have increases in latency due to contention. However, the advantage of using shared objects lies in the flexibility of allowing multiple addresses to access the same object in a coordinated manner.
To summarize, applications that are extremely sensitive to latency or gas costs, that do not need to handle complex multi-party transactions, or that already require an off-chain service could benefit from a design that only uses owned objects. Applications that require coordination between multiple parties typically benefit from using shared objects.
For more information on the types of objects that Sui supports, see Object Ownership.
## Example: Escrow​
The Escrow example demonstrates the trade-offs between shared objects and owned objects by implementing the same application in both styles. Both styles of the example implement a service that enables a trustless swap of objects between two addresses (a "trade"), with the service holding those objects in escrow.
###  `Locked<T>` and `Key`​
Code Sample
Both implementations use a primitive for locking values, which offers the following interface:
```
module escrow::lock {  
publicfunlock<T: store>(obj: T, ctx: &mut TxContext): (Locked<T>, Key);  
publicfununlock<T: store>(locked: Locked<T>, key: Key): T  
}  

```

Any `T: store` can be locked, to get a `Locked<T>` and a corresponding `Key`, and conversely, the locked value and its corresponding key can be consumed to get back the wrapped object.
The important property that this interface provides is that locked values cannot be modified except by unlocking them first (and later relocking them). Because unlocking consumes the key, tampering with a locked value can be detected by remembering the ID of the key that it was locked with. This prevents situations where one party in a swap changes the object they are offering to reduce its value.
### Owned objects​
Click to open
`owned.move`
examples/trading/contracts/escrow/sources/owned.move
```
/// An escrow for atomic swap of objects using single-owner transactions that  
/// trusts a third party for liveness, but not safety.  
///  
/// Swap via Escrow proceeds in three phases:  
///  
/// 1. Both parties `lock` their objects, getting the `Locked` object and a  
///		`Key`.	Each party can `unlock` their object, to preserve liveness if the  
///		other party stalls before completing the second stage.  
///  
/// 2. Both parties register an `Escrow` object with the custodian, this  
///		requires passing the locked object and its key.	The key is consumed to  
///		unlock the object, but its ID is remembered so the custodian can ensure  
///		the right objects being swapped.	The custodian is trusted to preserve  
///		liveness.  
///  
/// 3. The custodian swaps the locked objects as long as all conditions are met:  
///  
///		- The sender of one Escrow is the recipient of the other and vice versa.  
///			If this is not true, the custodian has incorrectly paired together this  
///			swap.  
///  
///		- The key of the desired object (`exchange_key`) matches the key the  
///			other object was locked with (`escrowed_key`) and vice versa.  
  
///			If this is not true, it means the wrong objects are being swapped,  
///			either because the custodian paired the wrong escrows together, or  
///			because one of the parties tampered with their object after locking it.  
///  
///			The key in question is the ID of the `Key` object that unlocked the  
///			`Locked` object that the respective objects resided in immediately  
///			before being sent to the custodian.  
module escrow::owned;  
  
useescrow::lock::{Locked, Key};  
  
/// An object held in escrow  
publicstruct Escrow<T: key + store> haskey {  
id: UID,  
/// Owner of `escrowed`  
sender: address,  
/// Intended recipient  
recipient: address,  
/// The ID of the key that opens the lock on the object sender wants  
/// from recipient.  
exchange_key: ID,  
/// The ID of the key that locked the escrowed object, before it was  
/// escrowed.  
escrowed_key: ID,  
/// The escrowed object.  
escrowed: T,  
}  
  
// === Error codes ===  
  
/// The `sender` and `recipient` of the two escrowed objects do not match  
constEMismatchedSenderRecipient: u64 = 0;  
  
/// The `exchange_key` fields of the two escrowed objects do not match  
constEMismatchedExchangeObject: u64 = 1;  
  
// === Public Functions ===  
  
/// `ctx.sender()` requests a swap with `recipient` of a locked  
/// object `locked` in exchange for an object referred to by `exchange_key`.  
/// The swap is performed by a third-party, `custodian`, that is trusted to  
/// maintain liveness, but not safety (the only actions they can perform are  
/// to successfully progress the swap).  
///  
/// `locked` will be unlocked with its corresponding `key` before being sent  
/// to the custodian, but the underlying object is still not accessible  
/// until after the swap has executed successfully, or the custodian returns  
/// the object.  
///  
/// `exchange_key` is the ID of a `Key` that unlocks the sender's desired  
/// object.	Gating the swap on the key ensures that it will not succeed if  
/// the desired object is tampered with after the sender's object is held in  
/// escrow, because the recipient would have to consume the key to tamper  
/// with the object, and if they re-locked the object it would be protected  
/// by a different, incompatible key.  
publicfuncreate<T: key + store>(  
key: Key,  
locked: Locked<T>,  
exchange_key: ID,  
recipient: address,  
custodian: address,  
ctx: &mut TxContext,  
) {  
letescrow = Escrow {  
id: object::new(ctx),  
sender: ctx.sender(),  
				recipient,  
				exchange_key,  
escrowed_key: object::id(&key),  
escrowed: locked.unlock(key),  
		};  
  
		transfer::transfer(escrow, custodian);  
}  
  
/// Function for custodian (trusted third-party) to perform a swap between  
/// two parties.	Fails if their senders and recipients do not match, or if  
/// their respective desired objects do not match.  
publicfunswap<T: key + store, U: key + store>(obj1: Escrow<T>, obj2: Escrow<U>) {  
letEscrow {  
id: id1,  
sender: sender1,  
recipient: recipient1,  
exchange_key: exchange_key1,  
escrowed_key: escrowed_key1,  
escrowed: escrowed1,  
		} = obj1;  
  
letEscrow {  
id: id2,  
sender: sender2,  
recipient: recipient2,  
exchange_key: exchange_key2,  
escrowed_key: escrowed_key2,  
escrowed: escrowed2,  
		} = obj2;  
		id1.delete();  
		id2.delete();  
  
// Make sure the sender and recipient match each other  
assert!(sender1 == recipient2, EMismatchedSenderRecipient);  
assert!(sender2 == recipient1, EMismatchedSenderRecipient);  
  
// Make sure the objects match each other and haven't been modified  
// (they remain locked).  
assert!(escrowed_key1 == exchange_key2, EMismatchedExchangeObject);  
assert!(escrowed_key2 == exchange_key1, EMismatchedExchangeObject);  
  
// Do the actual swap  
		transfer::public_transfer(escrowed1, recipient1);  
		transfer::public_transfer(escrowed2, recipient2);  
}  
  
/// The custodian can always return an escrowed object to its original  
/// owner.  
publicfunreturn_to_sender<T: key + store>(obj: Escrow<T>) {  
letEscrow {  
				id,  
				sender,  
recipient: _,  
exchange_key: _,  
escrowed_key: _,  
				escrowed,  
		} = obj;  
		id.delete();  
		transfer::public_transfer(escrowed, sender);  
}  
  
// === Tests ===  
#[test_only]  
usesui::coin::{Self, Coin};  
#[test_only]  
usesui::sui::SUI;  
#[test_only]  
usesui::test_scenario::{Selfasts, Scenario};  
  
#[test_only]  
useescrow::lock;  
  
#[test_only]  
constALICE: address = @0xA;  
#[test_only]  
constBOB: address = @0xB;  
#[test_only]  
constCUSTODIAN: address = @0xC;  
#[test_only]  
constDIANE: address = @0xD;  
  
#[test_only]  
funtest_coin(ts: &mut Scenario): Coin<SUI> {  
		coin::mint_for_testing<SUI>(42, ts::ctx(ts))  
}  
  
#[test]  
funtest_successful_swap() {  
letmutts = ts::begin(@0x0);  
  
// Alice locks the object they want to trade  
let (i1, ik1) = {  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
letcid = object::id(&c);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, ALICE);  
				transfer::public_transfer(k, ALICE);  
				(cid, kid)  
		};  
  
// Bob locks their object as well.  
let (i2, ik2) = {  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
letcid = object::id(&c);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
				(cid, kid)  
		};  
  
// Alice gives the custodian their object to hold in escrow.  
		{  
				ts.next_tx(ALICE);  
letk1: Key = ts.take_from_sender();  
letl1: Locked<Coin<SUI>> = ts.take_from_sender();  
create(k1, l1, ik2, BOB, CUSTODIAN, ts.ctx());  
		};  
  
// Bob does the same.  
		{  
				ts.next_tx(BOB);  
letk2: Key = ts.take_from_sender();  
letl2: Locked<Coin<SUI>> = ts.take_from_sender();  
create(k2, l2, ik1, ALICE, CUSTODIAN, ts.ctx());  
		};  
  
// The custodian makes the swap  
		{  
				ts.next_tx(CUSTODIAN);  
swap<Coin<SUI>, Coin<SUI>>(  
						ts.take_from_sender(),  
						ts.take_from_sender(),  
				);  
		};  
  
// Commit effects from the swap  
		ts.next_tx(@0x0);  
  
// Alice gets the object from Bob  
		{  
letc: Coin<SUI> = ts.take_from_address_by_id(ALICE, i2);  
				ts::return_to_address(ALICE, c);  
		};  
  
// Bob gets the object from Alice  
		{  
letc: Coin<SUI> = ts.take_from_address_by_id(BOB, i1);  
				ts::return_to_address(BOB, c);  
		};  
  
		ts.end();  
}  
  
#[test]  
#[expected_failure(abort_code = EMismatchedSenderRecipient)]  
funtest_mismatch_sender() {  
letmutts = ts::begin(@0x0);  
  
letik1 = {  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, ALICE);  
				transfer::public_transfer(k, ALICE);  
				kid  
		};  
  
letik2 = {  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
				kid  
		};  
  
// Alice wants to trade with Bob.  
		{  
				ts.next_tx(ALICE);  
letk1: Key = ts.take_from_sender();  
letl1: Locked<Coin<SUI>> = ts.take_from_sender();  
create(k1, l1, ik2, BOB, CUSTODIAN, ts.ctx());  
		};  
  
// But Bob wants to trade with Diane.  
		{  
				ts.next_tx(BOB);  
letk2: Key = ts.take_from_sender();  
letl2: Locked<Coin<SUI>> = ts.take_from_sender();  
create(k2, l2, ik1, DIANE, CUSTODIAN, ts.ctx());  
		};  
  
// When the custodian tries to match up the swap, it will fail.  
		{  
				ts.next_tx(CUSTODIAN);  
swap<Coin<SUI>, Coin<SUI>>(  
						ts.take_from_sender(),  
						ts.take_from_sender(),  
				);  
		};  
  
abort1337  
}  
  
#[test]  
#[expected_failure(abort_code = EMismatchedExchangeObject)]  
funtest_mismatch_object() {  
letmutts = ts::begin(@0x0);  
  
letik1 = {  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, ALICE);  
				transfer::public_transfer(k, ALICE);  
				kid  
		};  
  
		{  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
		};  
  
// Alice wants to trade with Bob, but Alice has asked for an  
// object (via its `exchange_key`) that Bob has not put up for  
// the swap.  
		{  
				ts.next_tx(ALICE);  
letk1: Key = ts.take_from_sender();  
letl1: Locked<Coin<SUI>> = ts.take_from_sender();  
create(k1, l1, ik1, BOB, CUSTODIAN, ts.ctx());  
		};  
  
		{  
				ts.next_tx(BOB);  
letk2: Key = ts.take_from_sender();  
letl2: Locked<Coin<SUI>> = ts.take_from_sender();  
create(k2, l2, ik1, ALICE, CUSTODIAN, ts.ctx());  
		};  
  
// When the custodian tries to match up the swap, it will fail.  
		{  
				ts.next_tx(CUSTODIAN);  
swap<Coin<SUI>, Coin<SUI>>(  
						ts.take_from_sender(),  
						ts.take_from_sender(),  
				);  
		};  
  
abort1337  
}  
  
#[test]  
#[expected_failure(abort_code = EMismatchedExchangeObject)]  
funtest_object_tamper() {  
letmutts = ts::begin(@0x0);  
  
// Alice locks the object they want to trade  
letik1 = {  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, ALICE);  
				transfer::public_transfer(k, ALICE);  
				kid  
		};  
  
// Bob locks their object as well.  
letik2 = {  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
				kid  
		};  
  
// Alice gives the custodian their object to hold in escrow.  
		{  
				ts.next_tx(ALICE);  
letk1: Key = ts.take_from_sender();  
letl1: Locked<Coin<SUI>> = ts.take_from_sender();  
create(k1, l1, ik2, BOB, CUSTODIAN, ts.ctx());  
		};  
  
// Bob has a change of heart, so they unlock the object and tamper  
// with it.  
		{  
				ts.next_tx(BOB);  
letk: Key = ts.take_from_sender();  
letl: Locked<Coin<SUI>> = ts.take_from_sender();  
letmutc = lock::unlock(l, k);  
  
let_dust = coin::split(&mut c, 1, ts.ctx());  
let (l, k) = lock::lock(c, ts.ctx());  
create(k, l, ik1, ALICE, CUSTODIAN, ts.ctx());  
		};  
  
// When the Custodian makes the swap, it detects Bob's nefarious  
// behaviour.  
		{  
				ts.next_tx(CUSTODIAN);  
swap<Coin<SUI>, Coin<SUI>>(  
						ts.take_from_sender(),  
						ts.take_from_sender(),  
				);  
		};  
  
abort1337  
}  
  
#[test]  
funtest_return_to_sender() {  
letmutts = ts::begin(@0x0);  
  
// Alice locks the object they want to trade  
letcid = {  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
letcid = object::id(&c);  
let (l, k) = lock::lock(c, ts.ctx());  
leti = object::id_from_address(@0x0);  
create(k, l, i, BOB, CUSTODIAN, ts.ctx());  
				cid  
		};  
  
// Custodian sends it back  
		{  
				ts.next_tx(CUSTODIAN);  
return_to_sender<Coin<SUI>>(ts.take_from_sender());  
		};  
  
		ts.next_tx(@0x0);  
  
// Alice can then access it.  
		{  
letc: Coin<SUI> = ts.take_from_address_by_id(ALICE, cid);  
				ts::return_to_address(ALICE, c)  
		};  
  
		ts.end();  
}  

```

The protocol for swapping via escrow implemented using owned objects starts with both parties locking their respective objects.
This is used to prove that the object has not been tampered with after the swap has been agreed to. If either party doesn't want to proceed at this stage, they just unlock their object.
Assuming both parties are happy to continue, the next step requires both parties to swap the keys.
A third party acts as custodian. The custodian holds objects that are waiting for their counterparts to arrive and when they arrive, it matches them up to complete the swap.
examples/trading/contracts/escrow/sources/owned.move
```
publicfuncreate<T: key + store>(  
key: Key,  
locked: Locked<T>,  
exchange_key: ID,  
recipient: address,  
custodian: address,  
ctx: &mut TxContext,  
) {  
letescrow = Escrow {  
id: object::new(ctx),  
sender: ctx.sender(),  
        recipient,  
        exchange_key,  
escrowed_key: object::id(&key),  
escrowed: locked.unlock(key),  
    };  
  
    transfer::transfer(escrow, custodian);  
}  

```

The `create` function prepares the `Escrow` request and sends it to the `custodian`. The object being offered by this party is passed in, locked, with its key, and the object being requested is identified by the ID of the key it was locked with. While preparing the request, the offered object is unlocked, while remembering the ID of its key.
Although the custodian is trusted to preserve liveness (to complete swaps if it owns both sides of a swap and to return objects if requested), all other correctness properties are maintained in Move: Even though the custodian owns both objects being swapped, the only valid action they are permitted to take is to match them up with their correct counterpart to finish the swap, or to return them:
examples/trading/contracts/escrow/sources/owned.move
```
/// Function for custodian (trusted third-party) to perform a swap between  
/// two parties.  Fails if their senders and recipients do not match, or if  
/// their respective desired objects do not match.  
publicfunswap<T: key + store, U: key + store>(obj1: Escrow<T>, obj2: Escrow<U>) {  
letEscrow {  
id: id1,  
sender: sender1,  
recipient: recipient1,  
exchange_key: exchange_key1,  
escrowed_key: escrowed_key1,  
escrowed: escrowed1,  
    } = obj1;  
  
letEscrow {  
id: id2,  
sender: sender2,  
recipient: recipient2,  
exchange_key: exchange_key2,  
escrowed_key: escrowed_key2,  
escrowed: escrowed2,  
    } = obj2;  
    id1.delete();  
    id2.delete();  
  
// Make sure the sender and recipient match each other  
assert!(sender1 == recipient2, EMismatchedSenderRecipient);  
assert!(sender2 == recipient1, EMismatchedSenderRecipient);  
  
// Make sure the objects match each other and haven't been modified  
// (they remain locked).  
assert!(escrowed_key1 == exchange_key2, EMismatchedExchangeObject);  
assert!(escrowed_key2 == exchange_key1, EMismatchedExchangeObject);  
  
// Do the actual swap  
    transfer::public_transfer(escrowed1, recipient1);  
    transfer::public_transfer(escrowed2, recipient2);  
}  

```

The `swap` function checks that senders and recipients match and that each party wants the object that the other party is offering, by comparing their respective key IDs. If the custodian tried to match together two unrelated escrow requests to swap, the transaction would not succeed.
### Shared objects​
Click to open
`shared.move`
examples/trading/contracts/escrow/sources/shared.move
```
/// An escrow for atomic swap of objects using shared objects without a trusted  
/// third party.  
///  
/// The protocol consists of three phases:  
///  
/// 1. One party `lock`s their object, getting a `Locked` object and its `Key`.  
///		This party can `unlock` their object to preserve livness if the other  
///		party stalls before completing the second stage.  
///  
/// 2. The other party registers a publicly accessible, shared `Escrow` object.  
///		This effectively locks their object at a particular version as well,  
///		waiting for the first party to complete the swap.	The second party is  
///		able to request their object is returned to them, to preserve liveness as  
///		well.  
///  
/// 3. The first party sends their locked object and its key to the shared  
///		`Escrow` object.	This completes the swap, as long as all conditions are  
///		met:  
///  
///		- The sender of the swap transaction is the recipient of the `Escrow`.  
///  
///		- The key of the desired object (`exchange_key`) in the escrow matches  
///			the key supplied in the swap.  
///  
///		- The key supplied in the swap unlocks the `Locked<U>`.  
module escrow::shared;  
  
useescrow::lock::{Locked, Key};  
usesui::{dynamic_object_fieldasdof, event};  
  
/// The `name` of the DOF that holds the Escrowed object.  
/// Allows easy discoverability for the escrowed object.  
publicstruct EscrowedObjectKeyhascopy, store, drop {}  
  
/// An object held in escrow  
///  
/// The escrowed object is added as a Dynamic Object Field so it can still be looked-up.  
publicstruct Escrow<phantom T: key + store> haskey, store {  
id: UID,  
/// Owner of `escrowed`  
sender: address,  
/// Intended recipient  
recipient: address,  
/// ID of the key that opens the lock on the object sender wants from  
/// recipient.  
exchange_key: ID,  
}  
  
// === Error codes ===  
  
/// The `sender` and `recipient` of the two escrowed objects do not match  
constEMismatchedSenderRecipient: u64 = 0;  
  
/// The `exchange_for` fields of the two escrowed objects do not match  
constEMismatchedExchangeObject: u64 = 1;  
  
// === Public Functions ===  
publicfuncreate<T: key + store>(  
escrowed: T,  
exchange_key: ID,  
recipient: address,  
ctx: &mut TxContext,  
) {  
letmutescrow = Escrow<T> {  
id: object::new(ctx),  
sender: ctx.sender(),  
				recipient,  
				exchange_key,  
		};  
		event::emit(EscrowCreated {  
escrow_id: object::id(&escrow),  
key_id: exchange_key,  
sender: escrow.sender,  
				recipient,  
item_id: object::id(&escrowed),  
		});  
  
		dof::add(&mut escrow.id, EscrowedObjectKey {}, escrowed);  
  
		transfer::public_share_object(escrow);  
}  
  
/// The `recipient` of the escrow can exchange `obj` with the escrowed item  
publicfunswap<T: key + store, U: key + store>(  
mutescrow: Escrow<T>,  
key: Key,  
locked: Locked<U>,  
ctx: &TxContext,  
): T {  
letescrowed = dof::remove<EscrowedObjectKey, T>(&mut escrow.id, EscrowedObjectKey {});  
  
letEscrow {  
				id,  
				sender,  
				recipient,  
				exchange_key,  
		} = escrow;  
  
assert!(recipient == ctx.sender(), EMismatchedSenderRecipient);  
assert!(exchange_key == object::id(&key), EMismatchedExchangeObject);  
  
// Do the actual swap  
		transfer::public_transfer(locked.unlock(key), sender);  
  
		event::emit(EscrowSwapped {  
escrow_id: id.to_inner(),  
		});  
  
		id.delete();  
  
		escrowed  
}  
  
/// The `creator` can cancel the escrow and get back the escrowed item  
publicfunreturn_to_sender<T: key + store>(mutescrow: Escrow<T>, ctx: &TxContext): T {  
		event::emit(EscrowCancelled {  
escrow_id: object::id(&escrow),  
		});  
  
letescrowed = dof::remove<EscrowedObjectKey, T>(&mut escrow.id, EscrowedObjectKey {});  
  
letEscrow {  
				id,  
				sender,  
recipient: _,  
exchange_key: _,  
		} = escrow;  
  
assert!(sender == ctx.sender(), EMismatchedSenderRecipient);  
		id.delete();  
		escrowed  
}  
  
// === Events ===  
publicstruct EscrowCreatedhascopy, drop {  
/// the ID of the escrow that was created  
escrow_id: ID,  
/// The ID of the `Key` that unlocks the requested object.  
key_id: ID,  
/// The id of the sender who'll receive `T` upon swap  
sender: address,  
/// The (original) recipient of the escrowed object  
recipient: address,  
/// The ID of the escrowed item  
item_id: ID,  
}  
  
publicstruct EscrowSwappedhascopy, drop {  
escrow_id: ID,  
}  
  
publicstruct EscrowCancelledhascopy, drop {  
escrow_id: ID,  
}  
  
// === Tests ===  
#[test_only]  
usesui::coin::{Self, Coin};  
#[test_only]  
usesui::sui::SUI;  
#[test_only]  
usesui::test_scenario::{Selfasts, Scenario};  
  
#[test_only]  
useescrow::lock;  
  
#[test_only]  
constALICE: address = @0xA;  
#[test_only]  
constBOB: address = @0xB;  
#[test_only]  
constDIANE: address = @0xD;  
  
#[test_only]  
funtest_coin(ts: &mut Scenario): Coin<SUI> {  
		coin::mint_for_testing<SUI>(42, ts.ctx())  
}  
#[test]  
funtest_successful_swap() {  
letmutts = ts::begin(@0x0);  
  
// Bob locks the object they want to trade.  
let (i2, ik2) = {  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
letcid = object::id(&c);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
				(cid, kid)  
		};  
  
// Alice creates a public Escrow holding the object they are willing to  
// share, and the object they want from Bob  
leti1 = {  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
letcid = object::id(&c);  
create(c, ik2, BOB, ts.ctx());  
				cid  
		};  
  
// Bob responds by offering their object, and gets Alice's object in  
// return.  
		{  
				ts.next_tx(BOB);  
letescrow: Escrow<Coin<SUI>> = ts.take_shared();  
letk2: Key = ts.take_from_sender();  
letl2: Locked<Coin<SUI>> = ts.take_from_sender();  
letc = escrow.swap(k2, l2, ts.ctx());  
  
				transfer::public_transfer(c, BOB);  
		};  
// Commit effects from the swap  
		ts.next_tx(@0x0);  
  
// Alice gets the object from Bob  
		{  
letc: Coin<SUI> = ts.take_from_address_by_id(ALICE, i2);  
				ts::return_to_address(ALICE, c);  
		};  
  
// Bob gets the object from Alice  
		{  
letc: Coin<SUI> = ts.take_from_address_by_id(BOB, i1);  
				ts::return_to_address(BOB, c);  
		};  
  
		ts::end(ts);  
}  
  
#[test]  
#[expected_failure(abort_code = EMismatchedSenderRecipient)]  
funtest_mismatch_sender() {  
letmutts = ts::begin(@0x0);  
  
letik2 = {  
				ts.next_tx(DIANE);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, DIANE);  
				transfer::public_transfer(k, DIANE);  
				kid  
		};  
  
// Alice wants to trade with Bob.  
		{  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
create(c, ik2, BOB, ts.ctx());  
		};  
  
// But Diane is the one who attempts the swap  
		{  
				ts.next_tx(DIANE);  
letescrow: Escrow<Coin<SUI>> = ts.take_shared();  
letk2: Key = ts.take_from_sender();  
letl2: Locked<Coin<SUI>> = ts.take_from_sender();  
letc = escrow.swap(k2, l2, ts.ctx());  
  
				transfer::public_transfer(c, DIANE);  
		};  
  
abort1337  
}  
  
#[test]  
#[expected_failure(abort_code = EMismatchedExchangeObject)]  
funtest_mismatch_object() {  
letmutts = ts::begin(@0x0);  
  
		{  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
		};  
  
// Alice wants to trade with Bob, but Alice has asked for an object (via  
// its `exchange_key`) that Bob has not put up for the swap.  
		{  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
letcid = object::id(&c);  
create(c, cid, BOB, ts.ctx());  
		};  
  
// When Bob tries to complete the swap, it will fail, because they  
// cannot meet Alice's requirements.  
		{  
				ts.next_tx(BOB);  
letescrow: Escrow<Coin<SUI>> = ts.take_shared();  
letk2: Key = ts.take_from_sender();  
letl2: Locked<Coin<SUI>> = ts.take_from_sender();  
letc = escrow.swap(k2, l2, ts.ctx());  
  
				transfer::public_transfer(c, BOB);  
		};  
  
abort1337  
}  
  
#[test]  
#[expected_failure(abort_code = EMismatchedExchangeObject)]  
funtest_object_tamper() {  
letmutts = ts::begin(@0x0);  
  
// Bob locks their object.  
letik2 = {  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
				kid  
		};  
  
// Alice sets up the escrow  
		{  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
create(c, ik2, BOB, ts.ctx());  
		};  
  
// Bob has a change of heart, so they unlock the object and tamper with  
// it before initiating the swap, but it won't be possible for Bob to  
// hide their tampering.  
		{  
				ts.next_tx(BOB);  
letk: Key = ts.take_from_sender();  
letl: Locked<Coin<SUI>> = ts.take_from_sender();  
letmutc = lock::unlock(l, k);  
  
let_dust = c.split(1, ts.ctx());  
let (l, k) = lock::lock(c, ts.ctx());  
letescrow: Escrow<Coin<SUI>> = ts.take_shared();  
letc = escrow.swap(k, l, ts.ctx());  
  
				transfer::public_transfer(c, BOB);  
		};  
  
abort1337  
}  
  
#[test]  
funtest_return_to_sender() {  
letmutts = ts::begin(@0x0);  
  
// Alice puts up the object they want to trade  
letcid = {  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
letcid = object::id(&c);  
leti = object::id_from_address(@0x0);  
create(c, i, BOB, ts.ctx());  
				cid  
		};  
  
// ...but has a change of heart and takes it back  
		{  
				ts.next_tx(ALICE);  
letescrow: Escrow<Coin<SUI>> = ts.take_shared();  
letc = escrow.return_to_sender(ts.ctx());  
  
				transfer::public_transfer(c, ALICE);  
		};  
  
		ts.next_tx(@0x0);  
  
// Alice can then access it.  
		{  
letc: Coin<SUI> = ts.take_from_address_by_id(ALICE, cid);  
				ts::return_to_address(ALICE, c)  
		};  
  
		ts::end(ts);  
}  
  
#[test]  
#[expected_failure]  
funtest_return_to_sender_failed_swap() {  
letmutts = ts::begin(@0x0);  
  
// Bob locks their object.  
letik2 = {  
				ts.next_tx(BOB);  
letc = test_coin(&mut ts);  
let (l, k) = lock::lock(c, ts.ctx());  
letkid = object::id(&k);  
				transfer::public_transfer(l, BOB);  
				transfer::public_transfer(k, BOB);  
				kid  
		};  
  
// Alice creates a public Escrow holding the object they are willing to  
// share, and the object they want from Bob  
		{  
				ts.next_tx(ALICE);  
letc = test_coin(&mut ts);  
create(c, ik2, BOB, ts.ctx());  
		};  
  
// ...but then has a change of heart  
		{  
				ts.next_tx(ALICE);  
letescrow: Escrow<Coin<SUI>> = ts.take_shared();  
letc = escrow.return_to_sender(ts.ctx());  
				transfer::public_transfer(c, ALICE);  
		};  
  
// Bob's attempt to complete the swap will now fail.  
		{  
				ts.next_tx(BOB);  
letescrow: Escrow<Coin<SUI>> = ts.take_shared();  
letk2: Key = ts.take_from_sender();  
letl2: Locked<Coin<SUI>> = ts.take_from_sender();  
letc = escrow.swap(k2, l2, ts.ctx());  
  
				transfer::public_transfer(c, BOB);  
		};  
  
abort1337  
}  

```

The protocol in the shared object case is less symmetric, but still starts with the first party locking the object they want to swap.
The second party can then view the object that was locked, and if they decide they want to swap with it, they indicate their interest by creating a swap request:
examples/trading/contracts/escrow/sources/shared.move
```
publicfuncreate<T: key + store>(  
escrowed: T,  
exchange_key: ID,  
recipient: address,  
ctx: &mut TxContext,  
) {  
letmutescrow = Escrow<T> {  
id: object::new(ctx),  
sender: ctx.sender(),  
        recipient,  
        exchange_key,  
    };  
    event::emit(EscrowCreated {  
escrow_id: object::id(&escrow),  
key_id: exchange_key,  
sender: escrow.sender,  
        recipient,  
item_id: object::id(&escrowed),  
    });  
  
    dof::add(&mut escrow.id, EscrowedObjectKey {}, escrowed);  
  
    transfer::public_share_object(escrow);  
}  

```

This time the `create` request accepts the object being escrowed directly (not locked), and creates a shared `Escrow` object. The request remembers the address that sent it (who is allowed to reclaim the object if the swap hasn't already happened), and the intended recipient, who is then expected to continue the swap by providing the object they initially locked:
examples/trading/contracts/escrow/sources/shared.move
```
/// The `recipient` of the escrow can exchange `obj` with the escrowed item  
publicfunswap<T: key + store, U: key + store>(  
mutescrow: Escrow<T>,  
key: Key,  
locked: Locked<U>,  
ctx: &TxContext,  
): T {  
letescrowed = dof::remove<EscrowedObjectKey, T>(&mut escrow.id, EscrowedObjectKey {});  
  
letEscrow {  
        id,  
        sender,  
        recipient,  
        exchange_key,  
    } = escrow;  
  
assert!(recipient == ctx.sender(), EMismatchedSenderRecipient);  
assert!(exchange_key == object::id(&key), EMismatchedExchangeObject);  
  
// Do the actual swap  
    transfer::public_transfer(locked.unlock(key), sender);  
  
    event::emit(EscrowSwapped {  
escrow_id: id.to_inner(),  
    });  
  
    id.delete();  
  
    escrowed  
}  

```

Even though the `Escrow` object is a shared object that is accessible by anyone, the Move interface ensures that only the original sender and the intended recipient can successfully interact with it. `swap` checks that the locked object matches the object that was requested when the `Escrow` was created (again, by comparing key IDs) and assumes that the intended recipient wants the escrowed object (if they did not, they would not have called `swap`).
Assuming all checks pass, the object held in `Escrow` is extracted, its wrapper is deleted and it is returned to the first party. The locked object offered by the first party is also unlocked and sent to the second party, completing the swap.
### Comparison​
This topic explores two ways to implement a swap between two objects. In both cases there is a point at which one party has made a request and the other has not responded. At this point, both parties may want to access the `Escrow` object: One to cancel the swap, and the other to complete it.
In one case, the protocol uses only owned objects but requires a custodian to act as an intermediary. This has the advantage of avoiding the costs and latencies of consensus altogether, but involves more steps and requires trusting a third party for liveness.
In the other case, the object is custodied on chain in a shared object. This requires consensus but involves fewer steps, and no third party.
Previous
Sui 101
Next
Using Events
  * Example: Escrow
    * `Locked<T>` and `Key`
    * Owned objects
    * Shared objects
    * Comparison


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
