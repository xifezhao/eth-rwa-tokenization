# Smart Contract Project: RWA Tokenization Framework for "Scalable & Secure Real-World Asset Tokenization using Ethereum Staking & L2 Solutions"

This repository contains a collection of Solidity smart contracts and supporting scripts for a decentralized application (dApp) framework, as detailed in the paper "Scalable & Secure Real-World Asset Tokenization using Ethereum Staking & L2 Solutions". It focuses on Real-World Asset (RWA) tokenization, a Decentralized Autonomous Organization (DAO), ERC20/ERC721 token standards, and staking mechanisms.

## Overview

This project showcases the development and interaction of several key components integral to a comprehensive RWA tokenization platform:

1.  **DAO Contract (`DAOContract.sol`):** A basic DAO contract allowing members to create and vote on proposals governing platform parameters.
2.  **ERC20 Token (`MyERC20Token.sol`):** A standard ERC20 token contract, potentially representing fungible RWAs or governance tokens.
3.  **ERC721 NFT (`MyERC721NFT.sol`):** A standard ERC721 NFT contract for representing unique, non-fungible RWAs.
4.  **Token Staking Contract (`TokenStaking.sol`):** A contract that allows users to stake tokens, potentially for securing Layer-2 operations or participating in governance.
5.  **RWA Manager (`RWAManager.sol`):** A contract to manage aspects of RWA tokenization, such as yield distribution.
6.  **Mock Oracle (`MockOracle.sol`):** A simplified oracle contract for simulating external data feeds, like asset valuations.

## Contracts

### 1. DAO Contract (`DAOContract.sol`)

*   **Description:** Implements a basic Decentralized Autonomous Organization (DAO). Members can create proposals, and other members can vote on them.
*   **Key Features:** Proposal creation, voting mechanism, proposal execution, member management.
*   **Events:** `ProposalCreated`, `VoteCast`, `ProposalExecuted`.

### 2. ERC20 Token (`MyERC20Token.sol`)

*   **Description:** A standard ERC20 token. Can be used as a reward token, governance token, or to represent fungible RWAs.
*   **Key Features:** Basic token functionality, minting/burning (if implemented), metadata.

### 3. ERC721 NFT (`MyERC721NFT.sol`)

*   **Description:** A standard ERC721 non-fungible token. Used to represent unique digital assets or RWAs.
*   **Key Features:** Minting of unique NFTs, ownership tracking, metadata management.

### 4. Token Staking Contract (`TokenStaking.sol`)

*   **Description:** Allows users to stake their ERC20 tokens, potentially earning rewards or participating in platform security.
*   **Key Features:** Staking, withdrawal, reward calculation, reward claim.
*   **Events:** `Staked`, `Withdrawn`, `RewardClaimed`.

### 5. RWA Manager (`RWAManager.sol`)

*   **Description:** Manages specific RWA-related functionalities, such as depositing reward tokens and distributing them to token holders.
*   **Key Features:** Reward deposit, reward distribution.

### 6. Mock Oracle (`MockOracle.sol`)

*   **Description:** A simplified contract to simulate an oracle providing external data (e.g., asset prices) to the blockchain.
*   **Key Features:** Update asset values.

## Getting Started

### Prerequisites

