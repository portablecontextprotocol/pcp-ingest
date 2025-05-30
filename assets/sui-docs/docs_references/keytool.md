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


  *   * Sui CLI
  * Sui Keytool CLI


On this page
# Sui Keytool CLI
The Sui CLI `keytool` command provides several command-level access for the management and generation of addresses, as well as working with private keys, signatures, or zkLogin. For example, a user could export a private key from the Sui Wallet and import it into the local Sui CLI wallet using the `sui keytool import [...]` command.
## Check Sui CLI installation​
Before you can use the Sui CLI, you must install it. To check if the CLI exists on your system, open a terminal or console and type the following command:
```
$ sui --version  

```

If the terminal or console responds with a version number, you already have the Sui CLI installed.
If the command is not found, follow the instructions in Install Sui to get the Sui CLI on your system.
## Commands​
```
Usage: sui keytool [OPTIONS] <COMMAND>  
  
Commands:  
  convert                           	Convert private key from legacy formats (e.g. Hex or Base64) to Bech32 encoded 33 byte `flag || private key` begins with `suiprivkey`  
  decode-or-verify-tx                   Given a Base64 encoded transaction bytes, decode its components. If a signature is provided, verify the signature against the transaction   
  											and output the result.  
  decode-multi-sig                  	Given a Base64 encoded MultiSig signature, decode its components. If tx_bytes is passed in, verify the multisig  
  generate                          	Generate a new keypair with key scheme flag {ed25519 | secp256k1 | secp256r1} with optional derivation path, default to  
                                        	m/44'/784'/0'/0'/0' for ed25519 or m/54'/784'/0'/0/0 for secp256k1 or m/74'/784'/0'/0/0 for secp256r1. Word length can be { word12 |  
                                        	word15 | word18 | word21 | word24} default to word12 if not specified  
  import                            	Add a new key to sui.keystore using either the input mnemonic phrase or a private key (from the Wallet), the key scheme flag {ed25519 |  
                                        	secp256k1 | secp256r1} and an optional derivation path, default to m/44'/784'/0'/0'/0' for ed25519 or m/54'/784'/0'/0/0 for secp256k1  
                                        	or m/74'/784'/0'/0/0 for secp256r1. Supports mnemonic phrase of word length 12, 15, 18`, 21, 24  
  list                              	List all keys by its Sui address, Base64 encoded public key, key scheme name in sui.keystore  
  load-keypair                      	This reads the content at the provided file path. The accepted format can be [enum SuiKeyPair] (Base64 encoded of 33-byte `flag ||  
                                        	privkey`) or `type AuthorityKeyPair` (Base64 encoded `privkey`). This prints out the account keypair as Base64 encoded `flag ||  
                                        	privkey`, the network keypair, worker keypair, protocol keypair as Base64 encoded `privkey`  
  multi-sig-address                 	To MultiSig Sui Address. Pass in a list of all public keys `flag || pk` in Base64. See `keytool list` for example public keys  
  multi-sig-combine-partial-sig     	Provides a list of participating signatures (`flag || sig || pk` encoded in Base64), threshold, a list of all public keys and a list of  
                                        	their weights that define the MultiSig address. Returns a valid MultiSig signature and its sender address. The result can be used as  
                                        	signature field for `sui client execute-signed-tx`. The sum of weights of all signatures must be >= the threshold  
  multi-sig-combine-partial-sig-legacy  
  show                              	Read the content at the provided file path. The accepted format can be [enum SuiKeyPair] (Base64 encoded of 33-byte `flag || privkey`)  
                                        	or `type AuthorityKeyPair` (Base64 encoded `privkey`). It prints its Base64 encoded public key and the key scheme flag  
  sign                              	Create signature using the private key for the given address in sui keystore. Any signature commits to a [struct IntentMessage]  
                                        	consisting of the Base64 encoded of the BCS serialized transaction bytes itself and its intent. If intent is absent, default will be  
                                        	used  
  sign-kms                          	Creates a signature by leveraging AWS KMS. Pass in a key-id to leverage Amazon KMS to sign a message and the base64 pubkey. Generate  
                                        	PubKey from pem using MystenLabs/base64pemkey Any signature commits to a [struct IntentMessage] consisting of the Base64 encoded of the  
                                        	BCS serialized transaction bytes itself and its intent. If intent is absent, default will be used  
  unpack                            	This takes [enum SuiKeyPair] of Base64 encoded of 33-byte `flag || privkey`). It outputs the keypair into a file at the current  
                                        	directory where the address is the filename, and prints out its Sui address, Base64 encoded public key, the key scheme, and the key  
                                        	scheme flag  
  zk-login-sign-and-execute-tx      	Given the max_epoch, generate an OAuth url, ask user to paste the redirect with id_token, call salt server, then call the prover  
                                        	server, create a test transaction, use the ephemeral key to sign and execute it by assembling to a serialized zkLogin signature  
  zk-login-enter-token              	A workaround to the above command because sometimes token pasting does not work. All the inputs required here are printed from the  
                                        	command above  
  zk-login-sig-verify               	Given a zkLogin signature, parse it if valid. If tx_bytes provided, it verifies the zkLogin signature based on provider and its latest  
                                        	JWK fetched. Example request: sui keytool zk-login-sig-verify --sig $SERIALIZED_ZKLOGIN_SIG --tx-bytes $TX_BYTES --provider Google  
                                        	--curr-epoch 10  
  help                              	Print this message or the help of the given subcommand(s)  
  
