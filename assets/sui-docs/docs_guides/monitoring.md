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
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides
    * Sui Full Node Configuration
    * Sui Validator Node Configuration
    * Genesis
    * Sui Node Monitoring
    * Updating a Full Node
    * Data Management
    * Database Snapshots
    * Sui Archives
    * Node Tools
    * Sui Exchange Integration Guide
    * Sui Bridge Node Configuration
    * Validator Committee
    * Validator Tasks


  *   * Operator Guides
  * Sui Node Monitoring


On this page
# Sui Node Monitoring
These instructions are for advanced users. If you just need a local development environment, you should instead follow the instructions in Create a Local Sui Network to create a local Full node, validators, and faucet.
Nodes expose on `localhost:9184/metrics` by default.
You can view the metrics in the metrics UI, or you can use a tool like `curl` to get the metrics in a format that is easy to parse.
```
$ curl -s http://localhost:9184/metrics | grep -E 'sui_validator|sui_fullnode'  

```

## Production monitoring​
For production monitoring, we recommend using Prometheus and Grafana.
You can use grafana agent, grafana alloy, or another tool to scrape the metrics from your node.
Previous
Genesis
Next
Updating a Full Node
  * Production monitoring


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
