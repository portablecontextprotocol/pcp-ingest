Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search
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
  * Sui Archives


On this page
# Sui Archives
A Sui archive is a history of all transaction data on Sui. In some cases, peer nodes may not catch up with all transactions and effects through synchronization if they lag behind the current epoch by more than the latest few epochs. In such cases, instead of relying on synchronization, peer nodes can fallback to downloading the relevant information from an archive.
Starting with the 1.49 release, the existing special archive format is being deprecated in favor of a generic data ingestion format. Please migrate your configs using the configuration example that follows. The deprecated configuration is currently included for reference, but will be removed after a few releases.
## Set up archival fallback (latest)​
To enable your node to fallback to an archive in case of lag, add this to your fullnode.yaml file:
  * Mainnet
  * Testnet


```
state-archive-read-config:  
-ingestion-url:"https://checkpoints.mainnet.sui.io"  
# How many objects to read ahead when catching up  
concurrency:5  

```

```
state-archive-read-config:  
-ingestion-url:"https://checkpoints.testnet.sui.io"  
# How many objects to read ahead when catching up  
concurrency:5  

```

## Set up archival fallback(deprecated)​
  * Amazon S3
  * Google Cloud Storage


```
state-archive-read-config:  
-object-store-config:  
object-store:"S3"  
# Use mysten-testnet-archives for testnet  
# Use mysten-mainnet-archives for mainnet  
bucket:"mysten-<testnet|mainnet>-archives"  
# you can either provide your own aws credentials via "aws-secret-access-key" and  
# "aws-access-key-id" or set no-sign-request: true  
no-sign-request:true  
aws-region:"us-west-2"  
object-store-connection-limit:20  
concurrency:5  
# Whether to prune local state based on latest checkpoint in archive.  
# This should stay false for most use cases  
use-for-pruning-watermark:false  

```

```
state-archive-read-config:  
-object-store-config:  
object-store:"GCS"  
# Use mysten-mainnet-archives for mainnet  
# Notice there is no archive bucket setup for testnet in GCS  
bucket:"mysten-<testnet|mainnet>-archives"  
# Use your gcloud service account credentials  
google-service-account:"</path/to/service/account/credentials>"  
object-store-connection-limit:20  
# How many objects to read ahead when catching up  
concurrency:5  
# Whether to prune local state based on latest checkpoint in archive.  
# This should stay false for most use cases  
use-for-pruning-watermark:false  

```

Previous
Database Snapshots
Next
Node Tools
  * Set up archival fallback (latest)
  * Set up archival fallback(deprecated)


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
