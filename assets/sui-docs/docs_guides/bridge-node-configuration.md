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
  * Sui Bridge Node Configuration


On this page
# Sui Bridge Validator Node Configuration
Running a Bridge Validator Node (Bridge Node) requires registering your node with the bridge committee. Correct configuration of your node ensures optimal performance and valid metrics data. Follow this topic to make sure your Bridge Node is set up properly.
## Prerequisites​
To set up and run a Bridge Node, you need to install `sui` and `sui-bridge-cli`. You can install them using one of the following options:
Install from tip of `main`:
```
$ cargo install --locked --git "https://github.com/MystenLabs/sui.git" sui sui-bridge-cli  

```

Install with a commit sha:
```
$ cargo install --locked --git "https://github.com/MystenLabs/sui.git" --rev {SHA} sui sui-bridge-cli  

```

## Committee registration​
To join the network you must first register with the bridge validator committee.
### Prepare for metadata​
The required metadata includes two things:
  * `BridgeAuthorityKey`, an ECDSA key to sign messages. Because this is a hot key that is kept in memory, it’s fine to use the following tool to generate one and write it to file.
  * A REST API URL where the Bridge Node listens to and serves requests. Example: `https://bridge.example-sui-validator.io:443`. Make sure the port is correct and the URL does not contain any invalid characters, like quotes for example.


To create a `BridgeAuthorityKey`, run
```
$ sui-bridge-cli create-bridge-validator-key <PATH-TO-WRITE>  

```

where `<PATH-TO-WRITE>` is the location to write the key pair to.
It's highly recommended you create a new key pair in a secure environment (for example, in the same machine where your node runs) to avoid key compromise.
### Registration​
After you have both authority key file and REST API URL ready, you can register them by using Sui CLI:
```
$ sui validator register-bridge-committee --bridge-authority-key-path <BRIDGE-AUTHORITY-KEY-PATH> --bridge-authority-url <BRIDGE-AUTHORITY-URL>  

```

#### Offline signing​
If you keep your validator account key in cold storage or you want to perform offline signing, use flags `--print-only` and `--validator-address` (with the value for the validator address). This prints serialized unsigned transaction bytes, then you can use your preferred signing process to produce signed bytes.
Run the following command to execute it:
```
$ sui client execute-signed-tx  

```

#### Update metadata (before committee is finalized)​
Both key and URL are changeable **before the committee is finalized**. If you wish to update metadata, simply rerun `sui validator register-bridge-committee`.
#### View registered metadata​
To double check you registered the correct metadata on chain, run
```
$ sui-bridge-cli view-bridge-registration --sui-rpc-url {SUI-FULLNODE-URL}  

```

## Update metadata (after committee is finalized)​
Use the following command to update bridge node URL:
```
$ sui validator update-bridge-committee-node-url  

```

Refer to offline signing section in this page for how to sign the transaction offline.
Authoritiy key rotation is not supported yet.
## Bridge Node​
You have several options when configuring your Bridge Node for performance and metrics monitoring. Follow the instructions that follow to configure your node for best results in your environment.
### Bridge Node hardware requirements​
Suggested hardware requirements:
  * CPU: 6 physical cores
  * Memory: 16GB
  * Storage: 200GB
  * Network: 100Mbps


### WAF protection for Bridge Node​
To protect against distributed denial of service (DDoS) attacks and similar attacks intended to expend validator resources, you must provide rate limit protection for the bridge server.
In addition to protection, this gives node operators fine-grained control over the rate of requests they receive, and observability into those requests.
The currently recommended rate limit is `50 requests/second per unique IP`.
#### Web application firewall (WAF) options​
You can use a managed cloud service, for example:
  * Cloudflare WAF
  * AWS WAF
  * GCP Cloud Armor


