Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Sui RPC
    * GraphQL (Alpha)
    * JSON-RPC
    * Sui Full Node gRPC
    * RPC Best Practices
  * Sui CLI
    * Sui CLI Cheat Sheet
    * Sui Client CLI
    * Sui Client PTB CLI
    * Sui Console CLI
    * Sui Keytool CLI
    * Sui Move CLI
    * Sui Validator CLI
  * Sui IDE Support
    * Move Analyzer
    * Move Trace Debugger
  * Sui SDKs
    * dApp Kit
    * Rust SDK
    * TypeScript SDK
    * zkSend SDK
  * Move
    * Framework
      * Bridge
      * Std
      * Sui
      * Sui_system
    * The Move Book
    * The Move Reference
  * Glossary
  * Contribute


  *   * Move
  * Framework


On this page
# Sui Framework
The documentation in this section is created from the Rust `cargo doc` process. The process builds the content from comments in the source code.
## Framework documentation​
The child pages to this topic describe the module members for the following libraries:
## 🗃️ Bridge
8 items
## 🗃️ Std
21 items
## 🗃️ Sui
53 items
## 🗃️ Sui_system
11 items
## Source code​
You can find the source code for these Move modules in the crates/sui-framework/packages directory in the `sui` repository on GitHub. As previously mentioned, the comments included in the code provide context for the logic defined.
## Crate documentation​
You can review the raw `cargo doc` output of the following documentation in the `sui` repository. The .md files are located in the `crates/sui-framework/docs` directory. Online, they are located at https://github.com/MystenLabs/sui/tree/main/crates/sui-framework/docs.
## Build documentation locally​
The most recent documentation is always available in the `main` branch of the `sui` repository. You shouldn't need to build the documentation locally, but if the need arises you can:
  1. Open a terminal or console to the `sui/crates/sui-framework` directory.
  2. Run `cargo doc --workspace --exclude "sui-benchmark" --no-deps`.
  3. The docs are built to `crates/sui-framework/docs` into their respective subdirectories.


If the `cargo doc` process does not work as expected, try running `cargo clean` before attempting again.
Previous
Move References
Next
Bridge
  * Framework documentation
  * Source code
  * Crate documentation
  * Build documentation locally


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
