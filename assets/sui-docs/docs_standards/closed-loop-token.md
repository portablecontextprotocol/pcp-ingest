Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Coin
  * Closed-Loop Token
    * Action Request
    * Token Policy
    * Spending
    * Rules
    * Coin/Token API comparison
  * Sui Kiosk
  * Kiosk Apps
  * DeepBook
  * Sui Object Display
  * Wallet Standard


  *   * Closed-Loop Token


On this page
# Closed-Loop Token
Using the Closed-Loop Token standard, you can limit the applications that can use the token and set up custom policies for transfers, spends, and conversions. The `sui::token` module in the Sui framework defines the standard.
## Background and use cases​
The Coin standard on Sui is an example of an open-loop system - coins are free-flowing, wrappable, freely transferable and you can store them in any application. The best real world analogy would be cash - hardly regulated and can be freely used and passed.
Some applications, however, require constraining the scope of the token to a specific purpose. For example, some applications might need a token that you can only use for a specific service, or that an authorized account can only use, or a token that you can block certain accounts from using. A real-world analogy would be a bank account - regulated, bank-controlled, and compliant with certain rules and policies.
## Difference with Coin​
Token has key { Balance } 
Coin has key, store { Balance } 
Balance has store { u64 } 
to_balance
to_coin
Token<T>  
TreasuryCap<T>
Coin<T>  
TreasuryCap<T>
Balance<T>  
Supply<T>
Token has key { Balance } 
Coin has key, store { Balance } 
Balance has store { u64 } 
from_balance
from_coin
Token<T>  
TreasuryCap<T>
Coin<T>  
TreasuryCap<T>
Balance<T>  
Supply<T>
Unlike Coin, which has `key + store` abilities and thus supports wrapping and public transfers, Token has only the `key` ability and cannot be wrapped, stored as a dynamic field, or freely transferred (unless there's a custom policy for that). Due to this restriction, Token **can only be owned by an account** and can't be stored in an application (however, it can be "spent" - see Spending section section).
```
// defined in `sui::coin`  
struct Coin<phantom T> haskey, store {id: UID, balance: Balance<T> }  
  
// defined in `sui::token`  
struct Token<phantom T> haskey {id: UID, balance: Balance<T> }  

```

## Compliance and rules​
You can set up any rules for transfers, spends, and conversions for the tokens you create. You specify these rules per action in the TokenPolicy. Rules are custom programmable restrictions that you can use to implement any request authorization or validation logic.
For example, a policy can set a limit on a transfer - `X` tokens per operation; or require user verification before spending tokens; or allow spending tokens only on a specific service.
You can reuse rules across different policies and applications; and you can freely combine rules to create complex policies.
## Public actions​
Tokens have a set of public and protected actions that you can use to manage the token. Public actions are available to everyone and don't require any authorization. They have similar APIs to coins, but operate on the `Token` type:
  * `token::keep` - send a token to the transaction sender
  * `token::join` - join two tokens
  * `token::split` - split a token into two, specify the amount to split
  * `token::zero` - create an empty (zero balance) token
  * `token::destroy_zero` - destroy a token with zero balance


See Coin Token Comparison for coin and token methods comparison.
## Protected actions​
Protected actions are ones that issue an `ActionRequest` - a hot-potato struct that must be resolved for the transaction to succeed. There are three main ways to resolve an `ActionRequest`, most common of which is via the `TokenPolicy`.
  * `token::transfer` - transfer a token to a specified address
  * `token::to_coin` - convert a token to a coin
  * `token::from_coin` - convert a coin to a token
  * `token::spend` - spend a token on a specified address


The previous methods are included in the base implementation, however it is possible to create `ActionRequest`s for custom actions.
## Token policy and rules​
Protected actions are disabled by default but you can enable them in a `TokenPolicy`. Additionally, you can set custom restrictions called rules that a specific action must satisfy for it to succeed.
Previous
Coin
Next
Action Request
  * Background and use cases
  * Difference with Coin
  * Compliance and rules
  * Public actions
  * Protected actions
  * Token policy and rules


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
