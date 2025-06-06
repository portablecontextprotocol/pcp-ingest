Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Coin
  * Closed-Loop Token
  * Sui Kiosk
  * Kiosk Apps
  * DeepBook
  * Sui Object Display
  * Wallet Standard


  *   * Sui Kiosk


On this page
# Sui Kiosk
Kiosk is a decentralized system for commerce applications on Sui. It consists of `Kiosk` objects - shared objects owned by individual parties that store assets and allow listing them for sale as well as utilize custom trading functionality - for example, an auction. While being highly decentralized, Sui Kiosk provides a set of strong guarantees:
  * Kiosk owners retain ownership of their assets to the moment of purchase.
  * Creators set custom policies - sets of rules applied to every trade (such as pay royalty fee or do some arbitrary action X).
  * Marketplaces can index events the `Kiosk` object emits and subscribe to a single feed for on-chain asset trading.


Practically, Kiosk is a part of the Sui framework, and it is native to the system and available to everyone out of the box.
See the Kiosk SDK documentation for examples of working with Kiosk using TypeScript.
## Sui Kiosk owners​
Anyone can create a Sui Kiosk. Ownership of a kiosk is determined by the owner of the `KioskOwnerCap`, a special object that grants full access to a single kiosk. As the owner, you can sell any asset with a type (T) that has a shared `TransferPolicy` available, or you can use a kiosk to store assets even without a shared policy. You can’t sell or transfer any assets from your kiosk that do not have an associated transfer policy available.
To sell an item, if there is an existing transfer policy for the type (T), you just add your assets to your kiosk and then list them. You specify an offer amount when you list an item. Anyone can then purchase the item for the amount of SUI specified in the listing. The associated transfer policy determines what the buyer can do with the purchased asset.
A kiosk owner can:
  * Place and take items
  * List items for sale
  * Add and remove Extensions
  * Withdraw profits from sales
  * Borrow and mutate owned assets
  * Access the full set of trading tools, such as auctions, lotteries, and collection bidding


## Sui Kiosk for buyers​
A buyer is a party that purchases (or - more generally - receives) items from kiosks, anyone on the network can be a buyer (and, for example, a kiosk owner at the same time).
**Benefits:**
  * Buyers get access to global liquidity and can get the best offer
  * Buyers can place bids on collections through their kiosks
  * Most buyer actions performed in kiosks clean up seller objects, which results in free (gas-less) actions


**Responsibilities:**
  * Buyer is the party that pays the fees if they're set in the policy
  * Buyer must follow the rules set by creators or a transaction won't succeed


**Guarantees:**
  * When using a custom trading logic such as an auction, the items are guaranteed to be unchanged until the trade is complete


## Sui Kiosk for marketplaces​
As a marketplace operator, you can implement Sui Kiosk to watch for offers made in a collection of kiosks and display them on a marketplace site. You can also implement a custom system using Kiosk extensions (created by the community or third-parties). For example, marketplaces can use a `TransferPolicyCap` to implement application-specific transfer rules.
## Sui Kiosk for creators​
As a creator, Sui Kiosk supports strong enforcement for transfer policies and associated rules to protect assets and enforce asset ownership. Sui Kiosk gives creators more control over their creations, and puts creators and owners in control of how their works can be used.
Creator is a party that creates and controls the TransferPolicy for a single type. For example, the authors of SuiFrens are the Creators of the `SuiFren<Capy>` type and act as creators in the Kiosk ecosystem. Creators set the policy, but they might also be the first sellers of their assets through a kiosk.
**Creators can:**
  * Set any rules for trades
  * Set multiple ways ("tracks") of rules
  * Enable or disable trades at any moment with a policy
  * Enforce policies (like royalties) on all trades
  * Perform a primary sale of their assets through a kiosk


All of the above is effective immediately and globally.
**Creators cannot:**
  * Take or modify items stored in someone else's kiosk
  * Restrict taking items from kiosks if the "locking" rule was not set in the policy


## Sui Kiosk guarantees​
Sui Kiosk provides a set of guarantees that Sui enforces through smart contracts. These guarantees include:
  * Every trade in Sui Kiosk requires a `TransferPolicy` resolution. This gives creators control over how their assets can be traded.
  * True ownership, which means that only a kiosk owner can take, list, borrow, or modify the assets added to their kiosk. This is similar to how single-owner objects work on Sui.
  * Strong policy enforcement, for example Royalty policies, that lets creators enable or disable policies at any time that applies to all trades on the platform for objects with that policy attached.
  * Changes to a `TransferPolicy` apply instantly and globally.


