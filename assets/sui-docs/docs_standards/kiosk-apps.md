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


  *   * Kiosk Apps


On this page
# Kiosk Apps
Kiosk apps are a way to extend the functionality of Sui Kiosk while keeping the core functionality intact. You can develop apps to add new features to a kiosk without having to modify the core code or move the assets elsewhere.
There are two types of apps:
  * Basic apps
  * Permissioned apps


## Basic apps​
Basic Kiosk apps do not require Kiosk Apps API to function. They usually serve the purpose of adding custom metadata to a kiosk or wrapping/working with existing objects such as `Kiosk` or `KioskOwnerCap`. An example of an app that does not require the API is the Personal Kiosk app.
### UID access via the uid_mut​
Kiosk has an `id: UID` field like all objects on Sui, which allows this object to be uniquely identified and carry custom dynamic fields and dynamic object fields. The Kiosk itself is built around dynamic fields and features like place and list are built around dynamic object fields.
### The uid_mut_as_owner function​
Kiosk can carry additional dynamic fields and dynamic object fields. The `uid_mut_as_owner` function allows the Kiosk owner to mutably access the UID of the Kiosk object and use it to add or remove custom fields.
Function signature:
`kiosk::uid_mut_as_owner(self: &mut Kiosk, cap: &KioskOwnerCap): &mut UID`
### The public uid getter​
Anyone can read the `uid` of kiosks. This allows third party modules to read the fields of the kiosk if they're allowed to do so. Therefore enabling the object capability and other patterns.
### Basic app ideas​
You can attach custom dynamic fields to your kiosks that anyone can then read (but only you can modify), you can use this to implement basic apps. For example, a Kiosk Name app where you as the kiosk owner can set a name for the kiosk, attach it as a dynamic field, and make it readable by anyone.
```
module examples::kiosk_name_ext;  
  
usestd::string::String;  
usesui::dynamic_fieldasdf;  
usesui::kiosk::{Self, Kiosk, KioskOwnerCap};  
  
/// The dynamic field key for the Kiosk Name Extension  
struct KioskNamehascopy, store, drop {}  
  
/// Add a name to the Kiosk (in this implementation can be called only once)  
publicfunadd(self: &mut Kiosk, cap: &KioskOwnerCap, name: String) {  
letuid_mut = self.uid_mut_as_owner(cap);  
    df::add(uid_mut, KioskName {}, name)  
}  
  
/// Try to read the name of the Kiosk - if set - return Some(String), if not - None  
publicfunname(self: &Kiosk): Option<String> {  
if (df::exists_(self.uid(), KioskName {})) {  
        option::some(*df::borrow(self.uid(), KioskName {}))  
    } else {  
        option::none()  
    }  
}  

```

## Permissioned apps using the Kiosk Apps API​
Permissioned apps use the Kiosk Apps API to perform actions in the kiosk. They usually imply interaction with a third party and provide guarantees for the storage access (preventing malicious actions from the seller).
Just having access to the `uid` is often not enough to build an app due to the security limitations. Only the owner of a kiosk has full access to the `uid`, which means that an app involving a third party would require involvement from the kiosk owner in every step of the process.
In addition to limited and constrained access to storage, app permissions are also owner dependent. In the default setup, no party can place or lock items in a kiosk without its owner's consent. As a result, some cases such as collection bidding (offering X SUI for any item in a collection) requires the kiosk owner to approve the bid.
## kiosk_extension module​
The `kiosk_extension` module addresses concerns over owner bottlenecks and provides more guarantees for storage access. The module provides a set of functions that enable you to perform certain actions in the kiosk without the kiosk owner's involvement and have a guarantee that the storage of the app is not tampered with.
```
module example::my_extension;  
  
usesui::kiosk_extension;  
  
// ...  

```

## App lifecycle​
These are the key points in the lifecycle of a Sui Kiosk app:
  * You can only install an app with an explicit call in the `kiosk_extension` module.
  * A kiosk owner can revoke permissions of an app at any time by calling the `disable` function.
  * A kiosk owner can re-enable a disabled app at any time by calling the `enable` function.
  * You can only remove apps if the app storage is empty (all items are removed).


## Adding an app​
For the app to function, the kiosk owner first needs to install it. To achieve that, an app needs to implement the `add` function that the kiosk owner calls to request all necessary permissions.
### Implementing add function​
The signature of the `kiosk_extension::add` function requires the app witness, making it impossible to install an app without an explicit implementation. The following example shows how to implement the `add` function for an app that requires the `place` permission:
```
module examples::letterbox_ext;  
  
usesui::kiosk_extension;  
  
// ... dependencies  
  
/// The expected set of permissions for extension. It requires `place`.  
constPERMISSIONS: u128 = 1;  
  
/// The Witness struct used to identify and authorize the extension.  
struct Extensionhasdrop {}  
  
/// Install the Mallbox extension into the Kiosk.  
publicfunadd(kiosk: &mut Kiosk, cap: &KioskOwnerCap, ctx: &mut TxContext) {  
    kiosk_extension::add(Extension {}, kiosk, cap, PERMISSIONS, ctx)  
}  

```

