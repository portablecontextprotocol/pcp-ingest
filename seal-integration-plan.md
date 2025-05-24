# Seal Integration Plan for PCP-Ingest

## Overview

This plan outlines the integration of Mysten Labs' Seal (decentralized secrets management) into the pcp-ingest project. The integration will create a new data layer that exports data from the existing Neo4j database, encrypts it using Seal, and uploads it to Walrus with allowlist-based access control.

## Project Context

**Current State:**

- PCP-Ingest processes Sui documentation and stores structured knowledge in Neo4j via Graphiti
- Data includes entities like SuiGeneralConcept, MoveModuleDefinition, MoveFunctionDefinition, etc.
- Processing workflow: Document ingestion → Snippet extraction → Episode generation → Neo4j storage

**Target State:**

- Maintain existing functionality
- Add secure data export capability
- Implement Seal encryption for sensitive data
- Store encrypted data on Walrus with access control
- Enable secure data sharing with allowlisted addresses

## Architecture Overview

```
Neo4j Database → Data Export Layer → Seal Encryption → Walrus Storage
                                          ↓
                                  Allowlist Control (Move Smart Contracts)
```

## Implementation Plan

### Phase 1: Project Setup and Dependencies

#### 1.1 Create Move Development Environment

- **Location:** Create `move/` subdirectory in project root
- **Structure:**
  ```
  move/
  ├── Move.toml
  ├── sources/
  │   ├── allowlist.move
  │   ├── subscription.move
  │   └── utils.move
  └── README.md
  ```

#### 1.2 Install Dependencies

Add to `requirements.txt`:

```
aiofiles>=24.1.0
cryptography>=42.0.0
walrus-python>=0.1.0  # Official Python SDK for Walrus
requests>=2.31.0
```

**Node.js Setup:** Since Seal SDK is only available in TypeScript, we'll create a Node.js bridge. Create a `package.json` and install dependencies:

```bash
npm init -y
npm install @mysten/seal @mysten/sui
```

Add to `package.json`:

```json
{
  "type": "module",
  "scripts": {
    "seal-bridge": "node seal_integration/seal_bridge.js"
  }
}
```

#### 1.3 Environment Configuration

Add to `.env`:

```
# Seal Configuration
SEAL_KEY_SERVER_URLS=["https://testnet-key-server-1.sui.io", "https://testnet-key-server-2.sui.io"]
SEAL_THRESHOLD=2
SEAL_PACKAGE_ID=0x... # To be deployed

# Walrus Configuration
WALRUS_PUBLISHER_URL=https://publisher.walrus-testnet.walrus.space
WALRUS_AGGREGATOR_URL=https://aggregator.walrus-testnet.walrus.space

# Allowlist Configuration
HARDCODED_WALLET_ADDRESS=0x... # Hardcoded allowlisted address
SUI_NETWORK=testnet
SUI_RPC_URL=https://fullnode.testnet.sui.io:443
```

### Phase 2: Move Smart Contract Development

#### 2.1 Setup Move.toml

**File:** `move/Move.toml`

```toml
[package]
name = "pcp_seal_integration"
version = "1.0.0"
edition = "2024.beta"

[dependencies]
Sui = { git = "https://github.com/MystenLabs/sui.git", subdir = "crates/sui-framework/packages/sui-framework", rev = "framework/testnet" }

[addresses]
pcp_seal = "0x0"
sui = "0x2"
```

#### 2.2 Implement Allowlist Contract

**File:** `move/sources/allowlist.move`

- Copy and customize from Seal examples
- Implement access control for PCP data
- Add functions for managing allowlisted addresses
- Include namespace generation for PCP-specific data

#### 2.3 Implement Subscription Contract (Optional)

**File:** `move/sources/subscription.move`

- Copy from Seal examples for future paid access functionality
- Enable time-based access to encrypted data

#### 2.4 Utility Functions

**File:** `move/sources/utils.move`

- Helper functions for data validation
- Common utilities for both allowlist and subscription

### Phase 3: Data Export Layer

#### 3.1 Create Data Export Module

**File:** `data_export/exporter.py`

```python
class Neo4jDataExporter:
    """Exports structured data from Neo4j for Seal encryption"""

    async def export_entities_by_type(self, entity_type: str) -> List[Dict]
    async def export_full_graph_snapshot() -> Dict
    async def export_incremental_changes(since: datetime) -> Dict
    async def export_filtered_data(filters: Dict) -> Dict
```

#### 3.2 Create Data Serialization Module

**File:** `data_export/serializer.py`

