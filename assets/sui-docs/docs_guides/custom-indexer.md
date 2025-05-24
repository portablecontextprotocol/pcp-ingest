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
      * Migrating to Move 2024
      * Custom Indexer
      * On-Chain Randomness
      * Querying Sui RPC with GraphQL (Alpha)
      * Migrating to GraphQL (Alpha)
      * Object-Based Local Fee Markets
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Advanced Topics
  * Custom Indexer


On this page
# Custom Indexer
Refer to Access Sui Data for an overview of options to access Sui network data.
You can build custom indexers using the Sui micro-data ingestion framework. To create an indexer, you subscribe to a checkpoint stream with full checkpoint content. This stream can be one of the publicly available streams from Mysten Labs, one that you set up in your local environment, or a combination of the two.
Establishing a custom indexer helps improve latency, allows pruning the data of your Sui Full node, and provides efficient assemblage of checkpoint data.
## Interface and data format​
To use the framework, implement a basic interface:
```
#[async_trait]  
traitWorker:Send+Sync{  
asyncfnprocess_checkpoint(&self, checkpoint:&CheckpointData)->Result<()>;  
}  

```

In this example, the `CheckpointData` struct represents full checkpoint content. The struct contains checkpoint summary and contents, as well as detailed information about each individual transaction. The individual transaction data includes events and input/output objects. The full definition for this content is in the full_checkpoint_content.rs file of the `sui-types` crate.
See the Source code for an implementation section for a complete code example.
## Checkpoint stream sources​
Data ingestion for your indexer supports several checkpoint stream sources.
### Remote reader​
The most straightforward stream source is to subscribe to a remote store of checkpoint contents. Mysten Labs provides the following buckets:
  * Testnet: `https://checkpoints.testnet.sui.io`
  * Mainnet: `https://checkpoints.mainnet.sui.io`


The checkpoint files are stored in the following format: `https://checkpoints.testnet.sui.io/<checkpoint_id>.chk`. You can download the checkpoint file by sending an HTTP GET request to the relevant URL. Try it yourself for checkpoint 1 at https://checkpoints.testnet.sui.io/1.chk.
External
  
Indexer  
daemon
The Sui data ingestion framework provides a helper function to quickly bootstrap an indexer workflow.
examples/custom-indexer/rust/remote_reader.rs
```
useanyhow::Result;  
useasync_trait::async_trait;  
usesui_data_ingestion_core::{setup_single_workflow,Worker};  
usesui_types::full_checkpoint_content::CheckpointData;  
  
structCustomWorker;  
  
#[async_trait]  
implWorkerforCustomWorker{  
typeResult=();  
asyncfnprocess_checkpoint(&self, checkpoint:&CheckpointData)->Result<()>{  
// custom processing logic  
// print out the checkpoint number  
println!(  
"Processing checkpoint: {}",  
						checkpoint.checkpoint_summary.to_string()  
);  
Ok(())  
}  
}  
  
#[tokio::main]  
asyncfnmain()->Result<()>{  
let(executor, term_sender)=setup_single_workflow(  
CustomWorker,  
"https://checkpoints.testnet.sui.io".to_string(),  
0,/* initial checkpoint number */  
5,/* concurrency */  
None,/* extra reader options */  
)  
.await?;  
		executor.await?;  
Ok(())  
}  

```

This is suitable for setups with a single ingestion pipeline where progress tracking is managed outside of the framework.
### Local reader​
Colocate the data ingestion daemon with a Full node and enable checkpoint dumping on the latter to set up a local stream source. After enabling, the Full node starts dumping executed checkpoints as files to a local directory, and the data ingestion daemon subscribes to changes in the directory through an inotify-like mechanism. This approach allows minimizing ingestion latency (checkpoint are processed immediately after a checkpoint executor on a Full node) and getting rid of dependency on an externally managed bucket.
To enable, add the following to your Full node configuration file:
```
checkpoint-executor-config:  
checkpoint-execution-max-concurrency:200  
local-execution-timeout-sec:30  
data-ingestion-dir: <path to a local directory>  

```

Sui
Cloud storage
  
