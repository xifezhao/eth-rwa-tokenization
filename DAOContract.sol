// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract DAO is Ownable {
    struct Proposal {
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    mapping(address => bool) public members;

    // Event: Triggered when a new proposal is created
    event ProposalCreated(uint256 proposalId, string description);
    // Event: Triggered when a member votes on a proposal
    event VoteCast(address indexed voter, uint256 proposalId, bool voteFor);
    // Event: Triggered when a proposal is executed
    event ProposalExecuted(uint256 proposalId);

    constructor()