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
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Stablecoins


On this page
# Stablecoins on Sui
Stablecoins are a type of cryptocurrency that are designed to maintain a stable value relative to a fiat currency or a basket of assets. They are widely used for trading, lending, and as a store of value.
## Available stablecoins​
On Sui, you can interact with various stablecoins such as USDC, USDT, Agora, and Ondo USDY.
### USDC (USD Coin)​
USDC is a fully collateralized US dollar stablecoin issued by regulated financial institutions. Each USDC token is backed by one US dollar held in reserve. USDC is widely used for trading, payments, and as a stable store of value.
For more detailed information on how to interact with USDC on Sui, refer to the USDC guide.
**Site:** Circle
### USDT (Tether)​
USDT, also known as Tether, is one of the oldest and most widely used stablecoins. It is pegged to the US dollar and is backed by a mix of reserves, including cash, cash equivalents, and other assets.
USDT is currently not issued natively on Sui. For more information on bridging USDT to Sui, refer to SUI Bridging.
**Site:** Tether
### Agora​
AUSD is a fully collateralized US dollar stablecoin issued by Agora Finance.
**Site:** Agora Finance
### Ondo USDY​
USDY is a fully collateralized US dollar stablecoin issued by Ondo Finance, allowing users to earn yield from US Treasury Bills.
**Site:** Ondo Finance
## How to use USDC on Sui​
While this example uses USDC, the same principles can be applied to any asset on Sui that uses the Sui Coin standard.
### Prerequisites​
  * Make sure you have some USDC tokens. Get Testnet tokens from Circle's faucet.


### USDC stablecoin source code​
The USDC stablecoin source code is available in the circlefin/stablecoin-sui repository.
### Import the USDC module in your Move package​
To import the USDC module, add the following line to the `[dependencies]` section of your Move package's `Move.toml` file:
```
usdc={git="https://github.com/circlefin/stablecoin-sui.git",subdir="packages/usdc",rev="master"}  

```

After importing the module, your Move package should look like the following:
examples/move/usdc_usage/Move.toml
```
[package]  
name="usdc_usage"  
edition="2024.beta"  
  
[dependencies]  
Sui={override=true,local="../../../crates/sui-framework/packages/sui-framework"}  
usdc={git="https://github.com/circlefin/stablecoin-sui.git",subdir="packages/usdc",rev="master"}  
  
[addresses]  
usdc_usage="0x0"  

```

The `usdc` package uses a specific version of the `sui` package, which causes a version conflict with the `Sui` package in the Sui framework. You can override the version of the `Sui` package in your `Move.toml` file to use a different version. Add the `override = true` flag to the `Sui` package in your `Move.toml` file.
### Using USDC in Move​
USDC uses the Sui Coin standard and can be used just like any other coin type in the Sui framework.
After importing the `usdc` package, you can use the `USDC` type.
```
useusdc::usdc::USDC;  

```

Then use the `USDC` type just as you would use the `SUI` type when accepting a `Coin<SUI>` parameter.
examples/move/usdc_usage/sources/example.move
```
publicfunbuy_sword_with_usdc(  
coin: Coin<USDC>,  
tx_context: &mut TxContext  
): Sword {  
letsword = create_sword(coin.value(), tx_context);  
  
  transfer::public_transfer(coin, @0x0); // Essentially burning the coin, would send to actual recipient in production  
  
  sword  
}  

```

The following example demonstrates how to use the USDC stablecoin in a Move package and how it relates to using the `SUI` type as well as any generic coin types.
examples/move/usdc_usage/sources/example.move
```
module usdc_usage::example;  
  
usesui::coin::Coin;  
usesui::sui::SUI;  
useusdc::usdc::USDC;  
  
publicstruct Swordhaskey, store {  
id: UID,  
strength: u64  
}  
  
publicfunbuy_sword_with_usdc(  
coin: Coin<USDC>,  
tx_context: &mut TxContext  
): Sword {  
letsword = create_sword(coin.value(), tx_context);  
  
	transfer::public_transfer(coin, @0x0); // Essentially burning the coin, would send to actual recipient in production  
  
	sword  
}  
  
publicfunbuy_sword_with_sui(  
coin: Coin<SUI>,  
tx_context: &mut TxContext  
): Sword {  
letsword = create_sword(coin.value(), tx_context);  
  
	transfer::public_transfer(coin, @0x0); // Essentially burning the coin, would send to actual recipient in production  
  
	sword  
}  
  
publicfunbuy_sword_with_arbitrary_coin<CoinType>(  
coin: Coin<CoinType>,  
tx_context: &mut TxContext  
): Sword {  
letsword = create_sword(coin.value(), tx_context);  
  
	transfer::public_transfer(coin, @0x0); // Essentially burning the coin, would send to actual recipient in production  
  
	sword  
}  
  
funcreate_sword(strength: u64, tx_context: &mut TxContext): Sword {  
letid = object::new(tx_context);  
	Sword { id, strength }  
}  

```

### Using USDC in PTBs​
Use USDC in your PTBs just like any other coin type.
Create a `Coin<USDC>` object with the `coinWithBalance` function.
```
const usdcCoin =coinWithBalance({  
  type:'0xa1ec7fc00a6f40db9693ad1415d0c193ad3906494428cf252621037bd7117e29::usdc::USDC',  
  balance:1_000_000  
})  

```

`0xa1ec7fc00a6f40db9693ad1415d0c193ad3906494428cf252621037bd7117e29` is the Testnet address for USDC, while `0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7` is the Mainnet address.
This coin object can be used as a parameter for any function that accepts a `Coin<USDC>` parameter or a generic `Coin` parameter.
```
const[sword]= tx.moveCall({  
  target:'0xcbbf37a851ed7b625731ca497e2d4aea18cf18145fac3b78bd64f274f6a09d30::usdc_usage::buy_sword_with_usdc',  
  arguments:[  
    usdcCoin  
]  
});  

```

```
const[sword]= tx.moveCall({  
  target:'0xcbbf37a851ed7b625731ca497e2d4aea18cf18145fac3b78bd64f274f6a09d30::usdc_usage::buy_sword_with_arbitrary_coin',  
  typeArguments:['0xa1ec7fc00a6f40db9693ad1415d0c193ad3906494428cf252621037bd7117e29::usdc::USDC'],  
  arguments:[  
    usdcCoin  
]  
});  

```

This coin object can also be used as input for the `transferObjects` function.
```
tx.transferObjects([usdcCoin], recipientAddress);  

```

## Related links​
  * Regulated Coin and Deny List: Create a regulated coin and add or remove names from the deny list.
  * Loyalty Token: Create a token to reward user loyalty.
  * In-Game Token: Create tokens that can be used only within a mobile game.


Previous
Loyalty Tokens
Next
Create a Non-Fungible Token
  * Available stablecoins
    * USDC (USD Coin)
    * USDT (Tether)
    * Agora
    * Ondo USDY
  * How to use USDC on Sui
    * Prerequisites
    * USDC stablecoin source code
    * Import the USDC module in your Move package
    * Using USDC in Move
    * Using USDC in PTBs
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
