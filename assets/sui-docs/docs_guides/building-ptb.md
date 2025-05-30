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
        * Building Programmable Transaction Blocks
        * Coin Management
        * Simulating References
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
  * Working with PTBs
  * Building Programmable Transaction Blocks


On this page
# Building Programmable Transaction Blocks
This guide explores creating a programmable transaction block (PTB) on Sui using the TypeScript SDK. For an overview of what a PTB is, see Programmable Transaction Blocks in the Concepts section. If you don't already have the Sui TypeScript SDK, follow the install instructions on the Sui TypeScript SDK site.
This example starts by constructing a PTB to send Sui. If you are familiar with the legacy Sui transaction types, this is similar to a `paySui` transaction. To construct transactions, import the `Transaction` class, and construct it:
```
import{Transaction}from'@mysten/sui/transactions';  
  
const tx =newTransaction();  

```

Using this, you can then add transactions to this PTB.
```
// Create a new coin with balance 100, based on the coins used as gas payment.  
// You can define any balance here.  
const[coin]= tx.splitCoins(tx.gas,[tx.pure(100)]);  
  
// Transfer the split coin to a specific address.  
tx.transferObjects([coin], tx.pure('0xSomeSuiAddress'));  

```

You can attach multiple transaction commands of the same type to a PTB as well. For example, to get a list of transfers, and iterate over them to transfer coins to each of them:
```
interfaceTransfer{  
	to:string;  
	amount:number;  
}  
  
// Procure a list of some Sui transfers to make:  
const transfers:Transfer[]=getTransfers();  
  
const tx =newTransaction();  
  
// First, split the gas coin into multiple coins:  
const coins = tx.splitCoins(  
	tx.gas,  
	transfers.map((transfer)=> tx.pure(transfer.amount)),  
);  
  
// Next, create a transfer transaction for each coin:  
transfers.forEach((transfer, index)=>{  
	tx.transferObjects([coins[index]], tx.pure(transfer.to));  
});  

```

After you have the Transaction defined, you can directly execute it with a `SuiClient` and `KeyPair` using `client.signAndExecuteTransaction`.
```
client.signAndExecuteTransaction({ signer: keypair, transaction: tx });  

```

## Constructing inputs​
Inputs are how you provide external values to PTBs. For example, defining an amount of Sui to transfer, or which object to pass into a Move call, or a shared object.
There are currently two ways to define inputs:
  * For objects: the `tx.object(objectId)` function is used to construct an input that contains an object reference.
  * For pure values: the `tx.pure(value, type?)` function is used to construct an input for a non-object input.
    * If value is a `Uint8Array`, then the value is assumed to be raw bytes and is used directly.
    * If type is provided, it's used to generate the BCS serialization layout for the value. If not provided, the type is automatically determined based on the value.


## Available transactions​
Sui supports following transaction commands:
  * `tx.splitCoins(coin, amounts)`: Creates new coins with the defined amounts, split from the provided coin. Returns the coins so that it can be used in subsequent transactions.
    * Example: `tx.splitCoins(tx.gas, [tx.pure(100), tx.pure(200)])`
  * `tx.mergeCoins(destinationCoin, sourceCoins)`: Merges the sourceCoins into the destinationCoin.
    * Example: `tx.mergeCoins(tx.object(coin1), [tx.object(coin2), tx.object(coin3)])`
  * `tx.transferObjects(objects, address)`: Transfers a list of objects to the specified address.
    * Example: `tx.transferObjects([tx.object(thing1), tx.object(thing2)], tx.pure(myAddress))`
  * `tx.moveCall({ target, arguments, typeArguments })`: Executes a Move call. Returns whatever the Sui Move call returns.
    * Example: `tx.moveCall({ target: '0x2::devnet_nft::mint', arguments: [tx.pure(name), tx.pure(description), tx.pure(image)] })`
  * `tx.makeMoveVec({ type, elements })`: Constructs a vector of objects that can be passed into a moveCall. This is required as there's no other way to define a vector as an input.
    * Example: `tx.makeMoveVec({ elements: [tx.object(id1), tx.object(id2)] })`
  * `tx.publish(modules, dependencies)`: Publishes a Move package. Returns the upgrade capability object.


## Passing transaction results as arguments​
You can use the result of a transaction command as an argument in subsequent transaction commands. Each transaction command method on the transaction builder returns a reference to the transaction result.
```
// Split a coin object off of the gas object:  
const[coin]= tx.splitCoins(tx.gas,[tx.pure(100)]);  
// Transfer the resulting coin object:  
tx.transferObjects([coin], tx.pure(address));  

```

When a transaction command returns multiple results, you can access the result at a specific index either using destructuring, or array indexes.
```
// Destructuring (preferred, as it gives you logical local names):  
const[nft1, nft2]= tx.moveCall({ target:'0x2::nft::mint_many'});  
tx.transferObjects([nft1, nft2], tx.pure(address));  
  
// Array indexes:  
const mintMany = tx.moveCall({ target:'0x2::nft::mint_many'});  
tx.transferObjects([mintMany[0], mintMany[1]], tx.pure(address));  

```

