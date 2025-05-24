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
      * Write a Move Package
      * Build and Test Packages
      * Publish a Package
      * Debugging
      * Client App with Sui TypeScript SDK
    * Sui 101
    * Coins and Tokens
    * Stablecoins
    * NFTs
    * Cryptography
    * Advanced Topics
    * App Examples
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * Your First Sui dApp
  * Client App with Sui TypeScript SDK


On this page
# Client App with Sui TypeScript SDK
This exercise diverges from the example built in the previous topics in this section. Rather than adding a frontend to the running example, the instruction walks you through setting up dApp Kit in a React App, allowing you to connect to wallets, and query data from Sui RPC nodes to display in your app. You can use it to create your own frontend for the example used previously, but if you want to get a fully functional app up and running quickly, run the following command in a terminal or console to scaffold a new app with all steps in this exercise already implemented:
You must use the pnpm or yarn package managers to create Sui project scaffolds. Follow the pnpm install or yarn install instructions, if needed.
```
$ pnpm create @mysten/dapp --template react-client-dapp  

```

or
```
$ yarn create @mysten/dapp --template react-client-dapp  

```

## What is the Sui TypeScript SDK?​
The Sui TypeScript SDK (@mysten/sui) provides all the low-level functionality needed to interact with Sui ecosystem from TypeScript. You can use it in any TypeScript or JavaScript project, including web apps, Node.js apps, or mobile apps written with tools like React Native that support TypeScript.
For more information on the Sui TypeScript SDK, see the Sui TypeScript SDK documentation.
## What is dApp Kit?​
dApp Kit (@mysten/dapp-kit) is a collection of React hooks, components, and utilities that make building dApps on Sui straightforward. For more information on dApp Kit, see the dApp Kit documentation.
## Installing dependencies​
To get started, you need a React app. The following steps apply to any React, so you can follow the same steps to add dApp Kit to an existing React app. If you are starting a new project, you can use Vite to scaffold a new React app.
Run the following command in your terminal or console, and select React as the framework, and then select one of the TypeScript templates:
  * npm
  * Yarn
  * pnpm


```
$ npm init vite  

```

```
$ yarn create vite  

```

```
$ pnpm create vite  

```

Now that you have a React app, you can install the necessary dependencies to use dApp Kit:
  * npm
  * Yarn
  * pnpm


```
$ npm install @mysten/sui @mysten/dapp-kit @tanstack/react-query  

```

```
$ yarn add @mysten/sui @mysten/dapp-kit @tanstack/react-query  

```

```
$ pnpm add @mysten/sui @mysten/dapp-kit @tanstack/react-query  

```

## Setting up Provider components​
To use all the features of dApp Kit, wrap your app with a couple of `Provider` components.
Open the root component that renders your app (the default location the Vite template uses is `src/main.tsx`) and integrate or replace the current code with the following.
The first `Provider` to set up is the `QueryClientProvider` from `@tanstack/react-query`. This `Provider` manages request state for various hooks in dApp kit. If you're already using `@tanstack/react-query`, dApp Kit can share the same `QueryClient` instance.
```
import{QueryClient,QueryClientProvider}from'@tanstack/react-query';  
  
const queryClient =newQueryClient();  
  
ReactDOM.createRoot(document.getElementById('root')!).render(  
<React.StrictMode>  
<QueryClientProvider client={queryClient}>  
<App/>  
</QueryClientProvider>  
</React.StrictMode>,  
);  

```

Next, set up the `SuiClientProvider`. This `Provider` delivers a `SuiClient` instance from `@mysten/sui` to all the hooks in dApp Kit. This provider manages which network dApp Kit connects to, and can accept configuration for multiple networks. This exercise connects to `devnet`.
```
import{SuiClientProvider}from'@mysten/dapp-kit';  
import{ getFullnodeUrl }from'@mysten/sui/client';  
import{QueryClient,QueryClientProvider}from'@tanstack/react-query';  
  
const queryClient =newQueryClient();  
const networks ={  
	devnet:{ url:getFullnodeUrl('devnet')},  
	mainnet:{ url:getFullnodeUrl('mainnet')},  
};  
  
ReactDOM.createRoot(document.getElementById('root')!).render(  
<React.StrictMode>  
<QueryClientProvider client={queryClient}>  
<SuiClientProvider networks={networks} defaultNetwork="devnet">  
<App/>  
</SuiClientProvider>  
</QueryClientProvider>  
</React.StrictMode>,  
);  

```