*   Node.js and npm installed
*   Truffle development environment (as contracts were originally compiled with Truffle)
*   Ganache or other local Ethereum blockchain for testing
*   Python 3.x with `web3.py` and `pandas` installed (for running simulation scripts)

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/xifezhao/eth-rwa-tokenization.git
    cd eth-rwa-tokenization
    ```

2.  Install Node.js dependencies (primarily for OpenZeppelin contracts used by Solidity):

    ```bash
    npm install
    npm install @openzeppelin/contracts
    ```

3.  Compile the contracts using Truffle:
    (Ensure you are in the project's root directory where `truffle-config.js` is located)
    ```bash
    truffle compile
    ```
    This will create the contract artifacts in the `build/contracts/` directory, which are used by the deployment and simulation scripts.

### Deployment (Manual or via Scripts)

The contracts can be deployed to a local network like Ganache or a testnet. The simulation script `rwa_l1_l2_cost_simulation.py` handles deployment to a local Ganache instance.

For manual deployment or deployment to other networks:
1.  Configure your network in `truffle-config.js`.
2.  Create migration scripts in the `migrations/` directory if they don't already exist or need adjustment.
3.  Deploy the contracts:
    ```bash
    truffle migrate --network <network_name>
    ```

### Usage

1.  **Smart Contracts:** Interact with deployed contracts using tools like Truffle Console, Remix, or custom web interfaces.
2.  **Simulation Experiment:** The Python script `rwa_l1_l2_cost_simulation.py` demonstrates key functionalities and performs cost analysis.

---

## Layer-1 vs. Layer-2 RWA Transaction Cost Simulation Experiment

This repository also includes a Python-based simulation (`rwa_l1_l2_cost_simulation.py`) designed to compare the estimated costs of various Real-World Asset (RWA) related transactions on Ethereum Layer-1 versus a simulated Layer-2 (Optimistic Rollup-like) solution.

### Purpose of the Simulation

The primary goal is to provide a quantitative illustration of the potential gas cost savings and overall economic benefits of leveraging Layer-2 technology for RWA tokenization, as discussed in the associated research paper.

### Key Features of the Simulation:

*   **Contract Deployment:** Deploys the necessary smart contracts (ERC20, ERC721, RWAManager, SimpleDAO, MockOracle) to a local Ganache instance.
*   **Transaction Types Simulated:**
    *   RWA Token Issuance (ERC-721 minting)
    *   RWA Token Transfer (ERC-20 transfer)
    *   Yield Distribution to multiple token holders
    *   Governance Voting on a DAO proposal
    *   Oracle-dependent transaction (e.g., updating an asset's valuation)
*   **Layer-1 Cost Calculation:** Executes transactions directly on Ganache (simulating L1) and records actual gas used and transaction costs based on Ganache's gas price.
*   **Layer-2 Cost Simulation Model:**
    *   Estimates L2 operational gas based on a defined efficiency factor relative to L1 gas.
    *   Includes a fixed base fee for L2 transactions.
    *   Calculates amortized L1 batch submission costs (data + base transaction gas) based on configurable batch sizes.
*   **Oracle Service Fee:** Allows for a mock Oracle service fee to be factored into relevant transactions.
*   **Output:** Generates a CSV file (`rwa_cost_comparison_simulated.csv`) and prints a summary table to the console, comparing average gas used and transaction costs (in ETH and USD) for each transaction type on L1 versus simulated L2 (for different batch sizes).

### Running the Cost Simulation Experiment:

1.  **Prerequisites:**
    *   Ensure Python 3.x is installed.
    *   Install required Python libraries:
        ```bash
        pip install web3 pandas
        ```
    *   **Ganache must be running** (e.g., Ganache UI or `ganache-cli`). The script defaults to `http://127.0.0.1:8545`.
    *   **Contracts must be compiled** using `truffle compile` as described in the "Installation" section above. The script relies on the JSON artifacts in the `build/contracts/` directory.

2.  **Configuration (Optional):**
    Open `rwa_l1_l2_cost_simulation.py` and review the configuration constants at the beginning of the file. You can adjust parameters like:
    *   `GANACHE_URL`
    *   `ETH_PRICE_USD`
    *   `L2_GAS_EFFICIENCY_FACTOR`
    *   `L2_FIXED_TX_FEE_ETH`
    *   `L1_BATCH_SUBMISSION_BASE_GAS`
    *   `MOCK_ORACLE_SERVICE_FEE_USD`
    *   `l2_batch_sizes_to_test`

3.  **Execute the Script:**
    Navigate to the root directory of the project in your terminal and run:
    ```bash
    python rwa_l1_l2_cost_simulation.py
    ```