## Use the gas coin​
With PTBs, you can use the gas payment coin to construct coins with a set balance using `splitCoin`. This is useful for Sui payments, and avoids the need for up-front coin selection. You can use `tx.gas` to access the gas coin in a PTB, and it is valid as input for any arguments; with the exception of `transferObjects`, `tx.gas` must be used by-reference. Practically speaking, this means you can also add to the gas coin with `mergeCoins` or borrow it for Move functions with `moveCall`.
You can also transfer the gas coin using `transferObjects`, in the event that you want to transfer all of your coin balance to another address.
Of course, you can also transfer other coins in your wallet using their `Object ID`. For example,
```
const otherCoin = tx.object('0xCoinObjectId');  
const coin = tx.splitCoins(otherCoin,[tx.pure(100)]);  
tx.transferObjects([coin], tx.pure(address));  

```

## Get PTB bytes​
If you need the PTB bytes, instead of signing or executing the PTB, you can use the `build` method on the transaction builder itself.
You might need to explicitly call `setSender()` on the PTB to ensure that the `sender` field is populated. This is normally done by the signer before signing the transaction, but will not be done automatically if you're building the PTB bytes yourself.
```
const tx =newTransaction();  
  
// ... add some transactions...  
  
await tx.build({ provider });  

```

In most cases, building requires your JSON RPC provider to fully resolve input values.
If you have PTB bytes, you can also convert them back into a `Transaction` class:
```
const bytes =getTransactionBytesFromSomewhere();  
const tx =Transaction.from(bytes);  

```

## Building offline​
In the event that you want to build a PTB offline (as in with no `provider` required), you need to fully define all of your input values, and gas configuration (see the following example). For pure values, you can provide a `Uint8Array` which is used directly in the transaction. For objects, you can use the `Inputs` helper to construct an object reference.
```
import{Inputs}from'@mysten/sui/transactions';  
  
// For pure values:  
tx.pure(pureValueAsBytes);  
  
// For owned or immutable objects:  
tx.object(Inputs.ObjectRef({ digest, objectId, version }));  
  
// For shared objects:  
tx.object(Inputs.SharedObjectRef({ objectId, initialSharedVersion, mutable }));  

```

You can then omit the `provider` object when calling `build` on the transaction. If there is any required data that is missing, this will throw an error.
## Gas configuration​
The new transaction builder comes with default behavior for all gas logic, including automatically setting the gas price, budget, and selecting coins to be used as gas. This behavior can be customized.
### Gas price​
By default, the gas price is set to the reference gas price of the network. You can also explicitly set the gas price of the PTB by calling `setGasPrice` on the transaction builder.
```
tx.setGasPrice(gasPrice);  

```

### Budget​
By default, the gas budget is automatically derived by executing a dry-run of the PTB beforehand. The dry run gas consumption is then used to determine a balance for the transaction. You can override this behavior by explicitly setting a gas budget for the transaction, by calling `setGasBudget` on the transaction builder.
The gas budget is represented in Sui, and should take the gas price of the PTB into account.
```
tx.setGasBudget(gasBudgetAmount);  

```

### Gas payment​
By default, the gas payment is automatically determined by the SDK. The SDK selects all coins at the provided address that are not used as inputs in the PTB.
The list of coins used as gas payment will be merged down into a single gas coin before executing the PTB, and all but one of the gas objects will be deleted. The gas coin at the 0-index will be the coin that all others are merged into.
```
// NOTE: You need to ensure that the coins do not overlap with any  
// of the input objects for the PTB.  
tx.setGasPayment([coin1, coin2]);  

```

Gas coins should be objects containing the coins objectId, version, and digest (ie `{ objectId: string, version: string | number, digest: string }`).
### dApp / Wallet integration​
The Wallet Standard interface has been updated to support the `Transaction` kind directly. All `signTransaction` and `signAndExecuteTransaction` calls from dApps into wallets is expected to provide a `Transaction` class. This PTB class can then be serialized and sent to your wallet for execution.
To serialize a PTB for sending to a wallet, Sui recommends using the `tx.serialize()` function, which returns an opaque string representation of the PTB that can be passed from the wallet standard dApp context to your wallet. This can then be converted back into a `Transaction` using `Transaction.from()`.
You should not build the PTB from bytes in the dApp code. Using `serialize` instead of `build` allows you to build the PTB bytes within the wallet itself. This allows the wallet to perform gas logic and coin selection as needed.
```
// Within a dApp  
const tx =newTransaction();  
wallet.signTransaction({ transaction: tx });  
  
// Your wallet standard code:  
functionhandleSignTransaction(input){  
sendToWalletContext({ transaction: input.transaction.serialize()});  
}  
  
// Within your wallet context:  
functionhandleSignRequest(input){  
const userTx =Transaction.from(input.transaction);  
}  

```

## Sponsored PTBs​
The PTB builder can support sponsored PTBs by using the `onlyTransactionKind` flag when building the PTB.
```
const tx =newTransaction();  
// ... add some transactions...  
  
const kindBytes =await tx.build({ provider, onlyTransactionKind:true});  
  
// Construct a sponsored transaction from the kind bytes:  
const sponsoredTx =Transaction.fromKind(kindBytes);  
  
// You can now set the sponsored transaction data that is required:  
sponsoredTx.setSender(sender);  
sponsoredTx.setGasOwner(sponsor);  
sponsoredTx.setGasPayment(sponsorCoins);  

```

## Related links​
  * Using Stablecoins in PTBs


Previous
Avoiding Equivocation
Next
Coin Management
  * Constructing inputs
  * Available transactions
  * Passing transaction results as arguments
  * Use the gas coin
  * Get PTB bytes
  * Building offline
  * Gas configuration
    * Gas price
    * Budget
    * Gas payment
    * dApp / Wallet integration
  * Sponsored PTBs
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