It's also possible to use an open source load balancer, such as HAProxy for a practical, IP-based rate limit.
A shortened example HAProxy configuration looks like the following:
```
frontend http-in  
    bind *:80  
    # Define an ACL to count requests per IP and block if over limit  
    acl too_many_requests src_http_req_rate() gt 50  
    # Track the request rate per IP  
    stick-table type ip size 1m expire 1m store http_req_rate(1s)  
    # Check request rate and deny if the limit is exceeded  
    http-request track-sc0 src  
    http-request deny if too_many_requests  
  
    default_backend bridgevalidator  
  
backend bridgevalidator  
    # Note the port needs to match the value in Bridge Node config, default is 9191  
    server bridgevalidator 0.0.0.0:9191  

```

If choosing to use an open source load balancing option, make sure to set up metrics collection and alerting on the service.
### Bridge Node config​
Use `sui-bridge-cli` command to create a template. If you want to run `BridgeClient` (see the following section), pass `--run-client` as a parameter.
```
$ sui-bridge-cli create-bridge-node-config-template {PATH}  
$ sui-bridge-cli create-bridge-node-config-template --run-client {PATH}  

```

The generated configuration includes the following parameters:
Parameter | Description  
---|---  
`server-listen-port` | The port that Bridge Node listens to for handling requests.  
`metrics-port` | Port to export Prometheus metrics.  
`bridge-authority-key-path` | The path to the Bridge Validator key, generated from `sui-bridge-cli create-bridge-validator-key` command referenced previously.  
`run-client` | Whether Bridge Client should be enabled in Bridge Node (more instructions follow).  
`approved-governance-actions` | A list of governance actions that you want to support.  
`sui:sui-rpc-url` | Sui RPC URL.  
`sui:sui-bridge-chain-id` |  `0` for Sui Mainnet, `1` for Sui Testnet.  
`eth:eth-rpc-url` | Ethereum RPC URL.  
`eth:eth-bridge-proxy-address` | The proxy address for Bridge Solidity contracts on Ethereum.  
`eth:eth-bridge-chain-id` |  `10` for Ethereum Mainnet, `11` for Sepolia Testnet.  
`eth:eth-contracts-start-block-fallback` | The starting block BridgeNodes queries for from Ethereum FullNode. This number should be the block where Solidity contracts are deployed or slightly before.  
`metrics:push-url` | The url of the remote Sui metrics pipeline (for example, `https://metrics-proxy.[testnet_OR_mainnet].sui.io:8443/publish/metrics`). See the metrics push section that follows for more details.  
With `run-client: true`, you can find these additional fields in the generated config:
Parameter | Description  
---|---  
`db-path` | Path of BridgeClient database, for BridgeClient.  
`sui:bridge-client-key-path` | The file path of Bridge Client key. This key can be generated with `sui-bridge-cli create-bridge-client-key` as previously shown. When `run-client` is true but you do not provide `sui:bridge-client-key-path`, it defaults to use the Bridge Validator key to submit transactions on Sui. This is not recommended for the sake of key separation.  
### Bridge Client​
`BridgeClient` orchestrates bridge transfer requests. It is **optional** to run for a `BridgeNode`. `BridgeClient` submits transaction on the Sui network. Thus when it's enabled, you need a Sui account key with enough SUI balance.
To enable `bridge_client` feature on a `BridgeNode`, set the following parameters in `BridgeNodeConfig`:
```
run-client:true  
db-path: <PATH-TO-DB>  
sui:  
bridge-client-key-path: <PATH-TO-BRIDGE-CLIENT-KEY>  

```

To create a `BridgeClient` key pair, run
```
$ sui-bridge-cli create-bridge-client-key <PATH_TO_BRIDGE_CLIENT_KEY>  

```

This prints the newly created Sui Address. Then we need to fund this address with some SUI for operations.
### Build Bridge Node​
Build or install Bridge Node in one of the following ways:
  * Use `cargo install`.
```
$ cargo install --locked --git "https://github.com/MystenLabs/sui.git" --branch {BRANCH-NAME} sui-bridge  

```

Or
```
$ cargo install --locked --git "https://github.com/MystenLabs/sui.git" --rev {SHA-NAME} sui-bridge  

```

  * Compile from source code
```
$ git clone https://github.com/MystenLabs/sui.git  

```

