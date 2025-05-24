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


  *   * Sui IDE Support
  * Move Trace Debugger


On this page
# Move Trace Debugger
The Move Trace Debugger extension for Visual Studio Code provides a familiar debugging interface for Move unit tests. You can step through code execution, track local variable values, and set line breakpoints to understand how your Move code executes.
## Install​
You must have the Move extension installed to use the debugger. The Move extension includes the Move Trace Debugger so you should not need to install it separately. The install instructions are included for rare cases where an individual install might be necessary.
The Move Trace Debugger extension is available in the Visual Studio Code Marketplace. Search for `Move Trace Debugger` in the **Extensions** view, or press `Ctrl` + `P` or `⌘` + `P` and type `ext install mysten.move-trace-debug`.
Alternatively, run `code --install-extension mysten.move-trace-debug` to install the extension from the command line.
## Usage​
To use the debugger, you must also have the `sui` binary installed with the `tracing` feature flag enabled. The `sui` binaries in release tarballs, Homebrew, and Chocolatey have this feature enabled. See Install Sui for more information, including how to build from source.
Debugging a Move unit test is a two-step process:
**I. Generate execution traces**
  1. Open the command palette (`Shift` + `⌘` + `P` on macOS, `Ctrl` + `Shift` + `P` on Windows/Linux).
  2. Run the `Move: Trace Move test execution` command.
![Move Trace generation in the command palette](https://docs.sui.io/assets/images/trace_palette-44cdb9fffc49dac9aafdf2fb59f2477c.png)
  3. The extension displays a filter prompt. Either type a filter string to target specific tests or leave the field blank to run all tests and press `Enter`.
![Move Trace generation filter string](https://docs.sui.io/assets/images/filter_string-022e5c5770ff7730bbcee771555e3437.png)
  4. Find the generated traces in the `traces` directory.


**II. Start debugging**
  1. Open the Move file containing your test.
  2. Select **Run** -> **Start Debugging** from the menu.
![Start debugging](https://docs.sui.io/assets/images/start_debugging-9067d9648c28de2a89e40e48cb7611ae.png)
  3. If the file has multiple tests, select the specific test from the dropdown menu.
![Test selection](https://docs.sui.io/assets/images/test_selection-b87d383f49a8f94e7872d02360607aa7.png)


## Features​
Currently, the Move Trace Debugger supports basic forward debugging through test execution traces.
Support for reverse debugging and watch expressions is not currently available.
### Stepping through code execution​
Move Trace Debugger supports standard debugging features like step over, step into, step out, continue, and stop. You can step through normal code and Move macros.
![Stepping through code execution](https://docs.sui.io/assets/images/debugger_running-10c4adad4355295a3024512239788905.png)
### Tracking variable values​
Move Trace Debugger supports displaying the values of primitive types, Move structs, and references.
At present, the debugger doesn't support setting watch points on variables.
![Variable values](https://docs.sui.io/assets/images/variables-ae0a716ab061a6e87a08eb9e71a974f9.png)
Previous
Move Analyzer
Next
Sui and Community SDKs
  * Install
  * Usage
  * Features
    * Stepping through code execution
    * Tracking variable values


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