## App permissions​
Apps can request permissions from the kiosk owner on installation. Permissions follow the all or nothing principle. If the kiosk owner adds an app, it gets all of the requested permissions; if the kiosk owner then disables an app, it loses all of its permissions.
### Structure​
Permissions are represented as a `u128` integer storing a bitmap. Each of the bits corresponds to a permission, the first bit is the least significant bit. The following table lists all permissions and their corresponding bit:
Bit | Decimal | Permission  
---|---|---  
0000 | 0 | No permissions  
0001 | 1 | App can place  
0010 | 2 | App can place and lock  
0011 | 3 | App can place and lock  
Currently, Sui Kiosk has only two permissions: `place` (first bit) and `lock` and `place` (second bit). The remaining bits are reserved for future use.
### Using permissions in the add function​
It's considered good practice to define a constant containing permissions of the app:
```
module examples::letterbox_ext;  
// ... dependencies  
  
/// The expected set of permissions for the app. It requires `place`.  
constPERMISSIONS: u128 = 1;  
  
/// The witness struct used to identify and authorize the app.  
struct Extensionhasdrop {}  
  
/// Install the Mallbox app into the kiosk and request `place` permission.  
publicfunadd(kiosk: &mut Kiosk, cap: &KioskOwnerCap, ctx: &mut TxContext) {  
    kiosk_extension::add(Extension {}, kiosk, cap, PERMISSIONS, ctx)  
}  

```

### Accessing protected functions​
If an app requests and is granted permissions (and isn't disabled), it can access protected functions. The following example shows how to access the `place` function:
```
module examples::letterbox_ext;  
// ...  
  
/// Emitted when trying to place an item without permissions.  
constENotEnoughPermissions: u64 = 1;  
  
/// Place a letter into the kiosk without the `KioskOwnerCap`.  
publicfunplace(kiosk: &mut Kiosk, letter: Letter, policy: &TransferPolicy<T>) {  
assert!(kiosk_extension::can_place<Extension>(kiosk), ENotEnoughPermissions)  
  
    kiosk_extension::place(Extension {}, kiosk, letter, policy)  
}  

```

Currently, two functions are available:
  * `place<Ext, T>(Ext, &mut Kiosk, T, &TransferPolicy<T>)` - similar to place
  * `lock<Ext, T>(Ext, &mut Kiosk, T, &TransferPolicy<T>)` - similar to lock


### Checking permissions​
Use the `can_place<Ext>(kiosk: &Kiosk): bool` function to check if the app has the `place` permission. Similarly, you can use the `can_lock<Ext>(kiosk: &Kiosk): bool` function to check if the app has the `lock` permission. Both functions make sure that the app is enabled, so you don't need to explicitly check for that.
## App storage​
Every app gets its isolated storage as a bag type that only the app module can access (providing the app witness). See The Move Book to learn more about dynamic collections, like bags, available in Move. After you install an app, it can use the storage to store its data. Ideally, the storage should be managed in a way that allows the app to be removed from the kiosk if there are no active trades or other activities happening at the moment.
The storage is always available to the app if it is installed. The owner of a kiosk can't access the storage of the app if the logic for it is not implemented.
### Accessing the storage​
An installed app can access the storage mutably or immutably using one of the following functions:
  * `storage(_ext: Extension {}, kiosk: &Kiosk): Bag`: returns a reference to the storage of the app. Use the function to read the storage.
  * `storage_mut(_ext: Extension {}, kiosk: &mut Kiosk): &mut Bag`: returns a mutable reference to the storage of the app. Use the function to read and write to the storage.


## Disabling and removing​
The kiosk owner can disable any app at any time. Doing so revokes all permissions of the app and prevents it from performing any actions in the kiosk. The kiosk owner can also re-enable the app at any time.
Disabling an app does not remove it from the kiosk. An installed app has access to its storage until completely removed from the kiosk.
### Disabling an app​
Use the `disable<Ext>(kiosk: &mut Kiosk, cap: &KioskOwnerCap)` function to disable an app. It revokes all permissions of the app and prevents it from performing any protected actions in the kiosk.
**Example PTB**
```
let txb =newTransactionBuilder();  
let kioskArg = tx.object('<ID>');  
let capArg = tx.object('<ID>');  
  
txb.moveCall({  
target:'0x2::kiosk_extension::disable',  
arguments:[ kioskArg, capArg ],  
typeArguments:'<letter_box_package>::letterbox_ext::Extension'  
});  

```

### Removing an app​
You can remove an app only if the storage is empty. Use the `remove<Ext>(kiosk: &mut Kiosk, cap: &KioskOwnerCap)` function to facilitate removal. The function removes the app, unpacks the app storage and configuration and rebates the storage cost to the kiosk owner. Only the kiosk owner can perform this action.
The call fails if the storage is not empty.
**Example PTB**
```
let txb =newTransactionBuilder();  
let kioskArg = tx.object('<ID>');  
let capArg = tx.object('<ID>');  
  
txb.moveCall({  
target:'0x2::kiosk_extension::remove',  
arguments:[ kioskArg, capArg ],  
typeArguments:'<letter_box_package>::letterbox_ext::Extension'  
});  

```

## Related links​
  * NFT Rental: An example implementation of the Kiosk Apps standard that enables renting NFTs.
  * NFT Rental repository: GitHub repo that contains the source code for the NFT Rental app.


Previous
Sui Kiosk
Next
DeepBook
  * Basic apps
    * UID access via the uid_mut
    * The uid_mut_as_owner function
    * The public uid getter
    * Basic app ideas
  * Permissioned apps using the Kiosk Apps API
  * kiosk_extension module
  * App lifecycle
  * Adding an app
    * Implementing add function
  * App permissions
    * Structure
    * Using permissions in the add function
    * Accessing protected functions
    * Checking permissions
  * App storage
    * Accessing the storage
  * Disabling and removing
    * Disabling an app
    * Removing an app
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
