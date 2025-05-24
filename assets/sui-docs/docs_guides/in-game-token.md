Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search
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
      * Regulated Coin and Deny List
      * In-Game Currency
      * Loyalty Tokens
    * Stablecoins
    * NFTs
    * Cryptography
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Coins and Tokens
  * In-Game Currency


On this page
# In-Game Currency
Using the Sui Closed-Loop Token standard, you can create in-game currency (such as gems or diamonds in mobile games) that you can grant to players for their actions or make available to purchase. You mint the tokens on Sui, but players can only use the tokens within the economy of the game itself. These types of tokens are usually not transferrable and you would typically mint them in predefined amounts to maintain scarcity and game balance.
The following example creates an in-game currency called a GEM, which represents a certain number of SUI. In the example, the user can buy fungible GEMs using SUI, which can then be used as currency within the game. Use the code comments to follow the logic of the example.
## Example​
The Sui repo hosts a basic example of creating in-game currency. The Move modules that create the economy of the example are in the gems.move source file.
### Module examples::sword​
The `examples::sword` module creates one of the objects, a `sword`, that has in-game value. The module assigns a value in GEMs (the other valuable in-game item) to the sword. The module also provides the logic for trading GEMs to receive a sword.
examples/move/token/sources/gems.move
```
module examples::sword {  
useexamples::gem::GEM;  
usesui::token::{Self, Token, ActionRequest};  
  
constEWrongAmount: u64 = 0;  
  
constSWORD_PRICE: u64 = 10;  
  
publicstruct Swordhaskey, store {id: UID }  
  
publicfunbuy_sword(gems: Token<GEM>, ctx: &mut TxContext): (Sword, ActionRequest<GEM>) {  
assert!(SWORD_PRICE == token::value(&gems), EWrongAmount);  
        (Sword { id: object::new(ctx) }, token::spend(gems, ctx))  
    }  
}  

```

### Module examples::gem​
The `examples::gem` module creates the in-game currency, GEMs. Users spend SUI to purchase GEMs, which can then be traded for swords. The module defines three groups of GEMs (small, medium, and large), with each group representing a different in-game value. Constants hold both the value of each package and the actual number of GEMs the groups contain.
The module's `init` function uses `coin::create_currency` to create the GEM. The `init` function, which runs only the one time when the module publishes, also sets the policies for the in-game currency, freezes the metadata for the coin, and transfers the policy capability to the publisher of the package.
examples/move/token/sources/gems.move
```
funinit(otw: GEM, ctx: &mut TxContext) {  
let (treasury_cap, coin_metadata) = coin::create_currency(  
        otw,  
0,  
        b"GEM",  
        b"Capy Gems", // otw, decimal, symbol, name  
        b"In-game currency for Capy Miners",  
none(), // description, url  
        ctx,  
    );  
  
let (mut policy, cap) = token::new_policy(&treasury_cap, ctx);  
  
    token::allow(&mut policy, &cap, buy_action(), ctx);  
    token::allow(&mut policy, &cap, token::spend_action(), ctx);  
  
    transfer::share_object(GemStore {  
id: object::new(ctx),  
gem_treasury: treasury_cap,  
profits: balance::zero(),  
    });  
  
    transfer::public_freeze_object(coin_metadata);  
    transfer::public_transfer(cap, ctx.sender());  
    token::share_policy(policy);  
}  

```

The module handles the purchase of GEMs with the `buy_gems` function.
examples/move/token/sources/gems.move
```
publicfunbuy_gems(  
self: &mut GemStore,  
payment: Coin<SUI>,  
ctx: &mut TxContext,  
): (Token<GEM>, ActionRequest<GEM>) {  
letamount = coin::value(&payment);  
letpurchased = if (amount == SMALL_BUNDLE) {  
        SMALL_AMOUNT  
    } else if (amount == MEDIUM_BUNDLE) {  
        MEDIUM_AMOUNT  
    } else if (amount == LARGE_BUNDLE) {  
        LARGE_AMOUNT  
    } else {  
abortEUnknownAmount  
    };  
  
    coin::put(&mut self.profits, payment);  
  
letgems = token::mint(&mut self.gem_treasury, purchased, ctx);  
letreq = token::new_request(buy_action(), purchased, none(), none(), ctx);  
  
    (gems, req)  
}  

```