4.  **View Results:**
    The script will print detailed logs of contract deployments and transaction executions. At the end, it will display the cost comparison table in the console and save it as `rwa_cost_comparison_simulated.csv` in the project's root directory.

### Summary of Simulation Results (Illustrative - based on Table 9 from the paper)

The simulation demonstrates significant potential cost reductions when using a Layer-2 solution compared to Layer-1 for RWA transactions, especially as the L2 batch size increases. Below is an illustrative summary based on the findings (assuming ETH Price: $2000 USD, L1 Gas Price: ~2.00 Gwei, Oracle Cost: $0.10 USD where applicable).

| Transaction Type             | Platform             | Avg. Gas Used     | Avg. Cost (ETH) | Avg. Cost (USD) | Oracle Cost (USD) | Notes                                      |
|------------------------------|----------------------|-------------------|-----------------|-----------------|-------------------|--------------------------------------------|
| RWA Issue (ERC-721)          | Layer-1              | 74274             | 0.00002108      | 0.0422          | N/A               | L1 GasPrice: ≈ 2.00 Gwei                   |
| RWA Issue (ERC-721)          | Layer-2 (Sim. BS=10) | 7427 (L2 OpGas)   | 0.00002009      | 0.0402          | N/A               | BS=10, L2 OpGas                            |
| RWA Issue (ERC-721)          | Layer-2 (Sim. BS=50) | 7427 (L2 OpGas)   | 0.00001353      | 0.0271          | N/A               | BS=50, L2 OpGas                            |
| RWA Transfer (ERC-20)        | Layer-1              | 52172             | 0.00001135      | 0.0227          | N/A               | L1 GasPrice: ≈ 2.00 Gwei                   |
| RWA Transfer (ERC-20)        | Layer-2 (Sim. BS=10) | 5217 (L2 OpGas)   | 0.00001964      | 0.0393          | N/A               | BS=10, L2 OpGas                            |
| RWA Transfer (ERC-20)        | Layer-2 (Sim. BS=50) | 5217 (L2 OpGas)   | 0.00001308      | 0.0262          | N/A               | BS=50, L2 OpGas                            |
| Yield Dist. (N=3)            | Layer-1              | 139544            | 0.00001367      | 0.0273          | N/A               | L1 GasPrice: ≈ 2.00 Gwei                   |
| Yield Dist. (N=3)            | Layer-2 (Sim. BS=10) | 13954 (L2 OpGas)  | 0.00002139      | 0.0428          | N/A               | BS=10, L2 OpGas                            |
| Yield Dist. (N=3)            | Layer-2 (Sim. BS=50) | 13954 (L2 OpGas)  | 0.00001483      | 0.0297          | N/A               | BS=50, L2 OpGas                            |
| Governance Vote              | Layer-1              | 73894             | 0.00000555      | 0.0111          | N/A               | L1 GasPrice: ≈ 2.00 Gwei                   |
| Governance Vote              | Layer-2 (Sim. BS=10) | 7389 (L2 OpGas)   | 0.00002008      | 0.0402          | N/A               | BS=10, L2 OpGas                            |
| Governance Vote              | Layer-2 (Sim. BS=50) | 7389 (L2 OpGas)   | 0.00001352      | 0.0270          | N/A               | BS=50, L2 OpGas                            |
| Oracle Update                | Layer-1              | 48228             | 0.00000317      | 0.0063          | 0.1000            | L1 GasPrice: ≈ 2.00 Gwei                   |
| Oracle Update                | Layer-2 (Sim. BS=10) | 4823 (L2 OpGas)   | 0.00001956      | 0.0391          | 0.1000            | BS=10, L2 OpGas                            |
| Oracle Update                | Layer-2 (Sim. BS=50) | 4823 (L2 OpGas)   | 0.00001300      | 0.0260          | 0.1000            | BS=50, L2 OpGas                            |

