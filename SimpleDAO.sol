// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // 或者你实际使用的 ^0.8.x 版本

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SimpleDAO is Ownable {
    IERC20 public governanceToken;

    struct Proposal {
        string description;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
        bool exists; // 添加一个标志来表示提案是否有效，因为我们先 push 空的
        mapping(address => bool) hasVoted;
    }

    Proposal[] public proposals;

    event ProposalCreated(uint indexed proposalId, string description, address creator);
    event Voted(uint indexed proposalId, address voter, bool support, uint256 votingPower);

    constructor(
        address _governanceTokenAddress,
        address initialOwner // 新增参数
    )
        Ownable(initialOwner) // 调用 Ownable 构造函数
    {
        governanceToken = IERC20(_governanceTokenAddress);
    }

    function createProposal(string memory _description) public {
        uint proposalId = proposals.length;
        proposals.push(); // Push 一个默认初始化的 Proposal
        Proposal storage newProposal = proposals[proposalId];
        newProposal.description = _description;
        newProposal.exists = true; // 标记提案为有效
        // yesVotes, noVotes, executed 默认为 0 或 false
        // hasVoted mapping 自动为空

        emit ProposalCreated(proposalId, _description, msg.sender);
    }

    function vote(uint proposalId, bool support) public {
        require(proposalId < proposals.length && proposals[proposalId].exists, "Proposal does not exist or is invalid");
        Proposal storage p = proposals[proposalId];
        require(!p.hasVoted[msg.sender], "Already voted on this proposal");

        // 简化：每个投票者权重为1。
        // 真实场景应基于治理代币余额:
        // uint256 votingPower = governanceToken.balanceOf(msg.sender);
        // require(votingPower > 0, "No voting power");
        uint256 votingPower = 1; // 简化权重

        p.hasVoted[msg.sender] = true;
        if (support) {
            p.yesVotes += votingPower;
        } else {
            p.noVotes += votingPower;
        }

        emit Voted(proposalId, msg.sender, support, votingPower);
    }

    // 可以添加获取提案详情的函数
    function getProposal(uint proposalId) public view returns (string memory description, uint256 yesVotes, uint256 noVotes, bool executed) {
        require(proposalId < proposals.length && proposals[proposalId].exists, "Proposal does not exist or is invalid");
        Proposal storage p = proposals[proposalId];
        return (p.description, p.yesVotes, p.noVotes, p.executed);
    }

    // 可以添加执行提案的函数 (简化，不真正执行链上操作)
    function executeProposal(uint proposalId) public onlyOwner { // 只有 owner 可以执行
        require(proposalId < proposals.length && proposals[proposalId].exists, "Proposal does not exist or is invalid");
        Proposal storage p = proposals[proposalId];
        require(!p.executed, "Proposal already executed");
        require(p.yesVotes > p.noVotes, "Proposal did not pass"); // 简单的通过条件

        p.executed = true;
        // 在这里执行提案的实际逻辑...
    }
}