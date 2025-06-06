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


  *   * Sui RPC
  * RPC Best Practices


On this page
# RPC Best Practices
This topic provides some best practices for configuring your RPC settings to ensure a reliable infrastructure for your projects and services built on Sui.
Use dedicated nodes/shared services rather than public endpoints for production apps. The public endpoints maintained by Mysten Labs (`fullnode.<NETWORK>.sui.io:443`) are rate-limited, and support only 100 requests per 30 seconds. Do not use public endpoints in production applications with high traffic volume.
You can either run your own Full nodes, or outsource this to a professional infrastructure provider (preferred for apps that have high traffic). You can find a list of reliable RPC endpoint providers for Sui on the Sui Dev Portal using the **Node Service** tag.
## RPC provisioning guidance​
Consider the following when working with a provider:
  * **SLA and 24-hour support:** Choose a provider that offers a SLA that meets your needs and 24-hour support.
  * **Onboarding call:** Always do an onboarding call with the provider you select to ensure they can provide service that meets your needs. If you have a high-traffic event, such as an NFT mint coming up, notify your RPC provider with the expected traffic increase at least 48 hours in advance.
  * **Redundancy:** It is important for high-traffic and time-sensitive apps, like NFT marketplaces and DeFi protocols, to ensure they don't rely on just one provider for RPCs. Many projects default to just using a single provider, but that's extremely risky and you should use other providers to provide redundancy.
  * **Traffic estimate:** You should have a good idea about the amount and type of traffic you expect, and you should communicate that information in advance with your RPC provider. During high-traffic events (such as NFT mints), request increased capacity from your RPC provider in advance. Bot mitigation - As Sui matures, a lot of bots will emerge on the network. Sui dApp builders should think about bot mitigation at the infrastructure level. This depends heavily on use cases. For NFT minting, bots are undesirable. However, for certain DeFi use cases, bots are necessary. Think about the implications and prepare your infrastructure accordingly.
  * **Provisioning notice:** Make RPC provisioning requests at least one week in advance. This gives operators and providers advance notice so they can arrange for the configure hardware/servers as necessary. If there’s a sudden, unexpected demand, please reach out to us so we can help set you up with providers that have capacity for urgent situations.


Previous
Sui Full Node gRPC
Next
Sui CLI
  * RPC provisioning guidance


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
