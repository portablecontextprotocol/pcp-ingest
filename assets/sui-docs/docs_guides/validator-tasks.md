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
  * Validator Tasks


On this page
# Validator Tasks
This guide focuses on running the Sui node software as a validator.
## Requirements​
To run a Sui Validator a machine with the following is required:
  * CPU: 24 physical cores (or 48 virtual cores)
  * Memory: 128 GB
  * Storage: 4 TB NVME
  * Network: 1 Gbps


## Deployment​
You can deploy Sui node in a number of ways.
There are pre-built container images available in Docker Hub.
And pre built `linux/amd64` binaries available in S3 that you can fetch using one of the following methods:
```
$ wget https://releases.sui.io/$SUI_SHA/sui-node  

```

```
$ curl https://releases.sui.io/$SUI_SHA/sui-node -o sui-node  

```

To build directly from source:
```
$ git clone https://github.com/MystenLabs/sui.git && cd sui  

```

```
$ git checkout [SHA|BRANCH|TAG]  

```

```
$ cargo build --release --bin sui-node  

```

Configuration and guides are available for the following deployment options:
  * Systemd
  * Ansible
  * Docker Compose


## Configuration​
Sui node runs with a single configuration file provided as an argument, example:
`./sui-node --config-path /opt/sui/config/validator.yaml`.
See Validator for configuration templates.
## Connectivity​
Sui node uses the following ports by default:
protocol/port | reachability | purpose  
---|---|---  
TCP/8080 | inbound | validator/transaction interface  
TCP/8081 | inbound/outbound | consensus interface  
UDP/8084 | inbound/outbound | peer to peer state sync interface  
TCP/8443 | outbound | metrics pushing  
TCP/9184 | localhost | metrics scraping  
To run a validator successfully, it is critical that ports 8080-8084 are open as outlined, including the specific protocol (TCP/UDP).
## Network Buffer​
From load testing Sui validator networks, it has been determined that the default Linux network buffer sizes are too small. We recommend increasing them using one of the following two methods:
### Option 1: With /etc/sysctl.d/​
These settings can be added to a new sysctl file specifically for the sui-node, or appended to an existing file. Modifications made in this way will persist across system restarts.
Create a new sysctl file for the sui-node:
```
$ sudo nano /etc/sysctl.d/100-sui-node.conf  

```

Add these lines to the file, overwriting existing settings if necessary.
```
net.core.rmem_max = 104857600  
net.core.wmem_max = 104857600  
net.ipv4.tcp_rmem = 8192 262144 104857600  
net.ipv4.tcp_wmem = 8192 262144 104857600  

```

Apply the settings immediately, before the next restart
```
$ sudo sysctl --system  

```

### Option 2: With sysctl command​
These modifications do not persist across system restarts. Therefore, the commands should be run each time the host restarts.
```
$ sudo sysctl -w net.core.wmem_max=104857600  

```

```
$ sudo sysctl -w net.core.rmem_max=104857600  

```

```
$ sudo sysctl -w net.ipv4.tcp_rmem="8192 262144 104857600"  

```

```
$ sudo sysctl -w net.ipv4.tcp_wmem="8192 262144 104857600"  

```

### Verification​
To verify that the system settings have indeed been updated, check the output of the following command:
```
$ sudo sysctl -a | egrep [rw]mem  

```

## Storage​
All Sui node related data is stored by default under `/opt/sui/db/`. This is controlled in the Sui node configuration file.
```
$ cat /opt/sui/config/validator.yaml | grep db-path  
  db-path: /opt/sui/db/authorities_db  
  db-path: /opt/sui/db/consensus_db  

```

Ensure that you have an appropriately sized disk mounted for the database to write to.
  * To check the size of the local Sui node databases:


```
$ du -sh /opt/sui/db/  

```

```
$ du -sh /opt/sui/db/authorities_db  

```

```
$ du -sh /opt/sui/db/consensus_db  

```

  * To delete the local Sui node databases:


```
$ sudo systemctl stop sui-node  

```

```
$ sudo rm -rf /opt/sui/db/authorities_db /opt/sui/db/consensus_db  

```

## Key management​
The following keys are used by Sui node:
key | scheme | purpose  
---|---|---  
protocol.key | bls12381 | transactions  
account.key | ed25519 | controls assets for staking  
network.key | ed25519 | state sync  
worker.key | ed25519 | consensus (to be migrated)  
These are configured in the Sui node configuration file.
## Monitoring​
### Metrics​
Sui node exposes metrics via a local HTTP interface. These can be scraped for use in a central monitoring system as well as viewed directly from the node.
  * View all metrics:


