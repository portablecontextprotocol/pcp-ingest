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
      * Shared versus Owned Objects
      * Using Events
      * Access On-Chain Time
      * Signing and Sending Transactions
      * Sponsored Transactions
      * Avoiding Equivocation
      * Working with PTBs
    * Coins and Tokens
    * Stablecoins
    * NFTs
    * Cryptography
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Sui 101
  * Signing and Sending Transactions


On this page
# Signing and Sending Transactions
Transactions in Sui represent calls to specific functionality (like calling a smart contract function) that execute on inputs to define the result of the transaction.
Inputs can either be an object reference (either to an owned object, an immutable object, or a shared object), or an encoded value (for example, a vector of bytes used as an argument to a Move call). After a transaction is constructed, usually through using programmable transaction blocks (PTBs), the user signs the transaction and submits it to be executed on chain.
The signature is provided with the private key owned by the wallet, and its public key must be consistent with the transaction sender's Sui address.
Sui uses a `SuiKeyPair` to produce the signature, which commits to the Blake2b hash digest of the intent message (`intent || bcs bytes of tx_data`). The signature schemes currently supported are `Ed25519 Pure`, `ECDSA Secp256k1`, `ECDSA Secp256r1`, `Multisig`, and `zkLogin`.
You can instantiate `Ed25519 Pure`, `ECDSA Secp256k1`, and `ECDSA Secp256r1` using `SuiKeyPair` and use it to sign transactions. Note that this guide does not apply to `Multisig` and `zkLogin`, please refer to their own pages (Multisig and zkLogin respectively) for instructions.
With a signature and the transaction bytes, a transaction can be submitted to be executed.
## Workflow​
The following high-level process describes the overall workflow for constructing, signing and executing an on-chain transaction:
  * Construct the transaction data by creating a `Transaction` where multiple transactions are chained. See Building Programmable Transaction Blocks for more information.
  * The SDK's built-in gas estimation and coin selection picks the gas coin.
  * Sign the transaction to generate a signature.
  * Submit the `Transaction` and its signature for on-chain execution.


If you want to use a specific gas coin, first find the gas coin object ID to be used to pay for gas, and explicitly use that in the PTB. If there is no gas coin object, use the splitCoin transaction to create a gas coin object. The split coin transaction should be the first transaction call in the PTB.
## Examples​
The following examples demonstrate how to sign and execute transactions using Rust, TypeScript, or the Sui CLI.
  * TypeScript
  * Rust
  * Sui CLI


There are various ways to instantiate a key pair and to derive its public key and Sui address using the Sui TypeScript SDK.
```
import{ fromHex }from'@mysten/bcs';  
import{ getFullnodeUrl,SuiClient}from'@mysten/sui/client';  
import{typeKeypair}from'@mysten/sui/cryptography';  
import{Ed25519Keypair}from'@mysten/sui/keypairs/ed25519';  
import{Secp256k1Keypair}from'@mysten/sui/keypairs/secp256k1';  
import{Secp256r1Keypair}from'@mysten/sui/keypairs/secp256r1';  
import{Transaction}from'@mysten/sui/transactions';  
  
const kp_rand_0 =newEd25519Keypair();  
const kp_rand_1 =newSecp256k1Keypair();  
const kp_rand_2 =newSecp256r1Keypair();  
  
const kp_import_0 =Ed25519Keypair.fromSecretKey(  
fromHex('0xd463e11c7915945e86ac2b72d88b8190cfad8ff7b48e7eb892c275a5cf0a3e82'),  
);  
const kp_import_1 =Secp256k1Keypair.fromSecretKey(  
fromHex('0xd463e11c7915945e86ac2b72d88b8190cfad8ff7b48e7eb892c275a5cf0a3e82'),  
);  
const kp_import_2 =Secp256r1Keypair.fromSecretKey(  
fromHex('0xd463e11c7915945e86ac2b72d88b8190cfad8ff7b48e7eb892c275a5cf0a3e82'),  
);  
  
// $MNEMONICS refers to 12/15/18/21/24 words from the wordlist, e.g. "retire skin goose will hurry this field stadium drastic label husband venture cruel toe wire". Refer to [Keys and Addresses](/concepts/cryptography/transaction-auth/keys-addresses.mdx) for more.  
const kp_derive_0 =Ed25519Keypair.deriveKeypair('$MNEMONICS');  
const kp_derive_1 =Secp256k1Keypair.deriveKeypair('$MNEMONICS');  
const kp_derive_2 =Secp256r1Keypair.deriveKeypair('$MNEMONICS');  
  
const kp_derive_with_path_0 =Ed25519Keypair.deriveKeypair('$MNEMONICS',"m/44'/784'/1'/0'/0'");  
const kp_derive_with_path_1 =Secp256k1Keypair.deriveKeypair('$MNEMONICS',"m/54'/784'/1'/0/0");  
const kp_derive_with_path_2 =Secp256r1Keypair.deriveKeypair('$MNEMONICS',"m/74'/784'/1'/0/0");  
  
// replace `kp_rand_0` with the variable names above.  
const pk = kp_rand_0.getPublicKey();  
const sender = pk.toSuiAddress();  
  
// create an example transaction block.  
const txb =newTransaction();  
txb.setSender(sender);  
txb.setGasPrice(5);  
txb.setGasBudget(100);  
const bytes =await txb.build();  
const serializedSignature =(await keypair.signTransaction(bytes)).signature;  
  
// verify the signature locally  
expect(await keypair.getPublicKey().verifyTransaction(bytes, serializedSignature)).toEqual(true);  
  
// define sui client for the desired network.  
const client =newSuiClient({ url:getFullnodeUrl('testnet')});  
  
// execute transaction.  
let res = client.executeTransactionBlock({  
	transactionBlock: bytes,  
	signature: serializedSignature,  
});  
console.log(res);  

```

