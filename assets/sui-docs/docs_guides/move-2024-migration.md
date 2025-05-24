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
      * Migrating to Move 2024
      * Custom Indexer
      * On-Chain Randomness
      * Querying Sui RPC with GraphQL (Alpha)
      * Migrating to GraphQL (Alpha)
      * Object-Based Local Fee Markets
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Advanced Topics
  * Migrating to Move 2024


On this page
# Migrating to Move 2024
New features for Move are becoming available in 2024, a part of the aptly titled "Move 2024" edition. Many of these changes are enhancements to the source language, affecting the compiler without requiring any changes to the binary representation published on chain.
The primary goal of these changes is to make Move easier to write, and hopefully easier to read. The relatively few breaking changes introduced to the source language are to better position Move to handle future advancements.
Existing code will continue to compile, even with the addition of these new features. And because these features are opt-in, you can write your packages with the new features, even if your dependencies do not. Opting to take advantage of the new features in your current modules, however, does introduce some breaking changes.
This document highlights some new features to try out and shows how to migrate your existing modules to use Move 2024.
Please, provide any feedback or report any issues you encounter via GitHub, Discord, or Telegram.
## How to migrate​
To migrate a project to Move 2024 Beta:
  1. Delete your existing `Move.lock` file (if one exists) to make sure you're using the newest `sui-framework` version.
  2. Perform one of the following:
     * Run `sui move migrate` in the root of your Move project. See Automatic migration.
     * Alternatively, update your `Move.toml` file's `[package]` entry to include `edition = "2024.beta"`. If you do this, you might receive a number of new errors related to the breaking changes.


### Automatic migration​
Move 2024 includes an automatic migration script that you can use by calling `sui move migrate` in the root of your Move project. Upon running, your console prompts you for which Move edition to use. If you select `2024.beta`, the script invokes the compiler and attempts to automatically update your code to avoid the breaking changes the update introduces (including marking structs as `public`, mutable variables with the `mut` keyword, avoiding restricted keywords, swapping `friend`s for `public(package)`, and even updating paths to global paths in many cases).
After this is done, your console displays a diff of the changes the script intends to make. If you accept the changes, the script updates your code and your `Move.toml` file automatically. You are now using Move 2024 Beta.
### Update IDE support​
Use the new VSCode Move extension to get support for Move 2024 features. The new extension has a number of improvements over the original move-analyzer extension, but if you would like to keep using the original one, be sure to rebuild and reinstall the `move-analyzer` binary to get 2024 support:
```
$ cargo install --git https://github.com/MystenLabs/sui.git move-analyzer  

```

See the getting started guide on Move IDEs and plugins for more information.
## New features​
Here is a brief overview of some of the new features in Move 2024.
### Method syntax​
You can call certain functions now as methods using the `.` syntax. For example, the following call
```
vector::push_back(&mut v, coin::value(&c));  

```

can now be written as
```
v.push_back(c.value());  

```

Where the receiver of the method (`v` and `c` in this example) is automatically borrowed if necessary (as `&mut v` and `&c` respectively).
You can call any function defined in the same module as the receiver's type as a method if it takes the receiver as its first argument.
For functions defined outside the module, you can declare methods using `public use fun` and `use fun`.
### Index syntax​
With method syntax, you can annotate certain functions as being `#[syntax(index)]` methods. You then call these methods using `v[i]`-style calls.
For example,
```
*&mut v[i] = v[j];  

```

resolves to
```
*vector::borrow_mut(&mut v, i) = *vector::borrow(&v, j);  

```

### public(package)​
`friend` declarations, and the associated `public(friend)` visibility modifiers, are deprecated. In their place is the `public(package)` visibility modifier, which allows calling functions only within the same package where they are defined.
### Positional fields​
You can now define `struct`s with positional fields, which are accessed by zero-based index. For example,
```
publicstruct Pair(u64, u64) hascopy, drop, store;  

```

then to access each field,
```
publicfunsum(p: &Pair): u64 {  
  p.0 + p.1  
}  

```

And as this example shows, you can now declare abilities after the struct field list.
### Nested `use` and standard library defaults​
You can now nest `use` aliases for more conciseness.
```
usesui::{balance, coin::{Self, Coin}};  

```

Additionally, the following `use` declarations are now automatically included in every module:
```
usestd::vector;  
usestd::option::{Self, Option};  
usesui::object::{Self, ID, UID};  
usesui::transfer;  
usesui::tx_context::{Self, TxContext};  

```

### Automatic referencing in equality​
Equality operations, `==` and `!=`, now automatically borrow if one side is a reference and the other is not. For example,
```
funcheck(x: u64, r: &u64): bool {  
  x == r  
}  

```

is equivalent to
```
funcheck(x: u64, r: &u64): bool {  
  &x == r  
}  

```

This automatic borrowing can occur on either side of `==` and `!=`.
### Loop labels​
When nesting loops, it can be convenient to break to the outer loop. For example,
```
letmuti = 0;  
letmutj = 0;  
letmutterminate_loop = false;  
while (i < 10) {  
while (j < 10) {  
if (haystack(i, j) == needle) {  
            terminate_loop = true;  
break;  
        };  
        j = j + 1;  
    };  
if (terminate_loop) break;  
    i = i + 1;  
}  

```