```
$ curl -s http://localhost:9184/metrics  

```

  * Search for a particular metric:


```
$ curl http://localhost:9184/metrics | grep <METRIC>  

```

Sui node also pushes metrics to a central Sui metrics proxy.
### Logs​
Logs are controlled using the `RUST_LOG` environment variable.
The `RUST_LOG_JSON=1` environment variable can optionally be set to enable logging in JSON structured format.
Depending on your deployment method, these are configured in the following places:
  * Ansible
  * Native systemd
  * Docker Compose


To view and follow the Sui node logs:
```
$ journalctl -u sui-node -f  

```

To search for a particular match
```
$ journalctl -u sui-node -g <SEARCH_TERM>  

```

  * If using Docker Compose, look at the examples in the README.


It is possible to change the logging configuration while a node is running using the admin interface.
To view the currently configured logging values:
```
$ curl localhost:1337/logging  

```

To change the currently configured logging values:
```
$ curl localhost:1337/logging -d "info"  

```

### Dashboards​
Public dashboard for network wide visibility:
  * Sui Testnet Validators


## Software updates​
When an update is required to the Sui node software the following process can be used. Follow the relevant Systemd or Docker Compose runbook depending on your deployment type. It is highly unlikely that you will want to restart with a clean database.
  * Systemd
  * Docker Compose


## State sync​
Checkpoints in Sui contain the permanent history of the network. They are comparable to blocks in other blockchains with one big difference being that they are lagging instead of leading. All transactions are final and executed prior to being included in a checkpoint.
These checkpoints are synchronized between validators and fullnodes via a dedicated peer to peer state sync interface.
Inter-validator state sync is always permitted however there are controls available to limit what fullnodes are allowed to sync from a specific validator.
The default and recommended `max-concurrent-connections: 0` configuration does not affect inter-validator state sync, but will restrict all fullnodes from syncing. The Sui node configuration can be modified to allow a known fullnode to sync from a validator:
```
p2p-config:  
  anemo-config:  
    max-concurrent-connections: 0  
  seed-peers:  
    - address: <multiaddr>  # The p2p address of the fullnode  
      peer-id: <peer-id>    # hex encoded network public key of the node  
    - address: ...          # another permitted peer  
      peer-id: ...  

```

## Chain operations​
The following chain operations are executed using the `sui` CLI. This binary is built and provided as a release similar to `sui-node`, examples:
```
$ wget https://releases.sui.io/$SUI_SHA/sui  

```

```
$ chmod +x sui  

```

```
$ curl https://releases.sui.io/$SUI_SHA/sui -o sui  

```

```
$ chmod +x sui  

```

It is recommended and often required that the `sui` binary release/version matches that of the deployed network.
### Updating on-chain metadata​
You can leverage Validator Tool to perform majority of the following tasks.
An active/pending validator can update its on-chain metadata by submitting a transaction. Some metadata changes take effect immediately, including:
  * name
  * description
  * image url
  * project url


Other metadata (keys, addresses, and so on) only come into effect at the next epoch.
To update metadata, a validator makes a MoveCall transaction that interacts with the System Object. For example:
  1. to update name to `new_validator_name`, use the Sui Client CLI to call `sui_system::update_validator_name`:


Beginning with the Sui `v1.24.1` release, the `--gas-budget` option is no longer required for CLI commands.
```
$ sui client call --package 0x3 --module sui_system --function update_validator_name --args 0x5 \"new_validator_name\" --gas-budget 10000  

```

  1. to update p2p address starting from next epoch to `/ip4/192.168.1.1`, use the Sui Client CLI to call `sui_system::update_validator_next_epoch_p2p_address`:


```
$ sui client call --package 0x3 --module sui_system --function update_validator_next_epoch_p2p_address --args 0x5 "[4, 192, 168, 1, 1]" --gas-budget 10000  

```

See the full list of metadata update functions here.
### Operation cap​
To avoid touching account keys too often and allowing them to be stored off-line, validators can delegate the operation ability to another address. This address can then update the reference gas price and tallying rule on behalf of the validator.
Upon creating a `Validator`, an `UnverifiedValidatorOperationCap` is created as well and transferred to the validator address. The holder of this `Cap` object (short for "Capability") therefore could perform operational actions for this validator. To authorize another address to conduct these operations, a validator transfers the object to another address that they control. The transfer can be done by using Sui Client CLI: `sui client transfer`.
To rotate the delegatee address or revoke the authorization, the current holder of `Cap` transfers it to another address. In the event of compromised or lost keys, the validator could create a new `Cap` object to invalidate the incumbent one. This is done by calling `sui_system::rotate_operation_cap`:
```
$ sui client call --package 0x3 --module sui_system --function rotate_operation_cap --args 0x5 --gas-budget 10000  

```

