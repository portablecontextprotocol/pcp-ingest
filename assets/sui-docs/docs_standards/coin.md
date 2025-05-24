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


  *   * Coin


On this page
# Coin Standard
The Coin standard is the technical standard used for smart contracts on Sui for creating coins on the Sui blockchain. The standardization of coin creation on Sui means that wallets, exchanges, and other smart contracts can manage coins created on Sui the same as they manage SUI, without any additional processing logic.
See Sui Tokenomics to learn more about the SUI native coin and its use on the Sui network.
Although coins on Sui follow the Coin standard, they can offer specialized abilities. For example, you can create a regulated token that allows its creator to add specific addresses to a deny list, so that the identified addresses cannot use the token as inputs to transactions.
See the coin module documentation for all available options when creating a coin-type token on Sui.
## Fungible tokens​
In the Sui blockchain ecosystem, the `Coin<T>` type represents open-loop fungible tokens (see `Token<T>` for closed-loop tokens). Coins are denominated by their type parameter, `T`, which is also associated with metadata (like name, symbol, decimal precision, and so on) that applies to all instances of `Coin<T>`. The `sui::coin` module exposes an interface over `Coin<T>` that treats it as fungible, meaning that a unit of `T` held in one instance of `Coin<T>` is interchangeable with any other unit of `T`, much like how traditional fiat currencies operate.
The documentation refers to fungible tokens created on Sui using the Coin standard as "coins". For fungible tokens created on Sui using the Closed-Loop Token standard, the documentation uses the term "tokens". In practice, the terms for both these objects are often interchangeable.
## Treasury capability​
When you create a coin using the `coin::create_currency` function, the publisher of the smart contract that creates the coin receives a `TreasuryCap` object. The `TreasuryCap` object is required to mint new coins or to burn current ones. Consequently, only addresses that have access to this object are able to maintain the coin supply on the Sui network.
The `TreasuryCap` object is transferable, so a third party can take over the management of a coin that you create if you transfer the `TreasuryCap`. After transferring the capability, however, you are no longer able to mint and burn tokens yourself.
## Regulated coins​
The Coin standard includes the ability to create regulated coins. To create a regulated coin, you use the `coin::create_regulated_currency_v2` function (which uses the `coin::create_currency` function itself), but which also returns a `DenyCap` capability. The `DenyCap` capability allows the bearer to maintain a list of addresses that aren't allowed to use the token.
The regulated-coin-sample repository provides an example of regulated coin creation.
### DenyList object​
The list of addresses that aren't able to use a particular regulated coin is held within a system-created `DenyList` shared object. If you have access to the `DenyCap`, then you can use the `coin::deny_list_v2_add` and `coin::deny_list_v2_remove` functions to add and remove addresses.
### Global pause switch​
Regulated coin objects include an `allow_global_pause` Boolean field. When set to `true`, the bearer of the `DenyCapV2` object for the coin type can use the `coin::deny_list_v2_enable_global_pause` function to pause coin activity indefinitely. Immediately upon the bearer initiating the pause, the network disallows the coin type as input for any transactions. At the start of the next epoch (epochs last ~24 hours), the network additionally disallows all addresses from receiving the coin type.
When the bearer of the `DenyCapV2` object for the coin type removes the pause using `coin::deny_list_v2_disable_global_pause`, the coins are immediately available to use again as transaction inputs. Addresses cannot receive the coin type, however, until the following epoch.
The global pause functionality does not affect the deny list for the coin. After clearing the pause for the coin, any addresses included in the deny list are still unable to interact with the coin.
## Coin metadata​
Each coin you create includes metadata that describes it. Typically, smart contracts freeze this object upon creation using the `transfer::public_freeze_object` function because the metadata for coins should almost never change. Regulated coins freeze the metadata they create automatically.
Regular coins using the Coin standard include a `CoinMetadata` object. As mentioned previously, regulated coins build on top of the same procedure that creates regular coins, so they receive the same metadata object in addition to a `RegulatedCoinMetadata` object that includes deny list information.
The fields of the metadata objects include the following:
#### CoinMetadata​
Name | Description  
---|---  
`id` | The object ID of the metadata for the token.  
`decimals` | The number of decimals the token uses. If you set this field to `3`, then a token of value `1000` would display as `1.000`.  
`name` | Name of the coin.  
`symbol` | Symbol for the coin. This might be the same as `name`, but is typically fewer than five all capital letters. For example, `SUI` is the `symbol` for the native coin on Sui but its `name` is also `SUI`.  
`description` | A short description to describe the token.  
`icon_url` | The URL for the token's icon, used for display in wallets, explorers, and other apps.  
#### RegulatedCoinMetadata​
Name | Description  
---|---  
`id` | The ID of the metadata object for the regulated token.  
`coin_metadata_object` | The ID of the underlying metadata object (`CoinMetadata`) for the regulated token.  
`deny_cap_object` | The ID of the token's `DenyCapV2` object, which is necessary to maintain the deny list entries that controls who can and cannot use the token.  
## Minting and burning coins​
The `coin` module provides the logic for creating and destroying coins on the Sui network (as long as you own the associated `TreasuryCap`). These functions are the same for all coins and each requires the `TreasuryCap` as an input.
### Mint​
Use the `coin::mint` function to create new tokens.
crates/sui-framework/packages/sui-framework/sources/coin.move
```
publicfunmint<T>(cap: &mut TreasuryCap<T>, value: u64, ctx: &mut TxContext): Coin<T> {  
    Coin {  
id: object::new(ctx),  
balance: cap.total_supply.increase_supply(value),  
    }  
}  

```