```python
class DataSerializer:
    """Handles serialization of Neo4j data for encryption"""

    def serialize_for_encryption(self, data: Dict) -> bytes
    def compress_data(self, data: bytes) -> bytes
    def add_metadata(self, data: bytes, metadata: Dict) -> bytes
```

### Phase 4: Seal Integration Layer

#### 4.1 Create Seal Client Module

**File:** `seal_integration/seal_client.py`

```python
import asyncio
import json
import subprocess
import tempfile
from typing import List, Dict
from pathlib import Path

class PcpSealClient:
    """Wrapper around Seal TypeScript SDK via Node.js bridge"""

    def __init__(self, key_servers: List[str], threshold: int, package_id: str):
        self.key_servers = key_servers
        self.threshold = threshold
        self.package_id = package_id
        self.node_script_path = Path(__file__).parent / "seal_bridge.js"

    async def encrypt_data(self, data: bytes, allowlist_id: str) -> bytes:
        """Encrypt data using Seal via Node.js bridge"""
        # Write data to temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(data)
            tmp_file_path = tmp_file.name

        try:
            # Call Node.js script for encryption
            result = await self._call_node_script("encrypt", {
                "file_path": tmp_file_path,
                "allowlist_id": allowlist_id,
                "package_id": self.package_id,
                "threshold": self.threshold,
                "key_servers": self.key_servers
            })

            # Read encrypted data
            with open(result["encrypted_file_path"], "rb") as f:
                return f.read()
        finally:
            # Cleanup temporary files
            Path(tmp_file_path).unlink(missing_ok=True)
            if "encrypted_file_path" in result:
                Path(result["encrypted_file_path"]).unlink(missing_ok=True)

    async def decrypt_data(self, encrypted_data: bytes, allowlist_id: str, user_address: str) -> bytes:
        """Decrypt data using Seal via Node.js bridge"""
        # Similar implementation for decryption
        pass

    async def _call_node_script(self, operation: str, params: Dict) -> Dict:
        """Call Node.js script with parameters"""
        cmd = [
            "node",
            str(self.node_script_path),
            operation,
            json.dumps(params)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"Node.js script failed: {stderr.decode()}")

        return json.loads(stdout.decode())
```

**File:** `seal_integration/seal_bridge.js`

```javascript
// Node.js bridge script for Seal operations
const { SealClient, getAllowlistedKeyServers } = require("@mysten/seal");
const { SuiClient } = require("@mysten/sui/client");
const fs = require("fs").promises;
const path = require("path");

async function encrypt(params) {
  const { file_path, allowlist_id, package_id, threshold, key_servers } =
    params;

  // Initialize Seal client
  const suiClient = new SuiClient({ url: process.env.SUI_RPC_URL });
  const client = new SealClient({
    suiClient,
    serverObjectIds: key_servers,
    verifyKeyServers: false,
  });

  // Read file data
  const data = await fs.readFile(file_path);

  // Encrypt data
  const { encryptedObject } = await client.encrypt({
    threshold,
    packageId: package_id,
    id: allowlist_id,
    data: new Uint8Array(data),
  });

  // Write encrypted data to temporary file
  const encrypted_file_path = path.join(
    path.dirname(file_path),
    `encrypted_${path.basename(file_path)}`
  );
  await fs.writeFile(encrypted_file_path, encryptedObject);

  return { encrypted_file_path };
}

async function decrypt(params) {
  // Implementation for decryption
  // Similar pattern but using client.decrypt()
}

// Main execution
const [, , operation, paramsJson] = process.argv;
const params = JSON.parse(paramsJson);

(async () => {
  try {
    let result;
    switch (operation) {
      case "encrypt":
        result = await encrypt(params);
        break;
      case "decrypt":
        result = await decrypt(params);
        break;
      default:
        throw new Error(`Unknown operation: ${operation}`);
    }
    console.log(JSON.stringify(result));
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
})();
```

#### 4.2 Create Sui Integration Module

**File:** `seal_integration/sui_client.py`

```python
class SuiContractClient:
    """Handles interaction with Sui Move contracts"""

    async def create_allowlist(self, name: str, wallet_address: str) -> str
    async def add_to_allowlist(self, allowlist_id: str, address: str)
    async def remove_from_allowlist(self, allowlist_id: str, address: str)
    async def check_access(self, allowlist_id: str, address: str) -> bool
```

#### 4.3 Create Walrus Integration Module

**File:** `seal_integration/walrus_client.py`

