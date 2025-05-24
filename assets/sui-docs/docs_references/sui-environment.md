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
    * Sui Environment Setup
    * Docs Contribution
    * Contribute to Sui Repositories
    * Submit a SIP
    * Localize Sui Documentation
    * Code of Conduct
    * Style Guide


  *   * Contribute
  * Sui Environment Setup


On this page
# Sui Environment Setup
Before you start developing with Sui and Move, you should familiarize yourself with how to contribute to Sui, how Sui is structured, what tools and SDKs exist, and what plugins are available to use in your IDE.
## Fork the Sui repository​
The recommended way to contribute to the Sui repository is to fork the project, make changes on your fork, then submit a pull request (PR). The Sui repository is available on GitHub: https://github.com/MystenLabs/sui.
To create a local Sui repository:
  1. Go to the Sui repository on GitHub.
  2. Click the **Fork** button to create a copy of the repository in your account.
![Fork Sui repo](https://docs.sui.io/references/contribute/sui-environment)
  3. In your forked repository on GitHub, click the green `Code <>` button and copy the **HTTPS** URL GitHub provides.
![Copy URL](https://docs.sui.io/assets/images/gh-url-ee80fb7d30edd9a2722b4d2cbd0a34fc.png)
  4. Open a terminal or console on your system at the location you want to save the repository locally. Type `git clone ` and paste the URL you copied in the previous step and press `Enter`.
  5. Type `cd sui` to make `sui` the active directory.


You can use any branching strategy you prefer on your Sui fork. Make your changes locally and push to your repository, submitting PRs to the official Sui repository from your fork as needed.
Be sure to synchronize your fork frequently to keep it up-to-date with active development.
## Sui repository and how to contribute​
The Sui repo is a monorepo, containing all the source code that is used to build and run the Sui network, as well as this documentation.
The root folder of the Sui monorepo has the following top-level folders:
  * apps: Contains the source code for the main web applications that Mysten Labs runs, `Sui Wallet`.
  * consensus: Contains the source code of consensus.
  * crates: Contains all the Rust crates that are part of the Sui system.
  * dapps: Contains some examples of decentralized applications built on top of Sui, such as Kiosk or Sponsored Transactions.
  * dashboards: Currently empty.
  * doc: Contains deprecated documentation related to Move and Sui.
  * docker: Contains the docker files needed to spin up a node, an indexer, a Full node or other services.
  * docs: Contains this documentation and the source for this site.
  * examples: Contains examples of apps written for Sui and smart contracts written in Move.
  * external-crates: Contains the source code for the Move programming language.
  * kiosk: Contains the source code of the Mysten Labs Kiosk extensions and rules, as well as examples.
  * nre: Contains information about node and network reliability engineering.
  * scripts: Contains a number of scripts that are used internally.
  * sui-execution: Contains the source code responsible for abstracting access to the execution layer.


The following primary directories offer a good starting point for exploring the Sui codebase:
  * move - Move VM, compiler, and tools.
  * consensus - Consensus engine.
  * typescript-sdk - the Sui TypeScript SDK.
  * wallet - Chrome extension wallet for Sui.
  * sui - the Sui command line tool.
  * sui-core - Core Sui components.
  * sui-execution - Execution Layer (programmable transactions, execution integration).
  * sui-framework - Move system packages (0x1, 0x2, 0x3, 0xdee9).
  * sui-network - Networking interfaces.
  * sui-node - Validator and Full node software.
  * sui-protocol-config - On-chain system configuration and limits.
  * sui-sdk - The Sui Rust SDK.
  * sui-types - Sui object types, such as coins and gas.


## Development branches​
The Sui repository includes four primary branches: `devnet`, `testnet`, `mainnet`, and `main`.
The `devnet` branch includes the latest stable build of Sui. Choose the `devnet` branch if you want to build or test on Sui Devnet. If you encounter an issue or find a bug, it may already be fixed in the `main` branch. To submit a PR, you should push commits to your fork of the `main` branch.
The `testnet` branch includes the code running on the Sui Testnet network.
The `mainnet` branch includes the code running on the Sui Mainnet network.
The `main` branch includes the most recent changes and updates. Use the `main` branch if you want to contribute to the Sui project or to experiment with cutting-edge functionality. The `main` branch might include unreleased changes and experimental features, so use it at your own risk.
Previous
Docs Contribution
Next
Docs Contribution
  * Fork the Sui repository
  * Sui repository and how to contribute
  * Development branches


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