The signature shows that a `Coin<T>` results from calling the function with a `TreasuryCap`, value for the coin created, and the transaction context. The function updates the total supply in `TreasuryCap` automatically. Upon display, the coin `value` respects the `decimals` value in the metadata. So, if you supply 1000000 as the coin `value` that has a `decimal` value of `6`, the coin's value displays as `1.000000`.
### Burn​
Use the `coin::burn` function to destroy current tokens.
crates/sui-framework/packages/sui-framework/sources/coin.move
```
publicentryfunburn<T>(cap: &mut TreasuryCap<T>, c: Coin<T>): u64 {  
let Coin { id, balance } = c;  
    id.delete();  
    cap.total_supply.decrease_supply(balance)  
}  

```

The signature shows that only the `TreasuryCap` and coin object you want to burn are necessary inputs, returning the amount by which the supply was decreased (value of the coin). The function does not allow you to burn more coins than are available in the supply.
## Adding and removing addresses to and from the deny list​
The deny list is only applicable to regulated coins. As mentioned previously, when you create a regulated coin you receive a `DenyCapV2` that authorizes the bearer to add and remove addresses from the system-created `DenyList` object. Any address on the list for your coin is unable to use the coin as an input to transactions starting immediately upon being added. At the epoch that follows address addition to the deny list, the addresses additionally cannot receive the coin type. In other words, an address that gets added to the deny list for a coin type is immediately unable to send the coin. At the start of the following epoch, the address is still unable to send the coin but is also unable to receive it. From that point, the address cannot interact with the coin until expressly removed from the deny list by the `DenyCapV2` bearer.
### Add address to deny list​
Use the `coin::deny_list_v2_add` function to add the provided address to the deny list for your coin. The signature for the function is:
crates/sui-framework/packages/sui-framework/sources/coin.move
```
publicfundeny_list_v2_add<T>(  
deny_list: &mut DenyList,  
_deny_cap: &mut DenyCapV2<T>,  
addr: address,  
ctx: &mut TxContext,  
) {  
letty = type_name::get_with_original_ids<T>().into_string().into_bytes();  
    deny_list.v2_add(DENY_LIST_COIN_INDEX, ty, addr, ctx)  
}  

```

