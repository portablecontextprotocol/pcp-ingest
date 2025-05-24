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


On this page
# Contribute to Sui Documentation
As open source software, Sui depends on community contributions. This page covers the process for contributing to Sui's documentation.
To make changes to the documentation, you can fork and clone the Sui repository to your local machine and make changes from your preferred IDE of choice, or by the web interface on GitHub. This guide covers both scenarios.
## Style guide compliance​
All changes to the documentation must follow the style guide, as well as the review process and information on the editors throughout the process. Do not be offended by the number of change requests your docs PR might receive. This is not a reflection on your writing abilities, but an effort to keep a consistent tone across the documentation set. Depending on reviewer and workload, some reviews are more thorough than others. After your PR merges, your content might be changed at a later date to align better with Sui writing standards.
To create more engaging content, be sure to follow these rules in particular:
  * Always prefer active voice.
  * Present tense verbs are almost always the right choice.
  * Be concise. Use only the words strictly necessary to convey an idea.


## Set up local environment​
Cloning the documentation locally is recommended when you are creating larger, more significant changes to the docs. See Sui Environment Setup for instructions on forking the Sui repository, if necessary. The documentation is in the `docs/content` directory.
  1. If you are using the recommended Visual Studio Code IDE, install Prettier to ensure that your formatting is consistent.
  2. After you make all your changes, stage all files with changes (`git add .` to add all modified files), create a local commit (`git commit -m “message”`), and then push all your changes to your forked repository (`git push`).
  3. To view your changes via `localhost`, enter `pnpm install` into a terminal at the `docs/site` directory to install dependencies, then `pnpm start` to view the changes on `localhost:3000` to ensure that the website works as intended. You might need to install the `pnpm` package manager if you don't already have it.


## For beginners​
Editing the documentation via the GitHub web interface is recommended if you are not familiar with working in an IDE, or for smaller changes and fixes.
**Add New Page**
Navigate to the `docs/content` directory, then navigate to the appropriate subdirectory and click the `Add file` button in the top-right. Select `create new file` to create a new file and edit it directly on GitHub's web interface.
**Change Existing Page**
To change an existing page, navigate to the file you want to edit, click on the pencil icon in the top-right, and edit your changes there.
## Review process​
When you are finished creating your changes in your own fork or using the web interface, submit a PR to the Sui repository. When you do so, you can view the deployment on Vercel and double-check that everything behaves the way you intend. For every unique commit in a PR, Vercel generates a new preview. A reviewer then takes responsibility for providing clear and actionable feedback to your PR. As the owner of the PR, it is your responsibility to modify your PR to address the feedback that has been provided to you by the reviewer. Keep in mind that you may receive feedback from multiple reviewers. After a reviewer has approved your PR, it is merged into `main` and your contributions are made public.
Previous
Glossary
Next
Sui Environment Setup
  * Style guide compliance
  * Set up local environment
  * For beginners
  * Review process


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