Use the following toggle to control the display of the complete module.
Click to open
`examples::gem` module in `gems.move`
examples/move/token/sources/gems.move
```
module examples::gem {  
usestd::{option::none, string::{Self, String}};  
    use sui::{  
        balance::{Self, Balance},  
        coin::{Self, Coin, TreasuryCap},  
        sui::SUI,  
        token::{Self, Token, ActionRequest},  
        tx_context::sender  
    };  
  
constEUnknownAmount: u64 = 0;  
  
constSMALL_BUNDLE: u64 = 10_000_000_000;  
constSMALL_AMOUNT: u64 = 100;  
  
constMEDIUM_BUNDLE: u64 = 100_000_000_000;  
constMEDIUM_AMOUNT: u64 = 5_000;  
  
constLARGE_BUNDLE: u64 = 1_000_000_000_000;  
constLARGE_AMOUNT: u64 = 100_000;  
  
#[allow(lint(coin_field))]  
publicstruct GemStorehaskey {  
id: UID,  
profits: Balance<SUI>,  
gem_treasury: TreasuryCap<GEM>,  
    }  
  
publicstruct GEMhasdrop {}  
  
funinit(otw: GEM, ctx: &mut TxContext) {  
let (treasury_cap, coin_metadata) = coin::create_currency(  
            otw,  
0,  
            b"GEM",  
            b"Capy Gems", // otw, decimal, symbol, name  
            b"In-game currency for Capy Miners",  
none(), // description, url  
            ctx,  
        );  
  
let (mut policy, cap) = token::new_policy(&treasury_cap, ctx);  
  
        token::allow(&mut policy, &cap, buy_action(), ctx);  
        token::allow(&mut policy, &cap, token::spend_action(), ctx);  
  
        transfer::share_object(GemStore {  
id: object::new(ctx),  
gem_treasury: treasury_cap,  
profits: balance::zero(),  
        });  
  
        transfer::public_freeze_object(coin_metadata);  
        transfer::public_transfer(cap, ctx.sender());  
        token::share_policy(policy);  
    }  
  
publicfunbuy_gems(  
self: &mut GemStore,  
payment: Coin<SUI>,  
ctx: &mut TxContext,  
    ): (Token<GEM>, ActionRequest<GEM>) {  
letamount = coin::value(&payment);  
letpurchased = if (amount == SMALL_BUNDLE) {  
            SMALL_AMOUNT  
        } else if (amount == MEDIUM_BUNDLE) {  
            MEDIUM_AMOUNT  
        } else if (amount == LARGE_BUNDLE) {  
            LARGE_AMOUNT  
        } else {  
abortEUnknownAmount  
        };  
  
        coin::put(&mut self.profits, payment);  
  
letgems = token::mint(&mut self.gem_treasury, purchased, ctx);  
letreq = token::new_request(buy_action(), purchased, none(), none(), ctx);  
  
        (gems, req)  
    }  
  
publicfunbuy_action(): String { string::utf8(b"buy") }  
}  

```

