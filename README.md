# PCP Ingest

**Part of the Portable Context Protocol (PCP) Ecosystem**

A Python application for ingesting and processing documents into knowledge graphs, demonstrating how structured knowledge can be extracted, stored, and prepared for secure, user-owned context systems. This project serves as a foundation for building privacy-first, portable knowledge graphs that users can control across AI, gaming, and Web3 applications.

## About PCP (Portable Context Protocol)

PCP is a privacy-first protocol for secure, scoped, and portable context across digital platforms. Instead of AI systems owning your data, **you own your knowledge graph** and grant scoped access to applications that need it.

**Key PCP Principles:**

- 🔐 **Privacy-First**: Your context data is encrypted and only accessible with your permission
- 👤 **User-Owned**: You fully control your knowledge graph via NFT ownership
- 🚀 **Portable**: Seamlessly move context between AI systems, games, and dApps
- 🎯 **Scoped Access**: Applications request specific permissions (e.g., `career.read`, `gaming.stats.write`)

This `pcp-ingest` project demonstrates the **knowledge extraction and structuring** phase of the PCP ecosystem, using Sui documentation as a test case.

## Current Development Status

The PCP standard is currently under construction, but aims to create a unified standard for sharing personal information in knowledge graphs, while also maintaining user privacy and security through scoped access control and end-to-end encryption. Its integration and existence on the Sui network is because of the perfect fit that the Sui ecosystem provides when it comes to decentralized, programmable storage, key management on Seal, and access control through NFTs. We hope to complete by demo day.

## Project Structure

The application has been organized into the following modular components:

### Core Files

- `app.py` - Main application entry point that orchestrates the processing workflow
- `pcp_mcp_server.py` - MCP server for querying the knowledge graph
- `test_pcp_mcp.py` - Test suite for the MCP server functionality
- `utils.py` - General utility functions for file operations and database operations
- `snippet_processor.py` - Functions for processing and deduplicating snippets
- `snippet_extractor.py` - Logic for extracting snippets from documents
- `episode_generation.py` - Logic for generating episodes from snippets

### Client Modules

- `clients/graphiti_client.py` - Client initialization for Graphiti
- `clients/openai_client.py` - OpenAI configuration and client
- `clients/openai_compatible_client.py` - Compatible client for OpenAI API

### Data Models

- `models/snippet_extraction_model.py` - Data models for snippets
- `entities/sui_entities.py` - Entity type definitions

## Getting Started

### Prerequisites

- Python 3.9+
- Neo4j database (local or cloud)
- OpenAI API key or compatible LLM endpoint

### Quick Start

1. **Clone and Setup**

   ```bash
   git clone [repository-url]
   cd pcp-ingest
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**

   ```bash
   cp .env.example .env
   # Edit .env with your configurations:
   # - Neo4j connection details
   # - OpenAI API key
   # - Graphiti settings
   ```

4. **Run Knowledge Ingestion**

   ```bash
   python app.py
   ```

5. **Start the MCP Server** (Optional)
   ```bash
   python pcp_mcp_server.py
   ```

The application will process Sui documentation files and build a structured knowledge graph in Neo4j. The MCP server provides programmatic access to query and manage the knowledge graph.

### Understanding the Output

The system creates several types of knowledge entities:

- **Episodes**: Grouped facts about specific topics
- **Entities**: Structured objects (modules, functions, concepts)
- **Relationships**: Connections between entities
- **Communities**: Clustered related knowledge areas

### MCP Server Features

The built-in MCP server provides programmatic access to the knowledge graph:

**Available Tools:**

- `search_graph` - Search for relevant facts and entities
- `check_duplicates` - Analyze duplicate content in the graph
- `clean_duplicates` - Remove duplicate facts and nodes

**Example Usage:**

```bash
# Test the MCP server functionality
python test_pcp_mcp.py

# Start the server for external connections
python pcp_mcp_server.py
```

The MCP server exposes the knowledge graph through a standardized protocol, making it compatible with AI assistants, development tools, and other applications that support the Model Context Protocol.

## Processing Flow

1. **Document Discovery**: Finds all markdown files in the Sui documentation directory
2. **Knowledge Extraction**: Extracts structured facts (snippets) from documents using LLM processing
3. **Entity Recognition**: Identifies specific Sui/Move entities like:
   - `SuiGeneralConcept` - Core Sui principles and mechanisms
   - `MoveModuleDefinition` - Smart contract modules
   - `MoveFunctionDefinition` - Function definitions and logic
   - `SuiEventDefinition` - Event structures
   - `SuiClientCommand` - CLI commands and usage
4. **Deduplication**: Checks for existing knowledge to avoid redundancy
5. **Graph Storage**: Stores structured knowledge as episodes in Neo4j via Graphiti
6. **Statistics Reporting**: Provides processing metrics and results

## Vision: Towards User-Owned Knowledge Graphs

This project represents the **knowledge ingestion layer** of a larger PCP architecture:

```
Documents → Knowledge Extraction → Graph Storage → Encryption → User-Owned Context
    ↓              ↓                    ↓             ↓              ↓
 pcp-ingest    LLM Processing       Neo4j/Graphiti   Seal/Walrus    PCP Protocol