Options:  
  	--keystore-path <KEYSTORE_PATH>  
  	--json                       	Return command outputs in json format  
  -h, --help                       	Print help  

```

## JSON output​
Append the `--json` flag to commands to format responses in JSON instead of the more human friendly default Sui CLI output. This can be useful for extremely large datasets, for example, as those results can have a troublesome display on smaller screens. In these cases, the `--json` flag is useful.
## Examples​
The following examples demonstrate some of the most often used commands.
### List the key pairs in the local wallet​
Use the `sui keytool list` command to output all the Sui addresses that exist in the `~/.sui/sui_config/sui.keystore` file in a readable format.
```
$ sui keytool list  

```

```
╭────────────────────────────────────────────────────────────────────────────────────────────╮  
│ ╭─────────────────┬──────────────────────────────────────────────────────────────────────╮ │  
│ │ suiAddress      │  0x3047f142a84297a42a65fb0a8c7a716d9d1b0bd0413d6bfa5ddfec45df175235  │ │  
│ │ publicBase64Key │  AHsXwcxaWNaNtCIIszwu7V2G6HO8aNM1598w/8y0zI5q                        │ │  
│ │ keyScheme       │  ed25519                                                             │ │  
│ │ flag            │  0                                                                   │ │  
│ │ peerId          │  7b17c1cc5a58d68db42208b33c2eed5d86e873bc68d335e7df30ffccb4cc8e6a    │ │  
│ ╰─────────────────┴──────────────────────────────────────────────────────────────────────╯ │  
│ ╭─────────────────┬──────────────────────────────────────────────────────────────────────╮ │  
│ │ suiAddress      │  0x514692f08249c3e9957799ce29074695840422564bff85e424b56de462913e0d  │ │  
│ │ publicBase64Key │  AKJCGi8R8TslhYdO2OHIjI6rbr+to1eR+vlOjigLY6SX                        │ │  
│ │ keyScheme       │  ed25519                                                             │ │  
│ │ flag            │  0                                                                   │ │  
│ │ peerId          │  a2421a2f11f13b2585874ed8e1c88c8eab6ebfada35791faf94e8e280b63a497    │ │  
│ ╰─────────────────┴──────────────────────────────────────────────────────────────────────╯ │  
╰────────────────────────────────────────────────────────────────────────────────────────────╯  

```

### Generate a new key pair and store it in a file​
To generate a new key pair with the `ed25519` scheme, use the `sui keytool generate ed25519` command. For other schemes, see `sui keytool generate –help`. The key pair file is saved to the current directory with its filename being the address. The content of the file is a Base64 encoded string of 33-byte `flag || privkey`.
```
$ sui keytool generate ed25519  

```

```
╭─────────────────┬───────────────────────────────────────────────────────────────────────────────────╮  
│ suiAddress      │  0x5d8aa70f17d9343813d3ba6a59ecf5e8a23ffb487938e860999a722989eaef25               │  
│ publicBase64Key │  AKTAGf9iv0JqeLXXlsr4PUzBXb9VY8lK7xiZMS50GSu6                                     │  
│ keyScheme       │  ed25519                                                                          │  
│ flag            │  0                                                                                │  
│ mnemonic        │  cushion price ability recall payment embody kid media rude mosquito chalk broom  │  
│ peerId          │  a4c019ff62bf426a78b5d796caf83d4cc15dbf5563c94aef1899312e74192bba                 │  
╰─────────────────┴───────────────────────────────────────────────────────────────────────────────────╯  

```

### Show the key pair data from a file​
Use `sui keytool show [filename]` to show the key pair data that is stored in a file. For example, the previous command generated a file named `0x5d8aa70f17d9343813d3ba6a59ecf5e8a23ffb487938e860999a722989eaef25.key`.
```
$ sui keytool show 0x5d8aa70f17d9343813d3ba6a59ecf5e8a23ffb487938e860999a722989eaef25.key  