When using this function, you provide the `DenyList` object (`0x403`), the `DenyCap` you receive on coin creation, the address to add to the list, and the transaction context. After using this function, the address you provide is unable to use your coin by the next epoch.
### Remove address from deny list​
Use the `coin::deny_list_v2_remove` function to remove addresses from the deny list for your coin.
crates/sui-framework/packages/sui-framework/sources/coin.move
```
publicfundeny_list_v2_remove<T>(  
deny_list: &mut DenyList,  
_deny_cap: &mut DenyCapV2<T>,  
addr: address,  
ctx: &mut TxContext,  
) {  
letty = type_name::get_with_original_ids<T>().into_string().into_bytes();  
    deny_list.v2_remove(DENY_LIST_COIN_INDEX, ty, addr, ctx)  
}  

```

When using this function, you provide the `DenyList` object (`0x403`), the `DenyCapV2` you receive on coin creation, the address to remove from the list, and the transaction context. If you try to remove an address that isn't on the list, you receive an `ENotFrozen` error and the function aborts. After calling this function, the address you provide is able to use your coin by the next epoch.
### Using an SDK​
You can use either the TypeScript or Rust SDK to manipulate the addresses held in the `DenyList` for your coin. The following examples are based on the regulated coin sample.
  * TypeScript
  * Rust


```
const tx =newTransaction();  
  
tx.moveCall({  
    target:`0x2::coin::deny_list_v2_add`,  
    arguments:[  
        tx.object(<SUI-DENY-LIST-OBJECT-ID>),  
        tx.object(<DENY-CAP-ID>),  
        tx.pure.address(options.address),  
],  
    typeArguments:[<COIN-TYPE>],  
});  

```

  * `<SUI-DENY-LIST-OBJECT-ID>` is `"0x403"`
  * `<DENY-CAP-ID>` is the object of type `DenyCapV2<REGULATED_COIN>` you receive from publishing the contract
  * `options.address` is the address to ban
  * `<COIN-TYPE>` is `${PACKAGE-ID}::${MODULE-NAME}::${COIN-NAME}`, which is `${PACKAGE-ID}::regulated_coin::REGULATED_COIN` based on the example.


```
letmut ptb =ProgrammableTransactionBuilder::new();  
  
let deny_list = ptb.obj(ObjectArg::SharedObject{  
    id: deny_list.0,  
    initial_shared_version: deny_list.1,  
    mutable:true,  
})?;  
let deny_cap = ptb.obj(ObjectArg::ImmOrOwnedObject(deny_cap))?;  
let address = ptb.pure(cmd.address())?;  
ptb.command(Command::move_call(  
SUI_FRAMEWORK_PACKAGE_ID,  
Identifier::from(COIN_MODULE_NAME),  
Identifier::from_str("deny_list_v2_add".to_string())?,  
vec![<otw-type>],  
vec![deny_list, deny_cap, address],  
));  
  
let builder = ptb.finish();  

```

  * `deny_list` is of type `(ObjectID, SequenceNumber)`. 
    * `ObjectID` is `0x403`.
    * `SequenceNumber` is the `initial_shared_version` of the `DenyList` singleton.
  * `deny_cap` is the `ObjectRef` (`(ObjectID, SequenceNumber, ObjectDigest)`) of the `DenyCapV2<REGULATED_COIN>` the publisher has received.
  * `otw_type` is the `TypeTag` created from `<PACKAGE_ID>::regulated_coin::REGULATED_COIN` type.
  * `cmd.address()` returns the address to ban as a `SuiAddress`.


## Globally pausing and unpausing regulated coin activity​
Globally pausing coin activity is only applicable to regulated coin types.
### Pause coin activity​
To pause activity across the network for a regulated coin type with the `allow_global_pause` field set to `true`, use `coin::deny_list_v2_enable_global_pause`. You must provide the `DenyCapV2` object for the coin type to initiate the pause. Transaction activity is paused immediately, and no addresses can receive the coin in the epoch that follows the call to pause.
crates/sui-framework/packages/sui-framework/sources/coin.move
```
#[allow(unused_mut_parameter)]  
publicfundeny_list_v2_enable_global_pause<T>(  
deny_list: &mut DenyList,  
deny_cap: &mut DenyCapV2<T>,  
ctx: &mut TxContext,  
) {  
assert!(deny_cap.allow_global_pause, EGlobalPauseNotAllowed);  
letty = type_name::get_with_original_ids<T>().into_string().into_bytes();  
    deny_list.v2_enable_global_pause(DENY_LIST_COIN_INDEX, ty, ctx)  
}  

```