```python
from walrus import WalrusClient as WalrusSDK
from typing import Dict, Optional
import asyncio
import aiofiles

class WalrusClient:
    """Handles Walrus storage operations using walrus-python SDK"""

    def __init__(self, publisher_url: str, aggregator_url: str):
        self.client = WalrusSDK(
            publisher_base_url=publisher_url,
            aggregator_base_url=aggregator_url
        )

    async def store_blob(self, data: bytes, epochs: int = 1, deletable: bool = False) -> str:
        """Store blob on Walrus and return blob_id"""
        response = await asyncio.to_thread(self.client.put_blob, data=data, epochs=epochs, deletable=deletable)
        return response.get('blob_id')

    async def store_blob_from_file(self, file_path: str, epochs: int = 1, deletable: bool = False) -> str:
        """Store file on Walrus and return blob_id"""
        response = await asyncio.to_thread(self.client.put_blob_from_file, file_path, epochs=epochs, deletable=deletable)
        return response.get('blob_id')

    async def retrieve_blob(self, blob_id: str) -> bytes:
        """Retrieve blob content by blob_id"""
        return await asyncio.to_thread(self.client.get_blob, blob_id)

    async def retrieve_blob_as_file(self, blob_id: str, destination_path: str) -> None:
        """Retrieve blob and save to file"""
        await asyncio.to_thread(self.client.get_blob_as_file, blob_id, destination_path)

    async def get_blob_metadata(self, blob_id: str) -> Dict:
        """Get blob metadata"""
        return await asyncio.to_thread(self.client.get_blob_metadata, blob_id)
```

### Phase 5: Main Integration Module

#### 5.1 Create Secure Data Export Service

**File:** `secure_export.py`

```python
class SecureDataExportService:
    """Main service for exporting and encrypting PCP data"""

    async def export_and_encrypt_entities(
        self,
        entity_types: List[str],
        allowlist_addresses: List[str]
    ) -> Dict[str, str]  # Returns mapping of entity_type -> blob_id

    async def create_data_snapshot(
        self,
        snapshot_name: str,
        allowlist_addresses: List[str]
    ) -> str  # Returns snapshot blob_id

    async def export_filtered_data(
        self,
        filters: Dict,
        allowlist_addresses: List[str]
    ) -> str  # Returns blob_id
```

#### 5.2 Update Main Application

**File:** `app.py` (modifications)

- Add secure export functionality
- Integrate with existing workflow
- Add CLI commands for data export operations

### Phase 6: Configuration and Deployment

#### 6.1 Deploy Move Contracts

**Script:** `scripts/deploy_contracts.py`

```python
async def deploy_move_package():
    """Deploy Move contracts to Sui testnet"""
    # Compile and deploy the Move package
    # Store deployed package ID in environment
```

#### 6.2 Initialize Allowlist

**Script:** `scripts/initialize_allowlist.py`

```python
async def create_initial_allowlist():
    """Create initial allowlist with hardcoded wallet address"""
    # Create allowlist contract instance
    # Add hardcoded wallet address to allowlist
```

### Phase 7: CLI Integration

#### 7.1 Add Export Commands

**File:** `cli/export_commands.py`

```python
@click.group()
def export():
    """Secure data export commands"""
    pass

@export.command()
@click.option('--entity-types', multiple=True)
@click.option('--allowlist-addresses', multiple=True)
async def entities(entity_types, allowlist_addresses):
    """Export specific entity types with encryption"""

@export.command()
@click.option('--snapshot-name', required=True)
@click.option('--allowlist-addresses', multiple=True)
async def snapshot(snapshot_name, allowlist_addresses):
    """Create encrypted data snapshot"""
```

#### 7.2 Add Allowlist Management Commands

```python
@click.group()
def allowlist():
    """Allowlist management commands"""
    pass

@allowlist.command()
@click.option('--name', required=True)
async def create(name):
    """Create new allowlist"""

@allowlist.command()
@click.option('--allowlist-id', required=True)
@click.option('--address', required=True)
async def add_address(allowlist_id, address):
    """Add address to allowlist"""
```

### Phase 8: Testing and Validation

#### 8.1 Unit Tests

**Directory:** `tests/seal_integration/`

- Test data export functionality
- Test Seal encryption/decryption
- Test Sui contract interactions
- Test Walrus storage operations

#### 8.2 Integration Tests

**File:** `tests/test_full_integration.py`

- End-to-end testing of export → encrypt → upload → retrieve workflow
- Test allowlist access control
- Test error handling and edge cases

#### 8.3 Test Data Validation

**File:** `tests/test_data_integrity.py`

- Verify exported data matches source
- Test encryption/decryption round-trip
- Validate metadata preservation

### Phase 9: Documentation and Examples

#### 9.1 Update README

- Add Seal integration documentation
- Include setup instructions for Move development
- Document new CLI commands

#### 9.2 Create Usage Examples

**File:** `examples/seal_usage.py`

