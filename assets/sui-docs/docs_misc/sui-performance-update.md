![The Sui Blog](https://blog.sui.io/content/images/2023/04/SuiFoundation_Logo_DarkBlue-1.png)
  * Sui.io
  * Home
  * About
  * Contribute an Article


# Sui Performance Update
![Sui Foundation](https://blog.sui.io/content/images/2023/04/Sui_Droplet_Logo_Blue-3.png)
####  Sui Foundation
Apr 27, 2023 5 min
Sui has performed a series of tests to determine current peak throughput on various workloads as well as time to finality.
![Sui Performance Update](https://blog.sui.io/content/images/size/w1200/2023/04/BlogHeader-Performance.jpg)
## Key Results
  * A Sui network with 100 globally distributed validators achieved peak throughput ranging from 10,871 TPS to 297,000 TPS on various workloads
  * Sui’s time to finality is ~480 milliseconds


## The Journey
A little more than a year ago, Sui was announced to the world along with a single-validator, batched performance demonstration of 120,000 transactions-per-second (TPS) at peak running on an 8-core M1 Macbook Pro. Now that a long-lived, decentralized, and permissionless Testnet has launched, it's time to share the latest on Sui’s performance. This update is intended to
  * Characterize performance levels of the current version of the Sui protocol
  * Determine the next area of optimizations for the protocol
  * Provide the community with a baseline on what can be expected from Sui today and in the future


In order to achieve high-fidelity and realistic performance results, this performance characterization was conducted using a globally-distributed setup closely mirroring Mainnet in terms of hardware configurations, number of validators, geographic distribution of validators, and voting power distribution:
![](https://blog.sui.io/content/images/2023/04/data-src-image-9e98a25a-f252-40a3-8c88-fc92297a63ad.png)![](https://blog.sui.io/content/images/2023/04/data-src-image-78e010f4-d3c4-4ca4-8a61-c4702215b7d3.png)
  * 100 validators
  * The validator hardware configuration used is 24-core AMD, 256GB memory, and 25Gbps NIC
  * A scalable load generator was specifically developed for this exercise
  * Public Testnet was not used in order to avoid disruptions to ongoing development activities. Several short-duration performance stress tests at >100,000+ TPS were conducted on public Testnet.


## Measuring Sui’s Throughput
Before describing the results of this performance characterization, it is important to first establish how Sui’s throughput should be measured in a way that is both comparable to other blockchains and indicative of **Sui’s computational utility**. 
One of Sui’s most powerful core developer primitives is Programmable Transaction Blocks (PTB). For conventional blockchains, the fundamental unit of execution is a _transaction_ which is typically simplistic and close to the VM execution. On Sui, the fundamental, atomic unit of execution is elevated to the level of a complex, composable _sequence of transactions_ where
  * Any public on-chain Move function across all smart contracts is accessible to the Programmable Transaction Block
  * Typed outputs from earlier on-chain Move calls can be chained as typed inputs to later on-chain Move calls. These types can be arbitrary Sui objects that carry a rich set of attributes and properties. PTB can be highly heterogeneous. A single PTB can extract a **Player** object from a smart contract wallet, use it to make a move in a **Game** , then send a **Badge** object won by the move to a multi-game **TrophyCase** , _all without publishing any new smart contract code_. The natural compositionality of PTB allow existing contracts to seamlessly interoperate with both old and new code (e.g. the **Game** does not have to know/care that the user stores their **Player** in a multisig wallet or their **Badge** in a **TrophyCase**)
  * Chained transactions in a PTB execute and fail atomically. Here is an example of a DeFi-related PTB with 12 operations that performs 5 swaps across 3 distinct pools, mutating 20 existing objects and creating 7 new ones in the process.
  * Each PTB supports up to 1024 transactions which makes for both unbounded expressivity and efficiency. PTB can be used both for homogenous batching (e.g, for payments or NFT mints) and heterogeneous chains of single-sender operations like the two examples above. Both modes leverage Sui's high-speed execution and allow users to push already low transaction fees even lower by packing more productive work into a single PTB.


Due to Programmable Transaction Blocks’ convenience and power, developers on Sui are constructing increasingly sophisticated Programmable Transaction Blocks that are customized for their applications. Sui’s programmability was highly expressive even before PTB, but now _a single execution can perform up to 1024 heterogeneous operations_ , each of which would otherwise be an individual transaction on most other blockchains. Although this feature has only been live in Sui public Testnet for about one month, Sui developers are already exploring a variety of PTB sizes, even in the range of 500 - 1000 (example 1, example 2, example 3). The following graph illustrates the current distribution of PTB Size on Testnet: 
![](https://blog.sui.io/content/images/2023/04/PTB_Size.jpg)
While this early adoption is highly promising of future heterogeneous PTB usage to come, it creates an interesting dilemma for measuring or discussing _throughput, particularly as Programmable Transaction Blocks become larger and more advanced over time_.
_Transactions Per Second (TPS)_ is routinely used as a proxy for the theoretical capacity of a blockchain protocol. However, measuring the number of programmable transaction blocks executed per second is an inconsistent measure of Sui's computational capacity—if the average PTB increases in size, Sui’s throughput is increasing, but PTB/second would remain flat. **An effective throughput metric should capture the amount of computational utility Sui can deliver in a given unit of time, not how that computation is partitioned across executions.** In addition, the metric should be useful to track over time as the system continues to be optimized.
The _TPS_ capacity measurement most consistent with Sui’s design, least application-dependent, and most practical to track, is the number of individual transactions within a Programmable Transaction Block executed per second. For this and future updates, all mentions and measurements of TPS follow this convention.
## The Numbers
Experimental workloads with different numbers of homogenous transactions (referred to as _PTB Size_ below) in each Programmable Transaction Block were conducted. The homogeneous transactions are payments: each creates **N****N** participants would be identical in terms of object creations and transfers.
![](https://blog.sui.io/content/images/2023/04/TPS-vs.-PTB-Size.jpg)![](https://blog.sui.io/content/images/2023/04/WorkloadSummary.png)
## Time to Finality
In the blockchain space, finality is commonly understood as the point in the transaction lifecycle where a transaction is considered irrevocable, and can no longer be modified or reverted. 
For this performance update, the Time to Finality measures the point in the transaction lifecycle where both the transaction itself as well as the effects of the transaction are final, and can be used in subsequent transactions. 
  
| 50th Percentile Latency | 95th Percentile Latency  
---|---|---  
Time to Finality  | ~480 milliseconds | ~550 milliseconds  
## What’s Next
The Sui protocol has come a long way from its inception and has shown promising early performance results. Yet there are still many opportunities for optimization and scalability. In the near future, the following elements will be refined on Sui:
  * Scalability and coverage of benchmark tooling
  * Horizontal scalability to support intra-validator scaling across multiple machines
  * Resilience to under-performance of individual validators


As the protocol evolves and Sui’s performance elevates across more dimensions, more updates will be shared with the broader community for consideration and feedback.
  * Sui.io


The Sui Blog © 2025. Powered by Ghost
English
  * 한국어
  * 中文 (简体)
  * Tiếng Việt
  * 日本語