### Unpause coin activity​
To restart network activity for a paused regulated coin, use the `coin::deny_list_v2_disable_global_pause` function. As with pausing, you must provide the `DenyCapV2` object for the coin type. Transaction activity resumes immediately, and addresses can begin receiving the coin in the epoch that follows the call to remove the pause.
crates/sui-framework/packages/sui-framework/sources/coin.move
```
#[allow(unused_mut_parameter)]  
publicfundeny_list_v2_disable_global_pause<T>(  
deny_list: &mut DenyList,  
deny_cap: &mut DenyCapV2<T>,  
ctx: &mut TxContext,  
) {  
assert!(deny_cap.allow_global_pause, EGlobalPauseNotAllowed);  
letty = type_name::get_with_original_ids<T>().into_string().into_bytes();  
    deny_list.v2_disable_global_pause(DENY_LIST_COIN_INDEX, ty, ctx)  
}  

```

## Query coin data​
You can use the following functions to retrieve data from coins.
### Metadata​
Use the following functions to get the values for the respective fields on the metadata object for coins.
Function | Signature  
---|---  
`get_decimals` | `public fun get_decimals<T>(metadata: &coin::CoinMetadata<T>): u8`  
`get_name` | `public fun get_name<T>(metadata: &coin::CoinMetadata<T>): string::String`  
`get_symbol` | `public fun get_symbol<T>(metadata: &coin::CoinMetadata<T>): ascii::String`  
`get_description` | `public fun get_description<T>(metadata: &coin::CoinMetadata<T>): string::String`  
`get_icon_url` | `public fun get_icon_url<T>(metadata: &coin::CoinMetadata<T>): option::Option<url::Url>`  
### Supply​
Use the `coin::supply` function to get the current supply of a given coin.
## Update coin metadata​
If the `CoinMetadata` object was not frozen upon creation, you can use the following functions to update its values.
Each function signature is similar. Replace `<FUNCTION-NAME>` and `<ATTRIBUTE-TYPE>` with the values defined in the table to get the signature of each function:
```
publicentryfun <FUNCTION-NAME><T>(  
_treasury: &coin::TreasuryCap<T>,  
metadata: &mut coin::CoinMetadata<T>,  
  <ATTRIBUTE-TYPE>  
)  

```

`<FUNCTION-NAME>` | `<ATTRIBUTE-TYPE>`  
---|---  
`update_name` | `name: string::String`  
`update_symbol` | `symbol: ascii::String`  
`update_description` | `description: string::String`  
`update_icon_url` | `url: ascii::String`  
`RegulatedCoinMetadata` is frozen upon creation, so there are no functions to update its data.
## Related links​
Check out the following content for more information about coins and tokens on Sui:
  * Create a Coin: Guide for creating coins and regulated coins in your smart contracts.
  * Closed-Loop Token Standard: Details the Token standard on Sui.
  * `coin` module rustdoc documentation: Automated documentation output for the Sui framework `coin` module.
  * `token` module rustdoc documentation: Automated documentation output for the Sui framework `token` module.
  * Tokenomics: Discover the Sui ecosystem and where SUI coins fit within it.


Previous
Overview
Next
Closed-Loop Token
  * Fungible tokens
  * Treasury capability
  * Regulated coins
    * DenyList object
    * Global pause switch
  * Coin metadata
  * Minting and burning coins
    * Mint
    * Burn
  * Adding and removing addresses to and from the deny list
    * Add address to deny list
    * Remove address from deny list
    * Using an SDK
  * Globally pausing and unpausing regulated coin activity
    * Pause coin activity
    * Unpause coin activity
  * Query coin data
    * Metadata
    * Supply
  * Update coin metadata
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