In practice, these guarantees mean that:
  * When you list an item for sale, no one can modify it or take it from the kiosk.
  * When you define a `PurchaseCap`, an item remains locked and you can’t modify or take the item from the kiosk unless the trade uses or returns the `PurchaseCap`.
  * You can remove any rule at any time (as the owner).
  * You can disable any extension at any time (as the owner).
  * The state of an extension state is always accessible to the extension.


### Asset states in Sui Kiosk​
Sui Kiosk is a shared object that can store heterogeneous values, such as different sets of asset collectibles. When you add an asset to your kiosk, it has one of the following states:
  * PLACED - an item placed in the kiosk using the `kiosk::place` function. The kiosk owner can withdraw it and use it directly, borrow it (mutably or immutably), or list an item for sale.
  * LOCKED - an item placed in the kiosk using the `kiosk::lock` function. You can’t withdraw a Locked item from a kiosk, but you can borrow it mutably and list it for sale. Any item placed in a kiosk that has an associated kiosk lock policy have a LOCKED state.
  * LISTED - an item in the kiosk that is listed for sale using the `kiosk::list` or `kiosk::place_and_list` functions. You can’t modify an item while listed, but you can borrow it immutably or delist it, which returns it to its previous state.
  * LISTED EXCLUSIVELY - an item placed or locked in the kiosk by an extension that calls the `kiosk::list_with_purchase_cap` function. Only the kiosk owner can approve calling the function. The owner can only borrow it immutably. The extension must provide the functionality to delist / unlock the asset, or it might stay locked forever. Given that this action is explicitly performed by the owner - it is the responsibility of the owner to choose verified and audited extensions to use.


When someone purchases an asset from a kiosk, the asset leaves the kiosk and ownership transfers to the buyer’s address.
## Open a Sui Kiosk​
To use a Sui Kiosk, you must create one and have the `KioskOwnerCap` that matches the `Kiosk` object. You can create a new kiosk using a single transaction by calling the `kiosk::default` function. The function creates and shares a `Kiosk`, and transfers the `KioskOwnerCap` to your address.
### Create a Sui Kiosk using programmable transaction blocks​
```
let tx =newTransaction();  
tx.moveCall({  
target:'0x2::kiosk::default',  
});  

```

### Create a Sui Kiosk using the Sui CLI​
Beginning with the Sui `v1.24.1` release, the `--gas-budget` option is no longer required for CLI commands.
```
$ sui client call \  
    --package 0x2 \  
    --module kiosk \  
    --function default \  
    --gas-budget 1000000000  

```

### Create a Sui Kiosk with advanced options​
For more advanced use cases, when you want to choose the storage model or perform an action right away, you can use the programmable transaction block (PTB) friendly function `kiosk::new`. Kiosk is designed to be shared. If you choose a different storage model, such as owned, your kiosk might not function as intended or not be accessible to other users. You can make sure your kiosk works by testing it on Sui Testnet.
### Create a Sui Kiosk with advanced options using programmable transaction blocks​
```
let tx =newTransaction();  
let[kiosk, kioskOwnerCap]= tx.moveCall({  
target:'0x2::kiosk::new',  
});  
  
tx.transferObjects([kioskOwnerCap], sender);  
tx.moveCall({  
target:'0x2::transfer::public_share_object',  
arguments:[kiosk],  
typeArguments:'0x2::kiosk::Kiosk',  
});  

```

### Create a Sui Kiosk with advanced options using the SUI CLI​
Sui CLI does not support PTBs and transaction chaining yet. You can use the `kiosk::default` function instead.
## Place items in and take items from your kiosk​
As a kiosk owner, you can place any assets into your Sui Kiosk. You can take any item from your kiosk that is not currently listed for sale.
There's no limitations on which assets you can place in your kiosk. However, you can’t necessarily list and trade all of the items you place in your kiosk. The `TransferPolicy` associated with the type for the item determines whether you can trade it. To learn more, see the Purchase items from a kiosk section.
### Place an item in your kiosk​
To place an item to the kiosk, the owner needs to call the `sui::kiosk::place` function on the `Kiosk` object and pass the `KioskOwnerCap` and the `Item` as arguments.
`ITEM_TYPE` in the following examples represents the full type of the item.
### Place an item using programmable transaction blocks​
```
let tx =newTransaction();  
  
let itemArg = tx.object('<ID>');  
let kioskArg = tx.object('<ID>');  
let kioskOwnerCapArg = tx.object('<ID>');  
  
tx.moveCall({  
target:'0x2::kiosk::place',  
arguments:[kioskArg, kioskOwnerCapArg, itemArg],  
typeArguments:['<ITEM_TYPE>'],  
});  

```