```

```
╭─────────────────┬──────────────────────────────────────────────────────────────────────╮  
│ suiAddress      │  0x5d8aa70f17d9343813d3ba6a59ecf5e8a23ffb487938e860999a722989eaef25  │  
│ publicBase64Key │  AC+AKTAGf9iv0JqeLXXlsr4PUzBXb9VY8lK7xiZMS50GSu6                     │  
│ keyScheme       │  ed25519                                                             │  
│ flag            │  0                                                                   │  
│ peerId          │  a4c019ff62bf426a78b5d796caf83d4cc15dbf5563c94aef1899312e74192bba    │  
╰─────────────────┴──────────────────────────────────────────────────────────────────────╯  

```

### Sign a transaction​
```
$ sui keytool sign --data AAABACBRRpLwgknD6ZV3mc4pB0aVhAQiVkv/heQktW3kYpE+DQEBAQABAAAwR/FCqEKXpCpl+wqMenFtnRsL0EE9a/pd3+xF3xdSNQEaEUeErlBmGWxz3Bh+9BZh2mzayodzsri7xIZNDHRA3wIAAAAAAAAAILsR2d1FIZ5+ADDYZtJ2e9CWlpAxsGd4Y2rZrjlyTUF1MEfxQqhCl6QqZfsKjHpxbZ0bC9BBPWv6Xd/sRd8XUjXoAwAAAAAAAICWmAAAAAAAAA== --address 0x3047f142a84297a42a65fb0a8c7a716d9d1b0bd0413d6bfa5ddfec45df175235  

```

```
╭──────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮  
│ suiAddress   │ 0x3047f142a84297a42a65fb0a8c7a716d9d1b0bd0413d6bfa5ddfec45df175235                                                                                               │  
│ rawTxData    │ AAABACBRRpLwgknD6ZV3mc4pB0aVhAQiVkv/heQktW3kYpE+DQEBAQABAAAwR/FCqEKXpCpl+wqMenFtnRsL0EE9a/pd3+xF3xdSNQEaEUeErlBmGWxz3Bh+9BZh2mzayodzsri7xIZNDHRA3wIAAAAAAAAAILsR │  
│              │ 2d1FIZ5+ADDYZtJ2e9CWlpAxsGd4Y2rZrjlyTUF1MEfxQqhCl6QqZfsKjHpxbZ0bC9BBPWv6Xd/sRd8XUjXoAwAAAAAAAICWmAAAAAAAAA==                                                     │  
│ intent       │ ╭─────────┬─────╮                                                                                                                                                │  
│              │ │ scope   │  0  │                                                                                                                                                │  
│              │ │ version │  0  │                                                                                                                                                │  
│              │ │ app_id  │  0  │                                                                                                                                                │  
│              │ ╰─────────┴─────╯                                                                                                                                                │  
│ rawIntentMsg │ AAAAAAABACBRRpLwgknD6ZV3mc4pB0aVhAQiVkv/heQktW3kYpE+DQEBAQABAAAwR/FCqEKXpCpl+wqMenFtnRsL0EE9a/pd3+xF3xdSNQEaEUeErlBmGWxz3Bh+9BZh2mzayodzsri7xIZNDHRA3wIAAAAAAAAA │  
│              │ ILsR2d1FIZ5+ADDYZtJ2e9CWlpAxsGd4Y2rZrjlyTUF1MEfxQqhCl6QqZfsKjHpxbZ0bC9BBPWv6Xd/sRd8XUjXoAwAAAAAAAICWmAAAAAAAAA==                                                 │  
│ digest       │ +B8Cbr16HfOVT50DoN/QF8HB0+oznm8KAYy8Rm+TQFo=                                                                                                                     │  
│ suiSignature │ ANucBEl9TIE0uv+w965DvOjlfDUll7NUtIpJgRhPc3D3y3EtZ4cvaNbm8i5pc7TNIov/qI0FhzIYf2J6PbqoNQ57F8HMWljWjbQiCLM8Lu1dhuhzvGjTNeffMP/MtMyOag==                             │  
╰──────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯  

```

## Help​
Each command has its own help section. For example `sui keytool sign –help` displays the following prompt:
```
$ sui keytool sign --help  

```

```
Create signature using the private key for the given address in sui keystore. Any signature commits to a [struct IntentMessage] consisting of the Base64 encoded of the BCS serialized  
transaction bytes itself and its intent. If intent is absent, default will be used  
  
Usage: sui keytool sign [OPTIONS] --address <ADDRESS> --data <DATA>  
  
Options:  
  	--address <ADDRESS>    
  	--data <DATA>   	   
  	--json           	Return command outputs in json format  
  	--intent <INTENT>      
  -h, --help           	Print help  

```

Previous
Sui Console CLI
Next
Sui Move CLI
  * Check Sui CLI installation
  * Commands
  * JSON output
  * Examples
    * List the key pairs in the local wallet
    * Generate a new key pair and store it in a file
    * Show the key pair data from a file
    * Sign a transaction
  * Help


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