```

### Future Integration Goals

- **Seal Integration**: Encrypt knowledge graphs for secure, decentralized storage
- **Scoped Access**: Enable fine-grained permissions (`sui.concepts.read`, `move.functions.write`)
- **NFT Ownership**: Knowledge graphs owned via NFTs on Sui blockchain
- **Cross-Platform Portability**: Use the same Sui knowledge across different AI assistants, development tools, and dApps

### Example Use Cases in PCP Ecosystem

1. **AI Development Assistant**: An AI that remembers your Sui development patterns, preferred modules, and coding style
2. **Cross-Platform Learning**: Your Sui knowledge travels with you across different educational platforms
3. **Developer Marketplace**: Sell access to curated Sui knowledge graphs for other developers
4. **Decentralized Documentation**: Community-owned, evolving knowledge bases with contributor attribution

## Technical Architecture

### Modular and Hot-Swappable Components

The PCP standard is designed to be **hot-swappable in its components**, including the knowledge graph engine. This modular architecture allows for flexibility and optimization based on specific use cases and requirements.

We have already tested using different frameworks for different use cases. For example, we've successfully ingested documentation using [LightRAG](https://github.com/HKUDS/LightRAG), a state-of-the-art GraphRAG framework that offers different advantages for certain types of knowledge extraction and retrieval.

📹 **Demo**: [See LightRAG integration in action](https://www.loom.com/share/5bc794ed9cfd4a95864377a2c3094de4?sid=0fe940c3-68d6-4ac8-bf72-6edd1d933775)

This demonstrates that PCP's architecture allows developers to choose the best tools for their specific knowledge graph needs while maintaining compatibility with the broader PCP ecosystem.

**Current Stack:**

- **Knowledge Extraction**: Graphiti + OpenAI LLMs (primary), LightRAG (tested alternative)
- **Graph Database**: Neo4j for relationship modeling
- **Entity Modeling**: Pydantic schemas for Sui/Move constructs
- **Processing**: Python async workflows

**Planned Stack (via Seal Integration):**

- **Encryption**: Seal for decentralized secrets management
- **Storage**: Walrus for decentralized file storage
- **Access Control**: Sui Move contracts for allowlist management
- **Ownership**: NFT-based knowledge graph ownership

## Development Roadmap

### ✅ Phase 1: Knowledge Ingestion (Complete)

- [x] Sui documentation processing
- [x] Structured entity extraction
- [x] Neo4j graph storage
- [x] Deduplication and caching

### ✅ Phase 2: MCP Server (Complete)

- [x] MCP server implementation (`pcp_mcp_server.py`)
- [x] Graph search functionality
- [x] Duplicate detection and cleanup tools
- [x] RESTful API for knowledge access
- [x] Compatible with Model Context Protocol

### 🚧 Phase 3: Secure Storage (In Progress)

- [ ] Seal integration for encryption
- [ ] Walrus integration for decentralized storage
- [ ] Move contracts for access control
- [ ] NFT-based ownership model

### 🔮 Phase 4: PCP Integration (Planned)

- [ ] Scoped access permissions
- [ ] Cross-platform knowledge sharing
- [ ] Developer SDK and APIs

### 🌟 Phase 4: Ecosystem (Future)

- [ ] Knowledge marketplace
- [ ] Community contributions
- [ ] Multi-domain knowledge graphs
- [ ] AI agent integrations

## Contributing

This project is part of the broader PCP ecosystem building user-owned, privacy-first knowledge systems. We welcome contributions in several areas:

- **Knowledge Extraction**: Improving LLM prompts and entity recognition
- **Graph Modeling**: Enhancing relationship detection and schema design
- **Encryption Integration**: Implementing Seal-based security layers
- **Developer Experience**: Building better APIs and documentation

## Learn More

- **PCP Protocol**: [pcp-landing.vercel.app](https://pcp-landing.vercel.app/)
- **Seal Documentation**: [Mysten Labs Seal](https://github.com/MystenLabs/seal)
- **Sui Blockchain**: [docs.sui.io](https://docs.sui.io)
- **Graphiti Framework**: [Graphiti Core](https://github.com/getzep/graphiti)

---

_Building the future where users own their context and AI systems earn permission to access it._