### Place an item using the Sui CLI​
```
$ sui client call \  
    --package 0x2 \  
    --module kiosk \  
    --function place \  
    --args "<KIOSK_ID>" "<CAP_ID>" "<ITEM_ID>" \  
    --type-args "<ITEM_TYPE>" \  
    --gas-budget 1000000000  

```

## Take items from a kiosk​
To take an item from a kiosk you must be the kiosk owner. As the owner, call the `sui::kiosk::take` function on the `Kiosk` object, and pass the `KioskOwnerCap` and `ID` of the item as arguments.
`ITEM_TYPE` in the following examples represents the full type of the item.
### Take an item from a kiosk using programmable transaction blocks​
```
let tx =newTransaction();  
  
let itemId = tx.pure.id('<ITEM_ID>');  
let kioskArg = tx.object('<ID>');  
let kioskOwnerCapArg = tx.object('<ID>');  
  
let item = tx.moveCall({  
target:'0x2::kiosk::take',  
arguments:[kioskArg, kioskOwnerCapArg, itemId],  
typeArguments:['<ITEM_TYPE>'],  
});  

```

### Take an item from a kiosk using the Sui CLI​
The `kiosk::take` function is built to be PTB friendly and returns the asset. The Sui CLI does not yet support transaction chaining.
## Lock items in a kiosk​
Some policies require that assets never get removed from a kiosk, such as for strong royalty enforcement. To support this, Sui Kiosk provides a locking mechanism. Locking is similar to placing except that you can't take a locked asset out of the kiosk.
To lock an asset in a kiosk, call the `sui::kiosk::lock` function. To ensure that you can later unlock the asset you must associate a `TransferPolicy` with the asset.
After you lock an asset, you must use `list` or `list_with_purchase_cap` functions to list it.
### Lock an item in a kiosk​
When you use the `lock` function, similar to using the `place` function, you specify the `KioskOwnerCap` and the `Item` as arguments. But to lock the item, you must also show the `TransferPolicy`.
`<ITEM_TYPE>` in the following examples represents the full type of the asset.
### Lock an item using programmable transaction blocks​
```
const tx =newTransaction();  
  
let kioskArg = tx.object('<ID>');  
let kioskOwnerCapArg = tx.object('<ID>');  
let itemArg = tx.object('<ID>');  
let transferPolicyArg = tx.object('<ID>');  
  
tx.moveCall({  
target:'0x2::kiosk::lock',  
arguments:[kioskArg, kioskOwnerCapArg, transferPolicyArg, itemArg],  
typeArguments:['<ITEM_TYPE>'],  
});  

```

### Lock an item using the Sui CLI​
```
$ sui client call \  
    --package 0x2 \  
    --module kiosk \  
    --function lock \  
    --args "<KIOSK_ID>" "<CAP_ID>" "<TRANSFER_POLICY_ID>" "<ITEM_ID>" \  
    --type-args "<ITEM_TYPE>" \  
    --gas-budget 1000000000  

```

## List and delist items from a kiosk​
Sui Kiosk provides basic trading functionality. As a kiosk owner, you can list assets for sale, and buyers can discover and purchase them. Sui Kiosk supports listing items by default with three primary functions:
  * `kiosk::list` - list an asset for sale for a fixed price
  * `kiosk::delist` - remove an existing listing
  * `kiosk::purchase` - purchase an asset listed for sale


