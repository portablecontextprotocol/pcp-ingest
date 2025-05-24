Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Sui Components
  * App Developers
    * Object Model
    * Move Overview
    * Transactions
    * gRPC Overview (Beta)
    * GraphQL for Sui RPC (Alpha)
    * Gaming on Sui
  * Cryptography
  * Sui Architecture
  * Tokenomics
  * Research Papers


  *   * App Developers
  * gRPC Overview (Beta)


On this page
# gRPC Overview (Beta)
⚙️Early-Stage Feature
This content describes an alpha/beta feature or service. These early stage features and services are in active development, so details are likely to change.
This feature or service is currently available in
  * Devnet
  * Testnet
  * Mainnet


The Sui Full Node gRPC API provides a fast, type-safe, and efficient interface for interacting with the Sui blockchain. Designed for power users, indexers, explorers, and decentralized apps, this API enables access to Sui data with high performance and low latency.
Refer to Access Sui Data for an overview of options to access Sui network data.
## What is gRPC?​
gRPC offers a high-performance, efficient communication protocol that uses Protocol Buffers for fast, compact data serialization. Its strongly typed interfaces reduce runtime errors and simplify client/server development across multiple languages. With built-in support for code generation, you can scaffold clients in Typescript, Go, Rust, and more. This makes it ideal for scalable backend systems like indexers, blockchain explorers, and data-intensive decentralized apps.
In addition to request-response calls, gRPC supports server-side streaming, enabling real-time data delivery without constant polling. This is especially useful in environments where you need to track events and transactions live. gRPC's binary format is significantly faster and lighter than JSON, saving bandwidth and improving latency.
Refer to when to use gRPC vs GraphQL to access Sui data.
## gRPC on Sui​
Protocol buffers define the gRPC interface. You can find the relevant beta `.proto` files at sui-rpc-api on Github, which apart from the gRPC messages (request and response payloads) include the following services and types:
  * `sui/rpc/v2beta/transaction_execution_service.proto`
  * `sui/rpc/v2beta/ledger_service.proto`


These definitions can be used to generate client libraries in various programming languages.
There are some proto files in the folder `sui/rpc/v2alpha` as well. Those are are in alpha because they are early experimental versions that are subject to change and not recommended for production use.
The `TransactionExecutionService` currently offers a single RPC method: `ExecuteTransaction(ExecuteTransactionRequest)`, which is used to execute a transaction request. Whereas the `LedgerService` includes the core lookup queries for Sui data. Some of the RPCs in that service include:
  * `GetObject(GetObjectRequest)`: Retrieves details of a specific on-chain object.
  * `GetTransaction(GetTransactionRequest)`: Fetches information about a particular transaction.
  * `GetCheckpoint(GetCheckpointRequest)`: Fetches information about a particular checkpoint.


### Field masks​
A `FieldMask` in Protocol Buffers is a mechanism used to specify a subset of fields within a message that should be read, updated, or returned. Instead of retrieving the entire object, a client can request only the specific fields they need by providing a list of field paths. This improves performance and reduces unnecessary data transfer.
In the Sui gRPC API, `FieldMask`s are used in requests like `GetTransaction` to control which parts of the transaction (such as, `effects`, `events`) are included in the response. Field paths must match the structure of the response message. This selective querying is especially useful for building efficient applications and tools.
### Encoding​
In the Sui gRPC API, identifiers with standard human-readable formats are represented as `string`s in the proto schema:
  * `Address` and `ObjectId`: Represented as 64 hexadecimal characters with a leading `0x`.
  * `Digest`s: Represented as Base58.
  * `TypeTag` and `StructTag`: Represented in their canonical string format (for example, `0x0000000000000000000000000000000000000000000000000000000000000002::coin::Coin<0x0000000000000000000000000000000000000000000000000000000000000002::sui::SUI>`)


## Access using grpcurl​
Simplest way to experiment with gRPC is by using grpcurl.
Your results might differ from the examples that follow, depending on the breadth and maturity of the gRPC APIs available on Sui Full nodes.
### List available gRPC services​
```
$ grpcurl <full node URL:port> list  

```

where the port on Sui Foundation managed Full nodes is `443`. It should return something like:
```
grpc.health.v1.Health  
grpc.reflection.v1.ServerReflection  
sui.rpc.v2alpha.LiveDataService  
sui.rpc.v2alpha.SubscriptionService  
sui.rpc.v2beta.LedgerService  
sui.rpc.v2beta.TransactionExecutionService  

```

### List available APIs in the LedgerService​
```
$ grpcurl <full node URL:port> list sui.rpc.v2beta.LedgerService  

```