Indexer  
daemon
examples/custom-indexer/rust/local_reader.rs
```
usetokio::sync::oneshot;  
useanyhow::Result;  
useasync_trait::async_trait;  
usesui_types::full_checkpoint_content::CheckpointData;  
use sui_data_ingestion_core as sdic;  
usesdic::{Worker,WorkerPool,ReaderOptions};  
usesdic::{DataIngestionMetrics,FileProgressStore,IndexerExecutor};  
useprometheus::Registry;  
usestd::path::PathBuf;  
usestd::env;  
  
structCustomWorker;  
  
#[async_trait]  
implWorkerforCustomWorker{  
typeResult=();  
asyncfnprocess_checkpoint(&self, checkpoint:&CheckpointData)->Result<()>{  
// custom processing logic  
println!("Processing Local checkpoint: {}", checkpoint.checkpoint_summary.to_string());  
Ok(())  
}  
}  
  
#[tokio::main]  
asyncfnmain()->Result<()>{  
let concurrency =5;  
let(exit_sender, exit_receiver)=oneshot::channel();  
let metrics =DataIngestionMetrics::new(&Registry::new());  
let backfill_progress_file_path =  
env::var("BACKFILL_PROGRESS_FILE_PATH").unwrap_or("/tmp/local_reader_progress".to_string());  
let progress_store =FileProgressStore::new(PathBuf::from(backfill_progress_file_path));  
letmut executor =IndexerExecutor::new(progress_store,1/* number of workflow types */, metrics);  
let worker_pool =WorkerPool::new(CustomWorker,"local_reader".to_string(), concurrency);  
  
		executor.register(worker_pool).await?;  
		executor.run(  
PathBuf::from("./chk".to_string()),// path to a local directory  
None,  
vec![],// optional remote store access options  
ReaderOptions::default(),/* remote_read_batch_size */  
				exit_receiver,  
).await?;  
Ok(())  
}  

```

Let's highlight a couple lines of code:
```
let worker_pool =WorkerPool::new(CustomWorker,"local_reader".to_string(), concurrency);  
executor.register(worker_pool).await?;  

```

The data ingestion executor can run multiple workflows simultaneously. For each workflow, you need to create a separate worker pool and register it in the executor. The `WorkerPool` requires an instance of the `Worker` trait, the name of the workflow (which is used for tracking the progress of the flow in the progress store and metrics), and concurrency.
The concurrency parameter specifies how many threads the workflow uses. Having a concurrency value greater than 1 is helpful when tasks are idempotent and can be processed in parallel and out of order. The executor only updates the progress/watermark to a certain checkpoint when all preceding checkpoints are processed.
### Hybrid mode​
Specify both a local and remote store as a fallback to ensure constant data flow. The framework always prioritizes locally available checkpoint data over remote data. It's useful when you want to start utilizing your own Full node for data ingestion but need to partially backfill historical data or just have a failover.
```
executor.run(  
PathBuf::from("./chk".to_string()),// path to a local directory  
Some("https://checkpoints.testnet.sui.io".to_string()),// Remote Checkpoint Store  
vec![],// optional remote store access options  
ReaderOptions::default(),  
    exit_receiver,  
).await?;  

```

### Manifest​
Code for the cargo.toml manifest file for the custom indexer.
examples/custom-indexer/rust/Cargo.toml
```
[package]  
name="custom-indexer"  
version="0.1.0"  
edition="2021"  
  
[dependencies]  
async-trait="0.1.83"  
tokio={version="1.38.0",features=["full"]}  
sui_types={git="https://github.com/mystenlabs/sui",package="sui-types"}  
sui_data_ingestion_core={git="https://github.com/mystenlabs/sui",package="sui-data-ingestion-core"}  
prometheus="0.13.3"  
anyhow="1.0.86"  
  
[[bin]]  
name="local_reader"  
path="local_reader.rs"  
  
[[bin]]  
name="remote_reader"  
path="remote_reader.rs"  
  
[workspace]  

```