By default the new `Cap` object is transferred to the validator address, which then could be transferred to the new delegatee address. At this point, the old `Cap` becomes invalidated and no longer represents eligibility.
To get the current valid `Cap` object's ID of a validator, use the Sui Client CLI `sui client objects` command after setting the holder as the active address.
### Updating the gas price survey quote​
To update the gas price survey quote of a validator, which is used to calculate the reference gas price at the end of the epoch, the sender needs to hold a valid `UnverifiedValidatorOperationCap`. The sender could be the validator itself, or a trusted delegatee. To do so, call `sui_system::request_set_gas_price`:
```
$ sui client call --package 0x3 --module sui_system --function request_set_gas_price --args 0x5 {cap_object_id} {new_gas_price} --gas-budget 10000  

```

### Reporting/un-reporting validators​
To report a validator or undo an existing reporting, the sender needs to hold a valid `UnverifiedValidatorOperationCap`. The sender could be the validator itself, or a trusted delegatee. To do so, call `sui_system::report_validator/undo_report_validator`:
```
$ sui client call --package 0x3 --module sui_system --function report_validator/undo_report_validator --args 0x5 {cap_object_id} {reportee_address} --gas-budget 10000  

```

After a validator is reported by `2f + 1` other validators by voting power, their staking rewards will be slashed.
### Joining the validator set​
In order for a Sui address to join the validator set, they need to first sign up as a validator candidate by calling `sui_system::request_add_validator_candidate` with their metadata and initial configs:
```
$ sui client call --package 0x3 --module sui_system --function request_add_validator_candidate --args 0x5 {protocol_pubkey_bytes} {network_pubkey_bytes} {worker_pubkey_bytes} {proof_of_possession} {name} {description} {image_url} {project_url} {net_address} {p2p_address} {primary_address} {worker_address} {gas_price} {commission_rate} --gas-budget 10000  

```

After an address becomes a validator candidate, any address (including the candidate address itself) can start staking with the candidate's staking pool. Refer to our dedicated staking FAQ on how staking works. Once a candidate's staking pool has accumulated at least `sui_system::MIN_VALIDATOR_JOINING_STAKE` amount of stake, the candidate can call `sui_system::request_add_validator` to officially add themselves to next epoch's active validator set:
```
$ sui client call --package 0x3 --module sui_system --function request_add_validator --args 0x5 --gas-budget 10000000  

```

### Leaving the validator set​
To leave the validator set starting next epoch, the sender needs to be an active validator in the current epoch and should call `sui_system::request_remove_validator`:
```
$ sui client call --package 0x3 --module sui_system --function request_remove_validator --args 0x5 --gas-budget 10000  

```

After the validator is removed at the next epoch change, the staking pool will become inactive and stakes can only be withdrawn from an inactive pool.
## Private security fixes​
There might be instances where urgent security fixes need to be rolled out before publicly announcing it's presence (issues affecting liveliness, invariants such as SUI supply, governance, and so on). To not be actively exploited, Mysten Labs will release signed security binaries incorporating such fixes with a delay in publishing the source code until a large percentage of our validators have patched the vulnerability.
This release process is different and we expect us to announce the directory for such binaries out of band. Our public key to verify these binaries would be stored here
There is also a script available that downloads all the necessary signed binaries and docker artifacts incorporating the security fixes.
Usage `./download_private.sh <directory-name>`
You can also download and verify specific binaries that may not be included by the above script using the `download_and_verify_private_binary.sh` script.
Usage: `./download_and_verify_private_binary.sh <directory-name> <binary-name>`
Previous
Validator Committee
  * Requirements
  * Deployment
  * Configuration
  * Connectivity
  * Network Buffer
    * Option 1: With /etc/sysctl.d/
    * Option 2: With sysctl command
    * Verification
  * Storage
  * Key management
  * Monitoring
    * Metrics
    * Logs
    * Dashboards
  * Software updates
  * State sync
  * Chain operations
    * Updating on-chain metadata
    * Operation cap
    * Updating the gas price survey quote
    * Reporting/un-reporting validators
    * Joining the validator set
    * Leaving the validator set
  * Private security fixes


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
