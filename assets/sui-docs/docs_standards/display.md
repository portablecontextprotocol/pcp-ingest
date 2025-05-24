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


  *   * Sui Object Display


On this page
# Sui Object Display
The Sui Object Display standard is a template engine that enables on-chain management of off-chain representation (display) for a type. With it, you can substitute data for an object into a template string. The standard doesn’t limit the fields you can set. You can use the `{property}` syntax to access all object properties, and then insert them as a part of the template string.
Use a `Publisher` object that you own to set `sui::display` for a type. For more information about `Publisher` objects, see Publisher topic in _Sui Move by Example_.
In Sui Move, `Display<T>` represents an object that specifies a set of named templates for the type `T`. For example, for a type `0x2::capy::Capy` the display syntax is: `Display<0x2::capy::Capy>`.
Sui Full nodes process all objects of the type `T` by matching the `Display` definition, and return the processed result when you query an object with the `{ showDisplay: true }` setting in the query.
## Display properties​
The basic set of properties suggested includes:
  * `name` - A name for the object. The name is displayed when users view the object.
  * `description` - A description for the object. The description is displayed when users view the object.
  * `link` - A link to the object to use in an application.
  * `image_url` - A URL or a blob with the image for the object.
  * `thumbnail_url` - A URL to a **smaller** image to use in wallets, explorers, and other products as a preview.
  * `project_url` - A link to a website associated with the object or creator.
  * `creator` - A string that indicates the object creator.


### An example Sui Hero module​
The following code sample demonstrates how the `Display` for an example `Hero` module varies based on the `name`, `id`, and `image_url` properties of the type `Hero`. The following represents the template the `init` function defines:
```
{  
"name":"{name}",  
"link":"https://sui-heroes.io/hero/{id}",  
"image_url":"https://sui-heroes.io/hero/{image_url}",  
"description":"A true Hero of the Sui ecosystem!",  
"project_url":"https://sui-heroes.io",  
"creator":"Unknown Sui Fan"  
}  

```

```
/// Example of an unlimited "Sui Hero" collection - anyone can  
/// mint their Hero. Shows how to initialize the `Publisher` and how  
/// to use it to get the `Display<Hero>` object - a way to describe a  
/// type for the ecosystem.  
module examples::my_hero;  
  
usestd::string::String;  
  
// The creator bundle: these two packages often go together.  
usesui::package;  
usesui::display;  
  
/// The Hero - an outstanding collection of digital art.  
publicstruct Herohaskey, store {  
id: UID,  
name: String,  
image_url: String,  
}  
  
/// One-Time-Witness for the module.  
publicstruct MY_HEROhasdrop {}  
  
/// Claim the `Publisher` object in the module initializer   
/// to then create a `Display`. The `Display` is initialized with  
/// a set of fields (but can be modified later) and published via  
/// the `update_version` call.  
///  
/// Keys and values are set in the initializer but could also be  
/// set after publishing if a `Publisher` object was created.  
funinit(otw: MY_HERO, ctx: &mut TxContext) {  
letkeys = vector[  
        b"name".to_string(),  
        b"link".to_string(),  
        b"image_url".to_string(),  
        b"description".to_string(),  
        b"project_url".to_string(),  
        b"creator".to_string(),  
    ];  
  
letvalues = vector[  
// For `name` one can use the `Hero.name` property  
        b"{name}".to_string(),  
// For `link` one can build a URL using an `id` property  
        b"https://sui-heroes.io/hero/{id}".to_string(),  
// For `image_url` use an IPFS template + `image_url` property.  
        b"ipfs://{image_url}".to_string(),  
// Description is static for all `Hero` objects.  
        b"A true Hero of the Sui ecosystem!".to_string(),  
// Project URL is usually static  
        b"https://sui-heroes.io".to_string(),  
// Creator field can be any  
        b"Unknown Sui Fan".to_string(),  
    ];  
  
// Claim the `Publisher` for the package!  
letpublisher = package::claim(otw, ctx);  
  
// Get a new `Display` object for the `Hero` type.  
letmutdisplay = display::new_with_fields<Hero>(  
        &publisher, keys, values, ctx  
    );  
  
// Commit first version of `Display` to apply changes.  
    display.update_version();  
  
    transfer::public_transfer(publisher, ctx.sender());  
    transfer::public_transfer(display, ctx.sender());  
}  
  
/// Anyone can mint their `Hero`!  
publicfunmint(name: String, image_url: String, ctx: &mut TxContext): Hero {  
    Hero {  
id: object::new(ctx),  
        name,  
        image_url  
    }  
}  

```

