![The Sui Blog](https://blog.sui.io/content/images/2023/04/SuiFoundation_Logo_DarkBlue-1.png)
  * Sui.io
  * Home
  * About
  * Contribute an Article


Move
# Announcing the Move Registry (MVR): Radical Interoperability
![Mysten Labs](https://blog.sui.io/content/images/2023/11/MystenLabs_Logomark_Red-4.png)
####  Mysten Labs
Apr 24, 2025 4 min
The Move Registry (MVR) brings powerful onchain package management to Sui, making smart contracts easier to discover, trust, and integrate.
![Announcing the Move Registry \(MVR\): Radical Interoperability](https://blog.sui.io/content/images/size/w1200/2025/04/04-03-Blog-Header.png)
Big news for Sui, the _Move Registry (MVR)_ is here. MVR is a full-featured onchain package management system that improves discoverability, trust, and interoperability across the ecosystem. Sui is already one of the most interoperable chains, with the _Move language_ and _Programmable Transaction Blocks (PTBs)_ making it simple and easy for Sui builders to take advantage of an ever-expanding ecosystem. And with MVR, that interoperability just got a whole lot more powerful.
If you’ve used tools like _npm_ or _crates.io_, you’ll recognize some familiar concepts. MVR brings similar capabilities to Sui, including versioning, dependency resolution, and metadata linking. It also improves transparency, surfacing real usage data that shows at a glance how packages are actually being used.
Built specifically for Sui, MVR allows developers to manage packages through human-readable names, switch seamlessly between testnet and mainnet, and choose between locking to specific versions or following the latest updates. And because it leverages SuiNS under the hood, every package name is verifiable, persistent, and owned onchain.
## Why MVR matters for the ecosystem
For developers and non-developers alike, MVR is an important step toward a more transparent and user-friendly ecosystem. In the past, integrating or understanding a blockchain-based app often meant dealing with long, cryptic object addresses. These addresses were hard to read and easy to mishandle, especially when developers needed to update packages or move between testnet and mainnet environments. Wrangling sets of opaque identifiers is a job for computers, not humans. 
With MVR, that complexity fades into the background. Developers can now refer to packages using clear names like _@deepbook/core_, making source code easier to understand and maintain. At the same time, users and ecosystem participants benefit from increased transparency around which packages are being used, who maintains them, and how widely they’re adopted. All of this contributes to greater trust and a more open development environment.
While MVR builds on SuiNS for naming and ownership, it goes far beyond simple name to address resolution. It introduces a system for managing package versions, surfacing trust signals, and tracking onchain usage, features that transform it into a true registry, not just a directory. Ultimately, MVR will be the home for all metadata about Sui packages, where maintainers, auditors, and community members can collaborate to curate and improve the Sui open-source ecosystem. 
## A simpler way to build with Move
MVR is designed with interoperability in mind. Sui’s object-centric architecture and the Move Language already encourage developers to leverage Sui’s powerful interoperability. MVR enhances that by streamlining how dependencies are managed.
Instead of copying package addresses into every configuration file and updating them manually with every change, developers can use a single name and rely on MVR to resolve it to the appropriate address. They can choose to reference the latest version of a package for ongoing updates or lock to a specific version for stability. Switching between testnet and mainnet versions of a package becomes as simple as flipping a network setting, no more editing code just to test in a new environment.
If you’re a front-end developer, you might be feeling left out right now, but don’t worry: MVR brings radical interoperability for everyone. Package names can be used directly when constructing PTBs or running read queries, eliminating annoying churn edits, reducing confusion about what code you’re actually calling, and making your code completely straightforward for onboarding developers.
```
const transaction = new Transaction();
 
// testnet
// Notice how the suifren type has a V1 outer package id, and a V2 inner type package id,
// even if they are part of the same package upgrades.
transaction.moveCall({
    target: `0xe177697e191327901637f8d2c5ffbbde8b1aaac27ec1024c4b62d1ebd1cd7430::accessories::equip`,
    arguments: [..],
    typeArguments: [
        `0x80d7de9c4a56194087e0ba0bf59492aa8e6a5ee881606226930827085ddf2332::suifren::SuiFren<0x297d8afb6ede450529d347cf9254caeea2b685c8baef67b084122291ebaefb38::bullshark::Bullshark>`
    ]
});
 
// mainnet
transaction.moveCall({
    target: `0x54800ebb4606fd0c03b4554976264373b3374eeb3fd63e7ff69f31cac786ba8c::accessories::equip`,
    arguments: [..],
    typeArguments: [
        `0xee496a0cc04d06a345982ba6697c90c619020de9e274408c7819f787ff66e1a1::suifren::SuiFren<0x8894fa02fc6f36cbc485ae9145d05f247a78e220814fb8419ab261bd81f08f32::bullshark::Bullshark>`
    ]
});
```

Source code before MVR
```
const transaction = new Transaction();
 
// Now we can use `@suifrens/core` across all package upgrades for type reference.
// And we also have the guarantee to call the latest version of the accessories package.
transaction.moveCall({
    target: `@suifrens/accessories::accessories::equip`,
    arguments: [..],
    typeArguments: [
        `@suifrens/core::suifren::SuiFren<@suifrens/core::bullshark::Bullshark>`
    ]
})
```

Source code with MVR
But MVR is bigger than just code publishing, managing dependencies, and reducing annoying development churn. MVR is the onchain home for all metadata about Sui packages, including source code, maintainer contact info, even icons. You as the maintainer are the owner and sovereign of your metadata in MVR. It’s more than a naming tool - we are building a decentralized map of all code on Sui.
Our vision is for MVR to be the home of all valuable information about packages on Sui. One of the most important facts about a package is usage. All this information exists onchain, but has been illegible until MVR. Soon, we’ll be revealing this information to showcase which packages in the Sui ecosystem are the most popular to build upon in the form of a global MVR Leaderboard that will highlight the packages that are powering our ecosystem. This includes both direct calls and the indirect linkage relationships, showcasing for the first time the contributions of authors of library and utility packages, and giving the builders laying the foundation for our whole ecosystem to build upon the credit they deserve.
## Built for trust, transparency, and growth
Because MVR surfaces real usage data, not just download counts or GitHub stars, it gives developers and users more confidence in the packages they choose. Maintainers can associate metadata like source repositories, websites, or contact information with their packages, making it easier to verify authenticity and respond quickly to issues if they arise. This also helps prevent malicious clones and gives the community a clearer picture of which packages are actively maintained.
MVR is more than a developer tool—it’s infrastructure for a radically interoperable world. It’s about creating the onchain bazaar—a true commons, where open-source code can be shared, reused, and trusted at scale.
## Get started
If you’re ready to explore, the best place to begin is the _Move Registry Portal_. There, you can register a package name, browse existing packages, and start integrating named dependencies into your apps. The _Move Registry Docs_ provide everything you need to start building with MVR today, whether you’re just getting started or migrating an existing codebase.
For a step-by-step walkthrough, check out the _Onboarding Guide_.
## Help build the Move Registry
To Move developers: if you maintain a package on Sui, now’s the time to _register it_. Using named packages improves the developer experience for everyone and helps make your code more accessible to the community.
To teams working with partners: consider MVR as part of your mainnet launch playbook. Helping partners register their packages not only improves discoverability, but it also reinforces good open-source practices and strengthens the entire ecosystem.
MVR is here to remove unnecessary friction and help interoperability flourish on Sui. Let’s build this next layer of open infrastructure, together.
#### Read next
![New Move CLI Flag Gives Enhanced Error Context](https://blog.sui.io/content/images/size/w720/2025/02/CLI-flag.png)
### New Move CLI Flag Gives Enhanced Error Context
Developers using the new error flag in Sui 1.42 will have an easier time debugging code.
Jordan Jennings Feb 14, 2025
![Registration Now Open for Sui Overflow 2025, Sui's Premier Global Hackathon](https://blog.sui.io/content/images/size/w720/2025/02/Overflow-2025-reg.png)
### Registration Now Open for Sui Overflow 2025, Sui's Premier Global Hackathon
Teams and individuals can register for the eight week hackathon, which runs from April into May.
Sui Foundation Feb 12, 2025
![Move 2024: Macro Functions Guide](https://blog.sui.io/content/images/size/w720/2024/08/Macros-move-2024.png)
### Move 2024: Macro Functions Guide
Move 2024 beta edition now gives developers the ability to replace common loops with macro functions.
Mysten Labs Aug 28, 2024
  * Sui.io


The Sui Blog © 2025. Powered by Ghost
English
  * 한국어
  * 中文 (简体)
  * Tiếng Việt
  * 日本語