which should return something like:
```
sui.rpc.v2beta.LedgerService.BatchGetObjects  
sui.rpc.v2beta.LedgerService.BatchGetTransactions  
sui.rpc.v2beta.LedgerService.GetCheckpoint  
sui.rpc.v2beta.LedgerService.GetEpoch  
sui.rpc.v2beta.LedgerService.GetObject  
sui.rpc.v2beta.LedgerService.GetServiceInfo  
sui.rpc.v2beta.LedgerService.GetTransaction  

```

### Get the `events` and `effects` details of a particular transaction​
```
$ grpcurl -d '{ "digest": "3ByWphQ5sAVojiTrTrGXGM5FmCVzpzYmhsjbhYESJtxp" }' <full node URL:port> sui.rpc.v2beta.LedgerService/GetTransaction  

```

### Get the transactions in a particular checkpoint​
```
$ grpcurl -d '{ "sequence_number": "180529334", "read_mask": { "paths": ["transactions"]} }' <full node URL:port> sui.rpc.v2beta.LedgerService/GetCheckpoint  

```

## Sample clients in different programming languages​
  * TypeScript
  * Golang
  * Python


This is an example to build a Typescript client for Sui gRPC API. If you want to use a different set of tools or modules that you’re comfortable with, you can adjust the instructions accordingly.
**Install dependencies**
```
npm init -y  

```

```
npm install @grpc/grpc-js @grpc/proto-loader  

```

```
npm i -D tsx  

```

**Project structure**
```
.  
├── protos/  
│   └── sui/  
│       └── node/  
│           └── v2beta/  
│               ├── ledger_service.proto  
│               └── *.proto  
├── client.ts  
├── package.json  

```

Download all the `sui/rpc/v2beta` proto files from Github v2beta in the same folder.
**Sample client.ts to get`events` and `effects` details of a particular transaction**
```
import*as grpcfrom'@grpc/grpc-js';  
import*as protoLoaderfrom'@grpc/proto-loader';  
import*as pathfrom'path';  
  
constPROTO_PATH= path.join(__dirname,'protos/sui/rpc/v2beta/ledger_service.proto');  
  
// Load proto definitions  
const packageDefinition = protoLoader.loadSync(PROTO_PATH,{  
  keepCase:true,  
  longs:String,  
  enums:String,  
  defaults:true,  
  oneofs:true,  
  includeDirs:[path.join(__dirname,'protos')],  
});  
  
const suiProto = grpc.loadPackageDefinition(packageDefinition)asany;  
constLedgerService= suiProto.sui.rpc.v2beta.LedgerService;  
  
// Create gRPC client  
const client =newLedgerService(  
'<full node URL>:443',  
  grpc.credentials.createSsl()  
);  
  
// Sample transaction digest in Base58 format  
const base58Digest ='3ByWphQ5sAVojiTrTrGXGM5FmCVzpzYmhsjbhYESJtxp';  
  
// Construct the request  
const request ={  
  digest: base58Digest,  
  read_mask:{  
    paths:['events','effects'],  
},  
};  
  
// Make gRPC call  
client.GetTransaction(request,(err:any, response:any)=>{  
if(err){  
console.error('Error:', err);  
}else{  
console.log('Response:',JSON.stringify(response,null,2));  
}  
});  

```

**Run the sample client**
```
npx tsx c  

```

  * `proto-loader` handles any nested `.proto` files - just make sure paths and imports are correct.
  * The example assumes that gRPC is available on port `443` which requires SSL.
  * Digest in the request is directly provided in the `Base58` format, but check if you need to decode from your source format.


This is an example to build a golang client for Sui gRPC API. Feel free to use another set of tools or modules that you’re comfortable with.
**Install dependencies**
First make sure you have `go` and `protoc` installed in your environment, and then install:
```
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest  

```

```
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest  

```

In your `go.mod`, add the following (make sure to update the version numbers to the latest versions):
```
require (  
  google.golang.org/grpc v1.60.0  
  google.golang.org/protobuf v1.33.0  
)  

```

**Generate Golang code from proto files**
Assuming you have the the proto files from Github v2beta, run:
```
protoc --proto_path=./protos --go_out=. --go-grpc_out=. protos/sui/rpc/v2beta/ledger_service.proto  

```