## Work with Object Display​
The `display::new<T>` call creates a `Display`, either in a custom function or module initializer, or as part of a programmable transaction. The following code sample demonstrates how to create a `Display`:
```
module sui::display;  
  
/// Get a new Display object for the `T`.  
/// Publisher must be the publisher of the T, `from_package`  
/// check is performed.  
publicfunnew<T>(pub: &Publisher): Display<T> { /* ... */ }  

```

After you create the `Display`, you can modify it. The following code sample demonstrates how to modify a `Display`:
```
module sui::display;  
  
/// Sets multiple fields at once  
publicfunadd_multiple(  
self: &mut Display,  
keys: vector<String>,  
values: vector<String>  
) { /* ... */ }  
  
/// Edit a single field  
publicfunedit(self: &mut Display, key: String, value: String) { /* ... */ }  
  
/// Remove a key from Display  
publicfunremove(self: &mut Display, key: String ) { /* ... */ }  

```

Next, the `update_version` call applies the changes and sets the `Display` for the `T` by emitting an event. Full nodes receive the event and use the data in the event to retrieve a template for the type.
The following code sample demonstrates how to use the `update_version` call:
```
module sui::display;  
  
/// Update the version of Display and emit an event  
publicfunupdate_version(self: &mut Display) { /* ... */ }  

```

## Sui utility objects​
In Sui, utility objects enable authorization for capabilities. Almost all modules have features that can be accessed only with the required capability. Generic modules allow one capability per application, such as a marketplace. Some capabilities mark ownership of a shared object on-chain, or access the shared data from another account. With capabilities, it is important to provide a meaningful description of objects to facilitate user interface implementation. This helps avoid accidentally transferring the wrong object when objects are similar. It also provides a user-friendly description of items that users see.
The following example demonstrates how to create a capy capability:
```
module capy::utility;  
  
/// A capability which grants Capy Manager permission to add  
/// new genes and manage the Capy Market  
publicstruct CapyManagerCaphaskey, store {id: UID }  

```

## Typical objects with data duplication​
A common case with in-game items is to have a large number of similar objects grouped by some criteria. It is important to optimize their size and the cost to mint and update them. Typically, a game uses a single source image or URL per group or item criteria. Storing the source image inside of every object is not optimal. In some cases, users mint in-game items when a game allows them or when they purchase an in-game item. To enable this, some IPFS/Arweave metadata must be created and stored in advance. This requires additional logic that is usually not related to the in-game properties of the item.
The following example demonstrates how to create a Capy:
```
module capy::capy_items;  
  
usestd::string::String;  
  
/// A wearable Capy item. For some items there can be an  
/// unlimited supply. And items with the same name are identical.  
publicstruct CapyItemhaskey, store {  
id: UID,  
name: String  
}  

```

## Unique objects with dynamic representation​
Sui Capys use dynamic image generation. When a Capy is born, its attributes determine the Capy’s appearance, such as color or pattern. When a user puts an item on a Capy, the Capy’s appearance changes. When users put multiple items on a Capy, there’s a chance of a bonus for a combination of items.
To implement this, the Capys game API service refreshes the image in response to a user-initiated change. The URL for a Capy is a template with the `capy.id`. But storing the full URL - as well as other fields in the Capy object due to their diverse population - also leads to users paying for excess storage and increased gas fees.
The following example demonstrates how to implement dynamic image generation:
```
module capy::capy;  
  
/// A Capy - very diverse object with different combination  
/// of genes. Created dynamically + for images a dynamic SVG  
/// generation is used.  
publicstruct Capyhaskey, store {  
id: UID,  
genes: vector<u8>  
}  

```

## Objects with unique static content​
This is the simplest scenario - an object represents everything itself. It is very easy to apply a metadata standard to an object of this kind, especially if the object stays immutable forever. However, if the metadata standard evolves and some ecosystem projects add new features for some properties, this object always stays in its original form and might require backward-compatible changes.
```
module sui::devnet_nft;  
  
usestd::string::String;  
  
/// A Collectible with a static data. URL, name, description are  
/// set only once on a mint event  
publicstruct DevNetNFThaskey, store {  
id: UID,  
name: String,  
description: String,  
url: String,  
}  

```

Previous
Trade and Swap
Next
Wallet Standard
  * Display properties
    * An example Sui Hero module
  * Work with Object Display
  * Sui utility objects
  * Typical objects with data duplication
  * Unique objects with dynamic representation
  * Objects with unique static content


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