Now, you can directly name the outer loop (`outer` in this case) and break it all at once:
```
letmuti = 0;  
letmutj = 0;  
'outer:while (i < 10) {  
while (j < 10) {  
if (haystack(i, j) == needle) break'outer;  
        j = j + 1;  
    };  
    i = i + 1;  
}  

```

###  `break` with value​
It's now possible to `break` with a value from a `loop`. For example,
```
letmuti = 0;  
letx: u64 = loop {  
if (v[i] > 10) break i;  
    i = i + 1;  
};  

```

You can achieve this with labels, as well. For example,
```
letmuti = 0;  
letmutj = 0;  
letitem = 'outer: loop {  
while (j < 10) {  
letitem = haystack(i, j);  
if (item == needle) break'outer option::some(item);  
        j = j + 1;  
    };  
    i = i + 1;  
if (i == 10) break option::none();  
};  

```

## Breaking changes​
Breaking changes are, unfortunately, a growing pain in Move 2024. We anticipate these changes to be minimally invasive and have provided a migration script to automate them in most cases. In addition, these changes pave the way for new features still to come in Move 2024.
### Datatype visibility requirements​
Currently, all structs in Move are, by convention, public: any other module or package can import them and refer to them by type. To make this clearer, Move 2024 requires that all structs be declared with the `public` keyword. For example,
```
// legacy code  
struct S {x: u64 }  
  
// Move 2024 code  
publicstruct S {x: u64 }  

```

Any non-public struct produces an error at this time, though the Move team is working on new visibility options for future releases.
### Mutability requirements​
Previously, all variables in Move were implicitly mutable. For example,
```
funf(s: S, y: u64): u64 {  
leta = 0;  
let S { x } = s;  
    a = 1;  
    x = 10;  
    y = 5;  
    x + y  
}  

```

Now, you must declare mutable variables explicitly:
```
funf(s: S, muty: u64): u64 {  
letmuta = 0;  
let S { mut x } = 5;  
    a = 1;  
    x = 10;  
    y = 5;  
    x + y  
}  

```

The compiler now produces an error if you attempt to reassign or borrow a variable mutably without this explicit declaration.
### Removing friends and `public(friend)`​
Friends and the `public(friend)` visibilities were introduced early in Move's development, predating even the package system. As indicated in the public(package) section, `public(package)` deprecates `public(friend)` in Move 2024.
The following declaration now produces an error:
```
module pkg::m {  
friendpkg::a;  
public(friend) funf() { ... }  
}  
  
module pkg::a {  
funcalls_f() { ... pkg::m::f() ... }  
}  

```

Instead, if you want your function to be visible only in the package, write:
```
module pkg::m {  
public(package) funf() { ... }  
}  
  
module pkg::a {  
// this now works directly  
funcalls_f() { ... pkg::m::f() ... }  
}  

```

### New keywords​
Looking toward the future, Move 2024 Beta adds the following keywords to the language: `enum`, `for`, `match`, `mut`, and `type`. The compiler, unfortunately, now produces parsing errors when it finds these in other positions. This is a necessary change as the language matures. If you perform automatic migration, the migration tool renames these as `enum` and so on, rewriting the code to use these escaped forms.
### Revised paths and namespaces​
Move 2024 revises how paths and namespaces work compared to legacy Move, toward easing `enum` aliasing in the future. Consider the following snippet from a test annotation in the `sui_system` library:
```
usesui_system::sui_system;  
...  
#[expected_failure(abort_code = sui_system::validator_set::EInvalidCap)]  

```

Legacy Move would always treat a three-part name as an address(`sui_system`), module(`validator_set`), and module member (`EInvalidCap`). Move 2024 respects scope for `use`, so `sui_system` in the attribute resolves to the module, producing a name resolution error overall.
To avoid cases where this is the intended behavior, Move 2024 introduces a prefix operation for global qualification. To use, you can rewrite this annotation as:
```
usesui_system::sui_system;  
...  
#[expected_failure(abort_code = ::sui_system::validator_set::EInvalidCap)]  
// ^ note `::` here  

```

The migration script attempts to remediate naming errors using global qualification when possible.
## Follow along​
The beta release of Move 2024 comes with some powerful new features in addition to the breaking changes described here. There are also more on the horizon. Join the Sui developer newsletter to learn about new, exciting features coming to Move this year, including syntactic macros, enums with pattern matching, and other user-defined syntax extensions.
###  `alpha` and `beta` guidance​
  * `beta` (specified via `edition = "2024.beta"`) is the recommended edition. It includes all the new features mentioned above and all breaking changes. While there is the risk of breaking changes or bugs in `beta`, you should feel comfortable using it in your projects. As new features are added and tested, they will be included in the `beta` edition. The `beta` edition will end after _all_ features for the year have been added and finalized.
  * `alpha` (specified via `edition = "2024.alpha"`) will get new features and changes as they are developed. Breaking changes to features in `alpha` should be expected. As such, take caution when using`alpha` in your projects.


Previous
Advanced Topics
Next
Custom Indexer
  * How to migrate
    * Automatic migration
    * Update IDE support
  * New features
    * Method syntax
    * Index syntax
    * public(package)
    * Positional fields
    * Nested `use` and standard library defaults
    * Automatic referencing in equality
    * Loop labels
    * `break` with value
  * Breaking changes
    * Datatype visibility requirements
    * Mutability requirements
    * Removing friends and `public(friend)`
    * New keywords
    * Revised paths and namespaces
  * Follow along
    * `alpha` and `beta` guidance


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
