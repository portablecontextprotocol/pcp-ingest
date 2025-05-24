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
    * The Move Book
    * The Move Reference
  * Glossary
  * Contribute


  *   * Sui CLI


On this page
# Sui CLI
Sui provides a command line interface (CLI) tool to interact with the Sui network, its features, and the Move programming language. The complete suite of tools is called the Sui CLI, with commands grouped together by feature. Each group of commands is commonly referred to by its top-level command: Sui Client CLI, Sui Console CLI, Sui Keytool CLI, Sui Move CLI, and Sui Validator CLI.
## Check Sui CLI installation​
Before you can use the Sui CLI, you must install it. To check if the CLI exists on your system, open a terminal or console and type the following command:
```
$ sui --version  

```

If the terminal or console responds with a version number, you already have the Sui CLI installed.
If the command is not found, follow the instructions in Install Sui to get the Sui CLI on your system.
## Update CLI​
To get the latest version of the CLI, you can run the following command from a terminal or console. Be sure to replace `<BRANCH-NAME>` with `main`, `devnet`, `testnet`, or `mainnet` to get the desired version. For more information on the branches available, see Sui Environment Setup.
```
$ cargo install --locked --git https://github.com/MystenLabs/sui.git --branch <BRANCH-NAME> --features tracing sui  

```

The `tracing` feature is important as it adds Move test coverage and debugger support in the Sui CLI. Unless it is enabled you will not be able to use these two features.
## Sui CLI commands​
There are a number of top-level commands available, but the five most useful to users are the following. Use the `help` flag for the commands that are not documented yet. For example, `sui validator --help`.
  * **Sui Client CLI:** Use the `sui client` commands to interact with the Sui network.
  * **Sui Client PTB CLI:** Use the `sui client ptb` command to build and execute PTBs.
  * **Sui Console CLI:** Use `sui console` to open an interactive console with the currently active network.
  * **Sui Keytool CLI:** Use the `sui keytool` commands to access cryptography utilities.
  * **Sui Move CLI:** Use the `sui move` commands to work with the Move programming language.
  * **Sui Validator CLI:** Use the `sui validator` commands to access tools useful for Sui validators.


Previous
RPC Best Practices
Next
Sui CLI Cheat Sheet
  * Check Sui CLI installation
  * Update CLI
  * Sui CLI commands


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