- Example: Export specific entity types
- Example: Create and manage allowlists
- Example: Decrypt and access data

#### 9.3 API Documentation

- Document all new modules and classes
- Include code examples for common operations
- Add troubleshooting guide

## File Structure After Integration

```
pcp-ingest/
├── existing files...
├── move/                          # NEW
│   ├── Move.toml
│   ├── sources/
│   │   ├── allowlist.move
│   │   ├── subscription.move
│   │   └── utils.move
│   └── README.md
├── data_export/                   # NEW
│   ├── __init__.py
│   ├── exporter.py
│   └── serializer.py
├── seal_integration/              # NEW
│   ├── __init__.py
│   ├── seal_client.py
│   ├── seal_bridge.js             # Node.js bridge for Seal SDK
│   ├── sui_client.py
│   └── walrus_client.py
├── package.json                   # NEW (Node.js dependencies)
├── node_modules/                  # NEW (Node.js dependencies)
├── cli/                          # NEW
│   ├── __init__.py
│   ├── export_commands.py
│   └── allowlist_commands.py
├── scripts/                      # NEW
│   ├── deploy_contracts.py
│   └── initialize_allowlist.py
├── tests/seal_integration/       # NEW
├── examples/                     # NEW
│   └── seal_usage.py
├── secure_export.py              # NEW
└── requirements.txt              # UPDATED
```

## Dependencies and Resources

### Required External Resources

1. **Seal Repository:** https://github.com/MystenLabs/seal/tree/main
2. **Seal Examples:** https://github.com/MystenLabs/seal/tree/main/examples
3. **Sui Testnet:** For deploying Move contracts
4. **Walrus Testnet:** For encrypted data storage

### Key Dependencies

1. **Sui CLI:** For Move development and deployment
2. **Seal TypeScript SDK:** Accessed via Node.js bridge ([@mysten/seal](https://www.npmjs.com/package/@mysten/seal))
3. **Walrus Python SDK:** Direct Python integration ([walrus-python](https://github.com/standard-crypto/walrus-python))
4. **Sui Python SDK:** For blockchain interactions
5. **Node.js (v18+):** Required for Seal TypeScript SDK bridge

### Environment Setup Requirements

1. **Sui CLI installation**
2. **Testnet wallet with SUI tokens**
3. **Walrus publisher/aggregator access**
4. **Seal key server access**

## Security Considerations

1. **Hardcoded Wallet Address:** Store securely in environment variables
2. **Key Management:** Proper handling of encryption keys and wallet keys
3. **Access Control:** Validate allowlist membership before data access
4. **Data Integrity:** Verify data hasn't been tampered with during storage/retrieval
5. **Error Handling:** Secure error messages that don't leak sensitive information

## Success Criteria

1. ✅ Move contracts deployed successfully on Sui testnet
2. ✅ Data export from Neo4j working correctly
3. ✅ Seal encryption/decryption functional
4. ✅ Walrus storage integration operational
5. ✅ Allowlist access control enforced
6. ✅ CLI commands for all major operations
7. ✅ Comprehensive test coverage (>80%)
8. ✅ Documentation complete and accurate

## Timeline Estimate

- **Phase 1-2:** 3-4 days (Setup and Move contracts)
- **Phase 3-4:** 4-5 days (Data export and Seal integration)
- **Phase 5-6:** 3-4 days (Main integration and deployment)
- **Phase 7-8:** 3-4 days (CLI and testing)
- **Phase 9:** 2-3 days (Documentation)

**Total Estimated Time:** 15-20 days

## Technical Approach Summary

Based on the current state of Seal and Walrus ecosystems:

1. **Seal Integration:** Since Seal is TypeScript-only, we implement a Node.js bridge that Python calls via subprocess. This allows us to leverage the full Seal SDK functionality.

2. **Walrus Integration:** We use the mature [walrus-python](https://github.com/standard-crypto/walrus-python) SDK for direct Python integration with Walrus storage.

3. **Hybrid Architecture:** Python handles the main application logic, data export, and Walrus operations, while Node.js handles Seal encryption/decryption operations.

## Next Steps

1. Begin with Phase 1: Create the `move/` subdirectory and setup dependencies
2. Install Node.js and the Seal TypeScript SDK alongside Python dependencies
3. Study Seal examples thoroughly before implementing the bridge
4. Set up Sui testnet wallet and get test tokens
5. Plan the data export schema and encryption strategy
6. Implement in phases, testing each component before moving to the next

This plan provides a comprehensive roadmap for integrating Seal into the pcp-ingest project while maintaining the existing functionality and adding secure, decentralized data sharing capabilities. The hybrid Python/Node.js approach allows us to leverage the best tools available in each ecosystem.