## Source code for an implementation​
Find the following source code in the Sui repo.
examples/custom-indexer/rust/Cargo.toml
```
[package]  
name="custom-indexer"  
version="0.1.0"  
edition="2021"  
  
[dependencies]  
async-trait="0.1.83"  
tokio={version="1.38.0",features=["full"]}  
sui_types={git="https://github.com/mystenlabs/sui",package="sui-types"}  
sui_data_ingestion_core={git="https://github.com/mystenlabs/sui",package="sui-data-ingestion-core"}  
prometheus="0.13.3"  
anyhow="1.0.86"  
  
[[bin]]  
name="local_reader"  
path="local_reader.rs"  
  
[[bin]]  
name="remote_reader"  
path="remote_reader.rs"  
  
[workspace]  

```

examples/custom-indexer/rust/local_reader.rs
```
usetokio::sync::oneshot;  
useanyhow::Result;  
useasync_trait::async_trait;  
usesui_types::full_checkpoint_content::CheckpointData;  
use sui_data_ingestion_core as sdic;  
usesdic::{Worker,WorkerPool,ReaderOptions};  
usesdic::{DataIngestionMetrics,FileProgressStore,IndexerExecutor};  
useprometheus::Registry;  
usestd::path::PathBuf;  
usestd::env;  
  
structCustomWorker;  
  
#[async_trait]  
implWorkerforCustomWorker{  
typeResult=();  
asyncfnprocess_checkpoint(&self, checkpoint:&CheckpointData)->Result<()>{  
// custom processing logic  
println!("Processing Local checkpoint: {}", checkpoint.checkpoint_summary.to_string());  
Ok(())  
}  
}  
  
#[tokio::main]  
asyncfnmain()->Result<()>{  
let concurrency =5;  
let(exit_sender, exit_receiver)=oneshot::channel();  
let metrics =DataIngestionMetrics::new(&Registry::new());  
let backfill_progress_file_path =  
env::var("BACKFILL_PROGRESS_FILE_PATH").unwrap_or("/tmp/local_reader_progress".to_string());  
let progress_store =FileProgressStore::new(PathBuf::from(backfill_progress_file_path));  
letmut executor =IndexerExecutor::new(progress_store,1/* number of workflow types */, metrics);  
let worker_pool =WorkerPool::new(CustomWorker,"local_reader".to_string(), concurrency);  
  
		executor.register(worker_pool).await?;  
		executor.run(  
PathBuf::from("./chk".to_string()),// path to a local directory  
None,  
vec![],// optional remote store access options  
ReaderOptions::default(),/* remote_read_batch_size */  
				exit_receiver,  
).await?;  
Ok(())  
}  

```

examples/custom-indexer/rust/remote_reader.rs
```
useanyhow::Result;  
useasync_trait::async_trait;  
usesui_data_ingestion_core::{setup_single_workflow,Worker};  
usesui_types::full_checkpoint_content::CheckpointData;  
  
structCustomWorker;  
  
#[async_trait]  
implWorkerforCustomWorker{  
typeResult=();  
asyncfnprocess_checkpoint(&self, checkpoint:&CheckpointData)->Result<()>{  
// custom processing logic  
// print out the checkpoint number  
println!(  
"Processing checkpoint: {}",  
						checkpoint.checkpoint_summary.to_string()  
);  
Ok(())  
}  
}  
  
#[tokio::main]  
asyncfnmain()->Result<()>{  
let(executor, term_sender)=setup_single_workflow(  
CustomWorker,  
"https://checkpoints.testnet.sui.io".to_string(),  
0,/* initial checkpoint number */  
5,/* concurrency */  
None,/* extra reader options */  
)  
.await?;  
		executor.await?;  
Ok(())  
}  

```

## Related links​
  * Sui internal example: Sui data ingestion daemon that runs internal pipelines.
  * Production example: Sui Name Service custom indexer.
  * Using Events: Events in Sui enable you to monitor on-chain activity in near-real time when coupled with a custom indexer.


Previous
Migrating to Move 2024
Next
On-Chain Randomness
  * Interface and data format
  * Checkpoint stream sources
    * Remote reader
    * Local reader
    * Hybrid mode
    * Manifest
  * Source code for an implementation
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