The full code example below can be found under crates/sui-sdk.
There are various ways to instantiate a `SuiKeyPair` and to derive its public key and Sui address using the Sui Rust SDK.
```
// deterministically generate a keypair, testing only, do not use for mainnet, use the next section to randomly generate a keypair instead.  
let skp_determ_0 =  
SuiKeyPair::Ed25519(Ed25519KeyPair::generate(&mutStdRng::from_seed([0;32])));  
let _skp_determ_1 =  
SuiKeyPair::Secp256k1(Secp256k1KeyPair::generate(&mutStdRng::from_seed([0;32])));  
let _skp_determ_2 =  
SuiKeyPair::Secp256r1(Secp256r1KeyPair::generate(&mutStdRng::from_seed([0;32])));  
  
// randomly generate a keypair.  
let _skp_rand_0 =SuiKeyPair::Ed25519(get_key_pair_from_rng(&mutrand::rngs::OsRng).1);  
let _skp_rand_1 =SuiKeyPair::Secp256k1(get_key_pair_from_rng(&mutrand::rngs::OsRng).1);  
let _skp_rand_2 =SuiKeyPair::Secp256r1(get_key_pair_from_rng(&mutrand::rngs::OsRng).1);  
  
// import a keypair from a base64 encoded 32-byte `private key`.  
let _skp_import_no_flag_0 =SuiKeyPair::Ed25519(Ed25519KeyPair::from_bytes(  
&Base64::decode("1GPhHHkVlF6GrCty2IuBkM+tj/e0jn64ksJ1pc8KPoI=")  
.map_err(|_|anyhow!("Invalid base64"))?,  
)?);  
let _skp_import_no_flag_1 =SuiKeyPair::Ed25519(Ed25519KeyPair::from_bytes(  
&Base64::decode("1GPhHHkVlF6GrCty2IuBkM+tj/e0jn64ksJ1pc8KPoI=")  
.map_err(|_|anyhow!("Invalid base64"))?,  
)?);  
let _skp_import_no_flag_2 =SuiKeyPair::Ed25519(Ed25519KeyPair::from_bytes(  
&Base64::decode("1GPhHHkVlF6GrCty2IuBkM+tj/e0jn64ksJ1pc8KPoI=")  
.map_err(|_|anyhow!("Invalid base64"))?,  
)?);  
  
// import a keypair from a base64 encoded 33-byte `flag || private key`. The signature scheme is determined by the flag.  
let _skp_import_with_flag_0 =  
SuiKeyPair::decode_base64("ANRj4Rx5FZRehqwrctiLgZDPrY/3tI5+uJLCdaXPCj6C")  
.map_err(|_|anyhow!("Invalid base64"))?;  
let _skp_import_with_flag_1 =  
SuiKeyPair::decode_base64("AdRj4Rx5FZRehqwrctiLgZDPrY/3tI5+uJLCdaXPCj6C")  
.map_err(|_|anyhow!("Invalid base64"))?;  
let _skp_import_with_flag_2 =  
SuiKeyPair::decode_base64("AtRj4Rx5FZRehqwrctiLgZDPrY/3tI5+uJLCdaXPCj6C")  
.map_err(|_|anyhow!("Invalid base64"))?;  
  
// replace `skp_determ_0` with the variable names above  
let pk = skp_determ_0.public();  
let sender =SuiAddress::from(&pk);  

```

Next, sign transaction data constructed using an example programmable transaction block with default gas coin, gas budget, and gas price. See Building Programmable Transaction Blocks for more information.
```
// construct an example programmable transaction.  
let pt ={  
letmut builder =ProgrammableTransactionBuilder::new();  
        builder.pay_sui(vec![sender],vec![1])?;  
        builder.finish()  
};  
  
let gas_budget =5_000_000;  
let gas_price = sui_client.read_api().get_reference_gas_price().await?;  
  
// create the transaction data that will be sent to the network.  
let tx_data =TransactionData::new_programmable(  
        sender,  
vec![gas_coin.object_ref()],  
        pt,  
        gas_budget,  
        gas_price,  
);  

```