```
$ cd sui  

```

```
$ git fetch origin {BRANCH-NAME|SHA}  

```

```
$ git checkout {BRANCH-NAME|SHA}  

```

```
$ cargo build --release --bin sui-bridge  

```

  * Use `curl`/`wget` pre-built binaries (for Linux/AMD64 only).
```
$ curl https://sui-releases.s3.us-east-1.amazonaws.com/{SHA}/sui-bridge -o sui-bridge  

```

  * Use pre-built Docker image. Pull from Docker Hub: `mysten/sui-tools:{SHA}`


### Run Bridge Node​
Running Bridge Node is similar to running a Sui node using systemd or Ansible. The command to start the Bridge Node is:
```
$ RUST_LOG=info,sui_bridge=debug sui-bridge --config-path {BRIDGE-NODE-CONFIG-PATH}  

```

### Ingress​
Bridge Node listens for TCP connections over port `9191` (or the preferred port in the configuration file). You must allow incoming connections for that port on the host that is running Bridge Node.
Test ingress with `curl` on a remote machine and expect a `200` response:
```
$ curl -v {YOUR_BRIDGE_URL}  

```

### Bridge Node monitoring​
Use `uptime` to check if the node is running.
You can find a full list of Bridge Node metrics and their descriptions in the `sui-bridge` crate.
#### When `run-client: false`​
In this case Bridge Node runs as a passive observer and does not proactively poll on-chain activities. Important metrics to monitor in this case are the request handling metrics, such as:
  * `bridge_requests_received`
  * `bridge_requests_ok`
  * `bridge_err_requests`
  * `bridge_requests_inflight`
  * `bridge_eth_rpc_queries`
  * `bridge_eth_rpc_queries_latency`
  * `bridge_signer_with_cache_hit`
  * `bridge_signer_with_cache_miss`
  * `bridge_sui_rpc_errors`


#### When `run-client: true`​
In this case, Bridge Client is toggled on and syncs with blockchains proactively. The best metrics to track progress are:
  * `bridge_last_synced_sui_checkpoints`
  * `bridge_last_synced_eth_blocks`
  * `bridge_last_finalized_eth_block`
  * `bridge_sui_watcher_received_events`
  * `bridge_eth_watcher_received_events`
  * `bridge_sui_watcher_received_actions`
  * `bridge_eth_watcher_received_actions`


`bridge_gas_coin_balance` is also a critical metric to track the balance of your client gas coin, and top up after it dips below a certain threshold.
### Metrics push​
The Bridge Nodes can push metrics to the remote proxy for network-level observability.
To enable metrics push, set the following parameters in `BridgeNodeConfig`:
```
metrics:  
push-url: https://metrics-proxy.[testnet|mainnet].sui.io:8443/publish/metrics  

```

The proxy authenticates pushed metrics by using the metrics key pair. It is similar to `sui-node` pushing metrics with `NetworkKey`. Unlike `NetworkKey`, the Bridge Node metrics key is not recorded on chain and can be ephemeral. The metrics key is loaded from the `metrics-key-pair` field in `BridgeNodeConfig` if provided, otherwise a new key pair is generated on the fly. The proxy queries node public keys periodically by hitting the metrics public API key of each node.
When Bridge Node starts, it might log this line once:
```
unable to push metrics: error sending request for url (xyz); new client will be created  

```

This is okay to ignore as long as it does not persist. Otherwise, try:
```
$ curl -i  {your-bridge-node-url-onchain}/metrics_pub_key  

```

and make sure the public key is correctly returned.
Previous
Sui Exchange Integration Guide
Next
Validator Committee
  * Prerequisites
  * Committee registration
    * Prepare for metadata
    * Registration
  * Update metadata (after committee is finalized)
  * Bridge Node
    * Bridge Node hardware requirements
    * WAF protection for Bridge Node
    * Bridge Node config
    * Bridge Client
    * Build Bridge Node
    * Run Bridge Node
    * Ingress
    * Bridge Node monitoring
    * Metrics push


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