Anyone on the network can purchase an item listed from a Sui Kiosk. To learn more about the purchase flow, see the Purchase section. To learn more about asset states and what can be done with a listed item, see the Asset States section.
### List an item from a kiosk​
As a kiosk owner, you can use the `kiosk::list` function to list any asset you added to your kiosk. Include the item to sell and the list price as arguments. All listings on Sui are in SUI tokens. When you list an item, Sui emits a `kiosk::ItemListed` event that contains the kiosk ID, item ID, type of the item, and the list price.
### List an item using programmable transaction blocks​
```
let tx =newTransaction();  
  
let kioskArg = tx.object('<ID>');  
let capArg = tx.object('<ID>');  
let itemId = tx.pure.id('<ID>');  
let itemType ='ITEM_TYPE';  
let priceArg = tx.pure.u64('<price>');// in MIST (1 SUI = 10^9 MIST)  
  
tx.moveCall({  
target:'0x2::kiosk::list',  
arguments:[kioskArg, capArg, itemId, priceArg],  
typeArguments:[itemType],  
});  

```

### List an item using the Sui CLI​
```
$ sui client call \  
    --package 0x2 \  
    --module kiosk \  
    --function list \  
    --args "<KIOSK_ID>" "<CAP_ID>" "<ITEM_ID>" "<PRICE>" \  
    --type-args "ITEM_TYPE" \  
    --gas-budget 1000000000  

```

### Delist an item​
As a kiosk owner you can use the `kiosk::delist` to delist any currently listed asset. Specify the item to delist as an argument.
When you delist an item, Sui returns to the kiosk owner the gas fees charged to list the item.
When you delist an item, Sui emits a `kiosk::ItemDelisted` event that contains the kiosk ID, item ID, and the type of the item.
### Delist an item using the programmable transaction blocks​
```
let tx =newTransaction();  
let kioskArg = tx.object('<ID>');  
let capArg = tx.object('<ID>');  
let itemId = tx.pure.id('<ID>');  
let itemType ='ITEM_TYPE';  
  
tx.moveCall({  
target:'0x2::kiosk::delist',  
arguments:[kioskArg, capArg, itemId],  
typeArguments:[itemType],  
});  

```

### Delist an item using the Sui CLI​
```
$ sui client call \  
    --package 0x2 \  
    --module kiosk \  
    --function delist \  
    --args "<KIOSK_ID>" "<CAP_ID>" "<ITEM_ID>" \  
    --type-args "ITEM_TYPE" \  
    --gas-budget 1000000000  

```

## Purchase an item from a kiosk​
Anyone that has an address on the Sui network can purchase an item listed from a Sui Kiosk. To purchase an item, you can use the `kiosk::purchase` function. Specify the item to purchase and pay the list price set by the kiosk owner.
You can discover the items listed on the network with the `kiosk::ItemListed` event.
When you use the `kiosk::purchase` function, it returns the purchased asset and the `TransferRequest` for the type associated with the asset. To complete the purchase, you must meet the terms defined in the `TransferPolicy` applied to the asset.
## Borrow an item from a kiosk​
As a kiosk owner, you can access an asset placed or locked in a kiosk without taking the asset from the kiosk. You can always borrow the asset immutably. Whether you can mutably borrow an asset depends on the state of the asset. For example, you can’t borrow a listed asset because you can’t modify it while listed. The functions available include:
  * `kiosk::borrow` - returns an immutable reference to the asset
  * `kiosk::borrow_mut` - returns a mutable reference to the asset
  * `kiosk::borrow_val` - a PTB-friendly version of `borrow_mut`, which allows you to take an asset and place it back in the same transaction.


### Immutable borrow​
You can always borrow an asset from a kiosk immutably. You can use the `kiosk::borrow` function to borrow an asset, however, it is not possible to use references within a programmable transaction block. To access the asset you must use a published module (function).
### Immutably borrow an asset using Sui Move​
```
module examples::immutable_borrow;  
  
usesui::kiosk::{Self, Kiosk, KioskOwnerCap};  
  
publicfunimmutable_borrow_example<T>(self: &Kiosk, cap: &KioskOwnerCap, item_id: ID): &T {  
    self.borrow(cap, item_id)  
}  

```

### Mutable borrow with borrow_mut​
You can mutably borrow an asset from a kiosk if it is not listed. You can use the `kiosk::borrow_mut` function to mutably borrow an asset. However, it is not possible to use references within a PTB, so to access the mutably borrowed asset you must use a published module (function).
### Mutably borrow an asset using Sui Move​
```
module examples::mutable_borrow;  
  
usesui::kiosk::{Self, Kiosk, KioskOwnerCap};  
  
publicfunmutable_borrow_example<T>(  
self: &mut Kiosk, cap: &KioskOwnerCap, item_id: ID  
): &mut T {  
    self.borrow_mut(cap, item_id)  
}  

```