Commit a signature to the Blake2b hash digest of the intent message (`intent || bcs bytes of tx_data`).
```
// derive the digest that the keypair should sign on, i.e. the blake2b hash of `intent || tx_data`.  
let intent_msg =IntentMessage::new(Intent::sui_transaction(), tx_data);  
let raw_tx =bcs::to_bytes(&intent_msg).expect("bcs should not fail");  
letmut hasher =sui_types::crypto::DefaultHash::default();  
    hasher.update(raw_tx.clone());  
let digest = hasher.finalize().digest;  
  
// use SuiKeyPair to sign the digest.  
let sui_sig = skp_determ_0.sign(&digest);  
  
// if you would like to verify the signature locally before submission, use this function. if it fails to verify locally, the transaction will fail to execute in Sui.  
let res = sui_sig.verify_secure(  
&intent_msg,  
        sender,  
sui_types::crypto::SignatureScheme::ED25519,  
);  
assert!(res.is_ok());  

```

Finally, submit the transaction with the signature.
```
let transaction_response = sui_client  
.quorum_driver_api()  
.execute_transaction_block(  
sui_types::transaction::Transaction::from_generic_sig_data(  
                intent_msg.value,  
Intent::sui_transaction(),  
vec![GenericSignature::Signature(sui_sig)],  
),  
SuiTransactionBlockResponseOptions::default(),  
None,  
)  
.await?;  

```

When using the Sui CLI for the first time, it creates a local file in `~/.sui/keystore` on your machine with a list of private keys (encoded as Base64 encoded `flag || 32-byte-private-key`). You can use any key to sign transactions by specifying its address. Use `sui keytool list` to see a list of addresses.
There are three ways to initialize a key:
```
# generate randomly.  
sui client new-address ed25519  
sui client new-address secp256k1  
sui client new-address secp256r1  
  
# import the 32-byte private key to keystore.  
sui keytool import "0xd463e11c7915945e86ac2b72d88b8190cfad8ff7b48e7eb892c275a5cf0a3e82" ed25519  
sui keytool import "0xd463e11c7915945e86ac2b72d88b8190cfad8ff7b48e7eb892c275a5cf0a3e82" secp256k1  
sui keytool import "0xd463e11c7915945e86ac2b72d88b8190cfad8ff7b48e7eb892c275a5cf0a3e82" secp256r1  
  
# import the mnemonics (recovery phrase) with derivation path to keystore.  
# $MNEMONICS refers to 12/15/18/21/24 words from the wordlist, e.g. "retire skin goose will hurry this field stadium drastic label husband venture cruel toe wire". Refer to [Keys and Addresses](/concepts/cryptography/transaction-auth/keys-addresses.mdx) for more.  
  
sui keytool import "$MNEMONICS" ed25519  
sui keytool import "$MNEMONICS" secp256k1  
sui keytool import "$MNEMONICS" secp256r1  

```

Create a transfer transaction in the CLI. Set the `$SUI_ADDRESS` to the one corresponding to the keypair used to sign. `$GAS_COIN_ID` refers to the object ID that is owned by the sender to be used as gas. `$GAS_BUDGET` refers to the budget used to execute transaction. Then sign with the private key corresponding to the sender address. `$MNEMONICS` refers to 12/15/18/21/24 words from the wordlist, e.g. "retire skin goose will hurry this field stadium drastic label husband venture cruel toe wire". Refer to Keys and Addresses for more.
Beginning with the Sui `v1.24.1` release, the `--gas-budget` option is no longer required for CLI commands.
```
$ sui client gas  

```

```
$ sui client transfer-sui --to $SUI_ADDRESS --sui-coin-object-id $GAS_COIN_ID --gas-budget $GAS_BUDGET --serialize-unsigned-transaction  

```

```
$ sui keytool sign --address $SUI_ADDRESS --data $TX_BYTES  

```

```
$ sui client execute-signed-tx --tx-bytes $TX_BYTES --signatures $SERIALIZED_SIGNATURE  

```

### Notes​
  1. This guide demonstrates how to sign with a single private key. Refer to Multisig when it is preferred to set up more complex signing policies.
  2. Similarly, native zkLogin does not follow the above steps, see the docs to understand how to derive a zkLogin address, and produce a zkLogin signature with an ephemeral key pair.
  3. If you decide to implement your own signing mechanisms instead of using the previous tools, see the Signatures doc on the accepted signature specifications for each scheme.
  4. Flag is one byte that differentiates signature schemes. See supported schemes and its flag in Signatures.
  5. The `execute_transaction_block` endpoint takes a list of signatures, so it should contain exactly one user signature, unless you are using sponsored transaction that a second signature for the gas object can be provided. See Sponsored Transactions for more information.


Previous
Access On-Chain Time
Next
Sponsored Transactions
  * Workflow
  * Examples
    * Notes


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