*Note: "Avg. Gas Used" for Layer-2 (Sim.) refers to the simulated L2 operational gas (L2 OpGas), which is a fraction of the L1 equivalent gas. The total L2 cost includes this L2 OpGas, a fixed L2 transaction fee, and the amortized L1 batch submission cost. The L1 GasPrice in the simulation was dynamically obtained from Ganache (around 2 Gwei for these runs).*

### Understanding the Simulation's Scope:

*   This is a **simulation** and provides **estimated** costs, especially for Layer-2.
*   The L2 model is simplified and aims to capture the core cost-saving mechanics of rollups (off-chain computation, batched data submission).
*   Actual L2 costs on a live network will vary based on the specific L2 solution, network congestion, L1 gas prices, and L2 fee structures.
*   The primary value is in illustrating the *relative* cost differences and the impact of parameters like batch size.

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License.

---

## Citation / Reference to Paper

This repository accompanies the research paper:

Zhao, X., Ding, J., Su, Y., Wang, H., Guo, F., Zhang, Q., & Mu, M. (2025). Scalable & secure real-world asset tokenization using ethereum staking & layer-2 solutions. *Peer-to-Peer Networking and Applications*, *18*(5), 254. [https://doi.org/10.1007/s12083-025-02032-6](https://doi.org/10.1007/s12083-025-02032-6)

If you use this code or find the accompanying paper useful in your research, please consider citing it:

```bibtex
@article{ZhaoXF2025Sep,
   author = {Zhao, Xiaofei and Ding, Jieqiong and Su, Yunqi and Wang, Hua and Guo, Fanglin and Zhang, Qianggang and Mu, Mingyang},
   title = {Scalable & secure real-world asset tokenization using ethereum staking & layer-2 solutions},
   journal = {Peer-to-Peer Networking and Applications},
   volume = {18},
   number = {5},
   pages = {254},
   abstract = {Real-world asset (RWA) tokenization holds immense promise for revolutionizing financial markets, but existing solutions face a critical bottleneck: the simultaneous need for scalability, security, and decentralized governance. Many platforms prioritize one or two of these, often at the expense of the others. Scalability and security challenges hinder its widespread adoption. This paper proposes a novel framework leveraging Ethereum staking and Layer-2 scaling solutions to address these limitations. Our framework utilizes a hybrid token standard (ERC-20/ERC-721) for representing diverse asset classes and incorporates a robust due diligence process. Uniquely, ETH staking is integrated to incentivize validators and secure the Layer-2 network, which employs Optimistic Rollups for enhanced transaction throughput and reduced costs. A decentralized oracle network provides secure real-world data feeds, while a Decentralized Autonomous Organization (DAO) governs the platform. The parameters of core system such as reward mechanism, slashing and oracle are determined by DAO. The framework acknowledges and addresses the complex and evolving regulatory landscape surrounding RWA tokenization, including considerations related to asset classification, KYC/AML compliance, and jurisdictional variations. A comprehensive security analysis identifies and mitigates potential vulnerabilities, focusing on smart contract security, oracle manipulation, and Layer-2 attacks. A case study demonstrates the practical application of the framework for metering electricity consumption in appliances. Experimental results, based on a simulated blockchain environment, validate the framework’s feasibility and efficiency, achieving significant improvements in transaction throughput and gas cost reductions compared to traditional Layer-1 solutions. These results demonstrate the potential of the framework to address the key challenges of RWA tokenization. We discuss the framework’s advantages and limitations, highlighting its novel combination of staking for Layer-2 security and a DAO-governed approach, and analyze its potential to democratize access to RWAs, enhance liquidity, and streamline asset management processes. Future research directions include exploring alternative Layer-2 solutions, enhancing security measures, and investigating interoperability with other blockchain platforms.},
   ISSN = {1936-6450},
   DOI = {10.1007/s12083-025-02032-6},
   url = {https://doi.org/10.1007/s12083-025-02032-6},
   year = {2025},
   type = {Journal Article}
}
```

---

## Image Reference (Original Project Structure)

<img src="Project File Structure.png" alt="Project File Structure" width="800" height="600">