### Mutable borrow with borrow_val​
You can use the PTB-friendly kiosk::borrow_val function. It allows you to take an asset and place it back in the same transaction. To make sure the asset is placed back into the kiosk, the function "obliges" the caller with a “Hot Potato”.
### Mutable borrow with `borrow_val` using programmable transaction blocks​
```
let tx =newTransaction();  
  
let itemType ='ITEM_TYPE';  
let itemId = tx.pure.id('<ITEM_ID>');  
let kioskArg = tx.object('<ID>');  
let capArg = tx.object('<ID>');  
  
let[item, promise]= tx.moveCall({  
target:'0x2::kiosk::borrow_val',  
arguments:[kioskArg, capArg, itemId],  
typeArguments:[itemType],  
});  
  
// freely mutate or reference the `item`  
// any calls are available as long as they take a reference  
// `returnValue` must be explicitly called  
  
tx.moveCall({  
target:'0x2::kiosk::return_val',  
arguments:[kioskArg, item, promise],  
typeArguments:[itemType],  
});  

```

## Withdraw proceeds from a completed sale​
When someone purchases an item, Sui stores the proceeds from the sale in the kiosk. As the kiosk owner, you can withdraw the proceeds at any time by calling the `kiosk::withdraw` function. The function is simple, but because it is PTB friendly it is not currently supported in the Sui CLI.
### Withdraw proceeds using programmable transaction blocks​
```
let tx =newTransaction();  
let kioskArg = tx.object('<ID>');  
let capArg = tx.object('<ID>');  
  
// because the function uses an Option<u64> argument,  
// constructing is a bit more complex  
let amountArg = tx.moveCall({  
target:'0x1::option::some',  
arguments:[tx.pure.u64('<amount>')],  
typeArguments:['u64'],  
});  
  
// alternatively  
let withdrawAllArg = tx.moveCall({  
target:'0x1::option::none',  
typeArguments:['u64'],  
});  
  
let coin = tx.moveCall({  
target:'0x2::kiosk::withdraw',  
arguments:[kioskArg, capArg, amountArg],  
typeArguments:['u64'],  
});  

```

### Withdraw proceeds using the Sui CLI​
This action is not currently supported in the CLI environment.
Previous
Coin/Token API comparison
Next
Kiosk Apps
  * Sui Kiosk owners
  * Sui Kiosk for buyers
  * Sui Kiosk for marketplaces
  * Sui Kiosk for creators
  * Sui Kiosk guarantees
    * Asset states in Sui Kiosk
  * Open a Sui Kiosk
    * Create a Sui Kiosk using programmable transaction blocks
    * Create a Sui Kiosk using the Sui CLI
    * Create a Sui Kiosk with advanced options
    * Create a Sui Kiosk with advanced options using programmable transaction blocks
    * Create a Sui Kiosk with advanced options using the SUI CLI
  * Place items in and take items from your kiosk
    * Place an item in your kiosk
    * Place an item using programmable transaction blocks
    * Place an item using the Sui CLI
  * Take items from a kiosk
    * Take an item from a kiosk using programmable transaction blocks
    * Take an item from a kiosk using the Sui CLI
  * Lock items in a kiosk
    * Lock an item in a kiosk
    * Lock an item using programmable transaction blocks
    * Lock an item using the Sui CLI
  * List and delist items from a kiosk
    * List an item from a kiosk
    * List an item using programmable transaction blocks
    * List an item using the Sui CLI
    * Delist an item
    * Delist an item using the programmable transaction blocks
    * Delist an item using the Sui CLI
  * Purchase an item from a kiosk
  * Borrow an item from a kiosk
    * Immutable borrow
    * Immutably borrow an asset using Sui Move
    * Mutable borrow with borrow_mut
    * Mutably borrow an asset using Sui Move
    * Mutable borrow with borrow_val
    * Mutable borrow with `borrow_val` using programmable transaction blocks
  * Withdraw proceeds from a completed sale
    * Withdraw proceeds using programmable transaction blocks
    * Withdraw proceeds using the Sui CLI


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
