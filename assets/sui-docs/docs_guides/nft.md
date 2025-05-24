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
      * NFT Rental Example
      * Asset Tokenization
    * Cryptography
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * NFTs


On this page
# Create a Non-Fungible Token
On Sui, everything is an object. Moreover, everything is a non-fungible token (NFT) as its objects are unique, non-fungible, and owned.
Creating NFTs on Sui differs from other blockchains that are not object based. Those blockchains require a dedicated standard to handle the properties that define NFTs because they are based on a mapping between smart contracts and the token's ID. For instance, the ERC-721 standard on Ethereum was necessary to pair a globally unique ID with the relevant smart contract address to create a unique token instance on the network.
On Sui, every object already has a unique ID, so whether you're dealing with a million fungible tokens, like coins, or thousands of NFTs with individual characteristics, like SuiFrens, your smart contracts on Sui always interact with individual objects.
Imagine you create an Excitable Chimp NFT collection on Sui and another blockchain that isn't object based. To get an attribute like the Chimp's name on the other blockchain, you would need to interact with the smart contract that created the NFT to get that information (typically from off-chain storage) using the NFT ID. On Sui, the name attribute can be a field on the object that defines the NFT itself. This construct provides a much more straightforward process for accessing metadata for the NFT as the smart contract that wants the information can just return the name from the object itself.
## Example​
The following example creates a basic NFT on Sui. The `TestnetNFT` struct defines the NFT with an `id`, `name`, `description`, and `url` fields.
examples/move/nft/sources/testnet_nft.move
```
publicstruct TestnetNFThaskey, store {  
id: UID,  
name: string::String,  
description: string::String,  
url: Url,  
}  

```

In this example, anyone can mint the NFT by calling the `mint_to_sender` function. As the name suggests, the function creates a new `TestnetNFT` and transfers it to the address that makes the call.
examples/move/nft/sources/testnet_nft.move
```
#[allow(lint(self_transfer))]  
publicfunmint_to_sender(  
name: vector<u8>,  
description: vector<u8>,  
url: vector<u8>,  
ctx: &mut TxContext,  
) {  
letsender = ctx.sender();  
letnft = TestnetNFT {  
id: object::new(ctx),  
name: string::utf8(name),  
description: string::utf8(description),  
url: url::new_unsafe_from_bytes(url),  
    };  
  
    event::emit(NFTMinted {  
object_id: object::id(&nft),  
creator: sender,  
name: nft.name,  
    });  
  
    transfer::public_transfer(nft, sender);  
}  

```

The module includes functions to return NFT metadata, too. Referencing the hypothetical used previously, you can call the `name` function to get that value. As you can see, the function simply returns the name field value of the NFT itself.
examples/move/nft/sources/testnet_nft.move
```
publicfunname(nft: &TestnetNFT): &string::String {  
    &nft.name  
}  

```

Click to open
`testnet_nft.move`
examples/move/nft/sources/testnet_nft.move
```
module examples::testnet_nft;  
  
usestd::string;  
usesui::{event, url::{Self, Url}};  
  
/// An example NFT that can be minted by anybody  
publicstruct TestnetNFThaskey, store {  
id: UID,  
/// Name for the token  
name: string::String,  
/// Description of the token  
description: string::String,  
/// URL for the token  
url: Url,  
// TODO: allow custom attributes  
}  
  
// ===== Events =====  
  
publicstruct NFTMintedhascopy, drop {  
// The Object ID of the NFT  
object_id: ID,  
// The creator of the NFT  
creator: address,  
// The name of the NFT  
name: string::String,  
}  
  
// ===== Public view functions =====  
  
/// Get the NFT's `name`  
publicfunname(nft: &TestnetNFT): &string::String {  
		&nft.name  
}  
  
/// Get the NFT's `description`  
publicfundescription(nft: &TestnetNFT): &string::String {  
		&nft.description  
}  
  
/// Get the NFT's `url`  
publicfunurl(nft: &TestnetNFT): &Url {  
		&nft.url  
}  
  
// ===== Entrypoints =====  
  
#[allow(lint(self_transfer))]  
/// Create a new devnet_nft  
publicfunmint_to_sender(  
name: vector<u8>,  
description: vector<u8>,  
url: vector<u8>,  
ctx: &mut TxContext,  
) {  
letsender = ctx.sender();  
letnft = TestnetNFT {  
id: object::new(ctx),  
name: string::utf8(name),  
description: string::utf8(description),  
url: url::new_unsafe_from_bytes(url),  
		};  
  
		event::emit(NFTMinted {  
object_id: object::id(&nft),  
creator: sender,  
name: nft.name,  
		});  
  
		transfer::public_transfer(nft, sender);  
}  
  
/// Transfer `nft` to `recipient`  
publicfuntransfer(nft: TestnetNFT, recipient: address, _: &mut TxContext) {  
		transfer::public_transfer(nft, recipient)  
}  
  
/// Update the `description` of `nft` to `new_description`  
publicfunupdate_description(  
nft: &mut TestnetNFT,  
new_description: vector<u8>,  
_: &mut TxContext,  
) {  
		nft.description = string::utf8(new_description)  
}  
  
/// Permanently delete `nft`  
publicfunburn(nft: TestnetNFT, _: &mut TxContext) {  
let TestnetNFT { id, name: _, description: _, url: _ } = nft;  
		id.delete()  
}  

```

## Related links​
  * NFT Rental: Example that rents NFTs using Kiosk Apps.
  * Asset Tokenization: Example that uses NFTs to tokenize real-world assets.
  * Kiosk: Asset storage on the Sui network.
  * Kiosk Apps: Extend the functionality of the Kiosk standard.


Previous
Stablecoins
Next
NFT Rental Example
  * Example
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
