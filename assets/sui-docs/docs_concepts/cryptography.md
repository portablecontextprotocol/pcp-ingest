Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Sui Components
  * App Developers
  * Cryptography
    * Transaction Authentication
    * zkLogin
    * Passkey
    * Checkpoint Verification
  * Sui Architecture
  * Tokenomics
  * Research Papers


  *   * Cryptography


On this page
# Cryptography
Cryptographic agility is core to Sui. The system supports multiple cryptography algorithms and primitives and can switch between them rapidly. With Sui, you can choose the right cryptography solution for your system and implement the latest algorithms as they become available.
Sui defines its cryptography primitives, such as public key, signature, aggregated signature, and hash functions, under one unified type alias or enum wrapper that is shared across the entire repository. Making changes to these primitives affects all of an application's components. You can quickly update application cryptography and be assured of uniform security.
## Transaction Authentication​
Transaction authentication features on Sui provide security against unauthorized access to on-chain data. Transaction Authentication provides an overview of related topics.
Go to Transaction Authentication.
## zkLogin​
zkLogin is a Sui primitive that enables you to send transactions from a Sui address using an OAuth credential, without publicly linking the two.
Go to zkLogin.
## Passkey​
Sui supports the passkey signature scheme that enables you to sign-in to apps and sign transactions for Sui using a private key securely stored on a passkey authenticator. It uses the WebAuthn standard.
Go to Passkey.
## Related links​
  * Cryptography guides: See the cryptography guides for instruction on applying these concepts.


Previous
Gaming on Sui
Next
Transaction Authentication
  * Transaction Authentication
  * zkLogin
  * Passkey
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