Finally, set up the `WalletProvider` from `@mysten/dapp-kit`, and import styles for the `dapp-kit` components.
```
import'@mysten/dapp-kit/dist/index.css';  
  
import{SuiClientProvider,WalletProvider}from'@mysten/dapp-kit';  
import{ getFullnodeUrl }from'@mysten/sui/client';  
import{QueryClient,QueryClientProvider}from'@tanstack/react-query';  
  
const queryClient =newQueryClient();  
const networks ={  
	devnet:{ url:getFullnodeUrl('devnet')},  
	mainnet:{ url:getFullnodeUrl('mainnet')},  
};  
  
ReactDOM.createRoot(document.getElementById('root')!).render(  
<React.StrictMode>  
<QueryClientProvider client={queryClient}>  
<SuiClientProvider networks={networks} defaultNetwork="devnet">  
<WalletProvider>  
<App/>  
</WalletProvider>  
</SuiClientProvider>  
</QueryClientProvider>  
</React.StrictMode>,  
);  

```

## Connecting to a wallet​
With all `Providers` set up, you can use dApp Kit hooks and components. To allow users to connect their wallets to your dApp, add a `ConnectButton`.
```
import{ConnectButton}from'@mysten/dapp-kit';  
  
functionApp(){  
return(  
<div className="App">  
<header className="App-header">  
<ConnectButton/>  
</header>  
</div>  
);  
}  

```

The `ConnectButton` component displays a button that opens a modal on click, enabling the user to connect their wallet. Upon connection, it displays their address, and provides the option to disconnect.
## Getting the connected wallet address​
Now that you have a way for users to connect their wallets, you can start using the `useCurrentAccount` hook to get details about the connected wallet account.
```
import{ConnectButton, useCurrentAccount }from'@mysten/dapp-kit';  
  
functionApp(){  
return(  
<div className="App">  
<header className="App-header">  
<ConnectButton/>  
</header>  
  
<ConnectedAccount/>  
</div>  
);  
}  
  
functionConnectedAccount(){  
const account =useCurrentAccount();  
  
if(!account){  
returnnull;  
}  
  
return<div>Connected to {account.address}</div>;  
}  

```

## Querying data from Sui RPC nodes​
Now that you have the account to connect to, you can query for objects the connected account owns:
```
import{ useCurrentAccount, useSuiClientQuery }from'@mysten/dapp-kit';  
  
functionConnectedAccount(){  
const account =useCurrentAccount();  
  
if(!account){  
returnnull;  
}  
  
return(  
<div>  
<div>Connected to {account.address}</div>;  
<OwnedObjects address={account.address}/>  
</div>  
);  
}  
  
functionOwnedObjects({ address }:{ address:string}){  
const{ data }=useSuiClientQuery('getOwnedObjects',{  
		owner: address,  
});  
if(!data){  
returnnull;  
}  
  
return(  
<ul>  
{data.data.map((object)=>(  
<li key={object.data?.objectId}>  
<a href={`https://example-explorer.com/object/${object.data?.objectId}`}>  
{object.data?.objectId}  
</a>  
</li>  
))}  
</ul>  
);  
}  

```

You now have a dApp connected to wallets and can query data from RPC nodes.
## Related links​
The next step from here is to start interacting with Move modules, constructing transaction blocks, and making Move calls. This exercise continues in the Counter end-to-end example.
  * End-to-End Example: Continue this exercise by creating an app.
  * Sui 101: Learn the basics of the Sui network and how to interact with on-chain objects using Move.
  * Sui Move CLI: The `move` commands in the Sui CLI provide console or terminal interaction with the Move VM.


Previous
Debugging
Next
Sui 101
  * What is the Sui TypeScript SDK?
  * What is dApp Kit?
  * Installing dependencies
  * Setting up Provider components
  * Connecting to a wallet
  * Getting the connected wallet address
  * Querying data from Sui RPC nodes
  * Related links


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