**Sample main.go to get`events` and `effects` details of a particular transaction**
```
package main  
  
import(  
"context"  
"crypto/tls"  
"fmt"  
"log"  
"time"  
  
"google.golang.org/grpc"  
"google.golang.org/grpc/credentials"  
  
    pb "your_project/sui/rpc/v2beta"// adjust path based on where your generated .pb.go files are  
)  
  
funcmain(){  
// Set up gRPC connection with TLS (port 443)  
		creds := credentials.NewTLS(&tls.Config{})  
		conn, err := grpc.Dial("<full node URL>:443", grpc.WithTransportCredentials(creds))  
if err !=nil{  
			log.Fatalf("failed to connect: %v", err)  
}  
defer conn.Close()  
  
    client := pb.NewLedgerServiceClient(conn)  
  
// Sample transaction digest in Base58 format  
    base58Digest :="3ByWphQ5sAVojiTrTrGXGM5FmCVzpzYmhsjbhYESJtxp"  
  
// Build request  
		req :=&pb.GetTransactionRequest{  
			Digest: base58Digest,  
			ReadMask:&pb.TransactionReadMask{  
				Paths:[]string{"events","effects"},  
},  
}  
  
// Make the request  
    ctx, cancel := context.WithTimeout(context.Background(),10*time.Second)  
defercancel()  
  
    resp, err := client.GetTransaction(ctx, req)  
if err !=nil{  
        log.Fatalf("GetTransaction failed: %v", err)  
}  
  
// Print the response  
    fmt.Printf("Response:\n%+v\n", resp)  
}  

```

**Run the sample client**
If your `go.mod` is properly set up, and you've already generated the gRPC code (`*.pb.go`, `*_grpc.pb.go`), simply run:
```
go run main.go  

```

  * If you see errors like `cannot find package`, ensure you’ve generated the proto files and imported them correctly.
  * If your generated files are in a nested directory like `sui/rpc/v2beta`, your import in `main.go` should match:


```
import pb "your_project/sui/rpc/v2beta"  

```

You can replace `your_project` with a module name or relative import path depending on how your `go.mod` is defined.
  * The example assumes that gRPC is available on port `443` which requires SSL.
  * Digest in the request is directly provided in the `Base58` format, but check if you need to decode from your source format.


This is an example to build a python client for Sui gRPC API. Feel free to use another set of tools or modules that you’re comfortable with.
**Install dependencies**
First make sure you have `python` and `protoc` installed in your environment, and then install:
```
pip install grpcio grpcio-tools protobuf  

```

**Generate Python code from proto files**
Assuming you have the the proto files from Github v2beta, run:
```
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/sui/rpc/v2beta/ledger_service.proto  

```

**Sample client.py to get`events` and `effects` details of a particular transaction**
```
import grpc  
from sui.rpc.v2beta import ledger_service_pb2, ledger_service_pb2_grpc  
  
defmain():  
# Create secure channel to port 443  
    channel = grpc.secure_channel("<full node URL>:443", grpc.ssl_channel_credentials())  
    stub = ledger_service_pb2_grpc.LedgerServiceStub(channel)  
  
# Sample transaction digest in Base58 format  
    base58_digest ="3ByWphQ5sAVojiTrTrGXGM5FmCVzpzYmhsjbhYESJtxp"  
  
# Build the request  
    request = ledger_service_pb2.GetTransactionRequest(  
        digest=base58_digest,  
        read_mask=ledger_service_pb2.TransactionReadMask(paths=["events","effects"])  
)  
  
# Make the RPC call  
    response = stub.GetTransaction(request)  
  
# Print response  
print(response)  
  
if __name__ =="__main__":  
    main()  

```

**Run the sample client**
```
python client.py  

```

  * The import paths like `sui.rpc.v2beta.ledger_service_pb2` depend on your proto structure.
  * You might need to adjust `__init__.py` files or PYTHONPATH to ensure proper module resolution.
  * The example assumes that gRPC is available on port `443` which requires SSL.
  * Digest in the request is directly provided in the `Base58` format, but check if you need to decode from your source format.


## Frequently asked questions​
  * Q: In a batch object request (`BatchGetObjects`), does the field mask specified in individual `GetObjectRequest`s override the top-level field mask in the `BatchGetObjectsRequest`?
    * A: **No** , only the top-level field mask defined in the `BatchGetObjectsRequest` is used. Any field masks specified within individual `GetObjectRequest` entries are ignored. This behavior also applies to other batch request APIs in the `LedgerService` interface.
  * Q: In `ExecuteTransactionRequest`, why is the `transaction` field marked as `optional`?
    * A: While the `transaction` field is marked as `optional` in the `TransactionExecutionService` .proto file, it is not optional in the API contract. It is required when making the request. This is a quirk of Protocol Buffers: marking a field as `optional` enables field presence, which allows the API to distinguish between fields that were explicitly set and those that were left unset. Some of the benefits of field presence include: 
      * Differentiating between missing and default values
      * Enabling patch or partial update semantics
      * Avoiding ambiguity when default values (like `0`, `""`, or `false`) are valid inputs


Previous
Gas Smashing
Next
GraphQL for Sui RPC (Alpha)
  * What is gRPC?
  * gRPC on Sui
    * Field masks
    * Encoding
  * Access using grpcurl
    * List available gRPC services
    * List available APIs in the LedgerService
    * Get the `events` and `effects` details of a particular transaction
    * Get the transactions in a particular checkpoint
  * Sample clients in different programming languages
  * Frequently asked questions


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