### Complete code​
Toggle display of the complete source for this example, including comments, or use the link in the Related links section to view the project source on GitHub.
Click to open
`gems.move`
examples/move/token/sources/gems.move
```
/// This is a simple example of a permissionless module for an imaginary game  
/// that sells swords for Gems. Gems are an in-game currency that can be bought  
/// with SUI.  
module examples::sword {  
useexamples::gem::GEM;  
usesui::token::{Self, Token, ActionRequest};  
  
/// Trying to purchase a sword with an incorrect amount.  
constEWrongAmount: u64 = 0;  
  
/// The price of a sword in Gems.  
constSWORD_PRICE: u64 = 10;  
  
/// A game item that can be purchased with Gems.  
publicstruct Swordhaskey, store {id: UID }  
  
/// Purchase a sword with Gems.  
publicfunbuy_sword(gems: Token<GEM>, ctx: &mut TxContext): (Sword, ActionRequest<GEM>) {  
assert!(SWORD_PRICE == token::value(&gems), EWrongAmount);  
				(Sword { id: object::new(ctx) }, token::spend(gems, ctx))  
		}  
}  
  
/// Module that defines the in-game currency: GEMs which can be purchased with  
/// SUI and used to buy swords (in the `sword` module).  
module examples::gem {  
usestd::{option::none, string::{Self, String}};  
		use sui::{  
				balance::{Self, Balance},  
				coin::{Self, Coin, TreasuryCap},  
				sui::SUI,  
				token::{Self, Token, ActionRequest},  
				tx_context::sender  
		};  
  
/// Trying to purchase Gems with an unexpected amount.  
constEUnknownAmount: u64 = 0;  
  
/// 10 SUI is the price of a small bundle of Gems.  
constSMALL_BUNDLE: u64 = 10_000_000_000;  
constSMALL_AMOUNT: u64 = 100;  
  
/// 100 SUI is the price of a medium bundle of Gems.  
constMEDIUM_BUNDLE: u64 = 100_000_000_000;  
constMEDIUM_AMOUNT: u64 = 5_000;  
  
/// 1000 SUI is the price of a large bundle of Gems.  
/// This is the best deal.  
constLARGE_BUNDLE: u64 = 1_000_000_000_000;  
constLARGE_AMOUNT: u64 = 100_000;  
  
#[allow(lint(coin_field))]  
/// Gems can be purchased through the `Store`.  
publicstruct GemStorehaskey {  
id: UID,  
/// Profits from selling Gems.  
profits: Balance<SUI>,  
/// The Treasury Cap for the in-game currency.  
gem_treasury: TreasuryCap<GEM>,  
		}  
  
/// The OTW to create the in-game currency.  
publicstruct GEMhasdrop {}  
  
// In the module initializer we create the in-game currency and define the  
// rules for different types of actions.  
funinit(otw: GEM, ctx: &mut TxContext) {  
let (treasury_cap, coin_metadata) = coin::create_currency(  
						otw,  
0,  
						b"GEM",  
						b"Capy Gems", // otw, decimal, symbol, name  
						b"In-game currency for Capy Miners",  
none(), // description, url  
						ctx,  
				);  
  
// create a `TokenPolicy` for GEMs  
let (mut policy, cap) = token::new_policy(&treasury_cap, ctx);  
  
				token::allow(&mut policy, &cap, buy_action(), ctx);  
				token::allow(&mut policy, &cap, token::spend_action(), ctx);  
  
// create and share the GemStore  
				transfer::share_object(GemStore {  
id: object::new(ctx),  
gem_treasury: treasury_cap,  
profits: balance::zero(),  
				});  
  
// deal with `TokenPolicy`, `CoinMetadata` and `TokenPolicyCap`  
				transfer::public_freeze_object(coin_metadata);  
				transfer::public_transfer(cap, ctx.sender());  
				token::share_policy(policy);  
		}  
  
/// Purchase Gems from the GemStore. Very silly value matching against module  
/// constants...  
publicfunbuy_gems(  
self: &mut GemStore,  
payment: Coin<SUI>,  
ctx: &mut TxContext,  
		): (Token<GEM>, ActionRequest<GEM>) {  
letamount = coin::value(&payment);  
letpurchased = if (amount == SMALL_BUNDLE) {  
						SMALL_AMOUNT  
				} else if (amount == MEDIUM_BUNDLE) {  
						MEDIUM_AMOUNT  
				} else if (amount == LARGE_BUNDLE) {  
						LARGE_AMOUNT  
				} else {  
abortEUnknownAmount  
				};  
  
				coin::put(&mut self.profits, payment);  
  
// create custom request and mint some Gems  
letgems = token::mint(&mut self.gem_treasury, purchased, ctx);  
letreq = token::new_request(buy_action(), purchased, none(), none(), ctx);  
  
				(gems, req)  
		}  
  
/// The name of the `buy` action in the `GemStore`.  
publicfunbuy_action(): String { string::utf8(b"buy") }  
}  

```

## Related links​
  * Closed Loop Token standard: Details for the standard used to create tokens on Sui.
  * Source code: The source code in GitHub for this example.
  * Loyalty Tokens: Example of how to create tokens that are valid only for a specific service, useful in loyalty reward programs.
  * Regulated Coin and Deny List: Example of how to create regulated coins on the Sui network.


Previous
Regulated Coin and Deny List
Next
Loyalty Tokens
  * Example
    * Module examples::sword
    * Module examples::gem
    * Complete code
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
