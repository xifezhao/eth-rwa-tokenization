# Smart Contract Project: DAO, ERC20, ERC721, and Staking

This repository contains a collection of Solidity smart contracts for a decentralized application (dApp), focusing on a Decentralized Autonomous Organization (DAO), an ERC20 token, an ERC721 NFT, and a staking mechanism.

## Overview

This project showcases the development of several key components often found in blockchain-based applications:

1.  **DAO Contract (`DAOContract.sol`):** A basic DAO contract allowing members to create and vote on proposals.
2.  **ERC20 Token (`MyERC20Token.sol`):** A standard ERC20 token contract that can be used for various purposes within the dApp.
3.  **ERC721 NFT (`MyERC721NFT.sol`):** A standard ERC721 NFT contract for creating and managing non-fungible tokens.
4.  **Token Staking Contract (`TokenStaking.sol`):** A contract that allows users to stake their ERC20 tokens and earn rewards.

## Contracts

### 1. DAO Contract (`DAOContract.sol`)

*   **Description:** This contract implements a basic Decentralized Autonomous Organization (DAO). Members can create proposals, and other members can vote on them.
*   **Key Features:**
    *   Proposal creation with a description.
    *   Voting mechanism (for and against).
    *   Proposal execution.
    *   Member management.
*   **Events:**
    *   `ProposalCreated`: Emitted when a new proposal is created.
    *   `VoteCast`: Emitted when a member votes on a proposal.
    *   `ProposalExecuted`: Emitted when a proposal is executed.

### 2. ERC20 Token (`MyERC20Token.sol`)

*   **Description:** This contract implements a standard ERC20 token. It can be used as the reward token in the staking contract or for other purposes within the dApp.
*   **Key Features:**
    *   Basic token functionality (transfer, balance, etc.).
    *   Minting and burning capabilities (if implemented).
    *   Optional: Metadata (name, symbol, decimals).

### 3. ERC721 NFT (`MyERC721NFT.sol`)

*   **Description:** This contract implements a standard ERC721 non-fungible token. It can be used to represent unique digital assets.
*   **Key Features:**
    *   Minting of unique NFTs.
    *   Ownership tracking.
    *   Metadata management (URI).

### 4. Token Staking Contract (`TokenStaking.sol`)

*   **Description:** This contract allows users to stake their ERC20 tokens and earn rewards over time.
*   **Key Features:**
    *   Staking functionality.
    *   Withdrawal of staked tokens.
    *   Reward calculation based on staked amount and time.
    *   Reward claim functionality.
*   **Events:**
    *   `Staked`: Emitted when a user stakes tokens.
    *   `Withdrawn`: Emitted when a user withdraws tokens.
    *   `RewardClaimed`: Emitted when a user claims rewards.

## Getting Started

### Prerequisites

*   Node.js and npm installed
*   Truffle or Hardhat development environment
*   Metamask or other Ethereum wallet

### Installation

1.  Clone the repository:

    ```bash
    git clone [repository_url]
    cd [repository_name]
    ```

2.  Install dependencies:

    ```bash
    npm install
    ```

3.  Install OpenZeppelin contracts:

    ```bash
    npm install @openzeppelin/contracts
    ```

4.  Compile the contracts:

    ```bash
    npx hardhat compile
    ```

### Deployment

1.  Configure your network in `hardhat.config.js` or `truffle-config.js`.
2.  Deploy the contracts to your desired network:

    ```bash
    npx hardhat run scripts/deploy.js --network <network_name>
    ```

    or

    ```bash
    truffle migrate --network <network_name>
    ```

### Usage

1.  **DAO:**
    *   Connect your wallet to the deployed contract.
    *   Create proposals and vote on them.
2.  **ERC20 Token:**
    *   Mint tokens for testing.
    *   Transfer tokens between addresses.
3.  **ERC721 NFT:**
    *   Mint NFTs for testing.
    *   View NFT ownership.
4.  **Staking:**
    *   Approve the staking contract to spend your ERC20 tokens.
    *   Stake your tokens.
    *   Withdraw staked tokens.
    *   Claim rewards.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License.

## Image Reference

*   `SCALABLE & SECURE RWA TOKENIZATION USING ETH & L-2`

