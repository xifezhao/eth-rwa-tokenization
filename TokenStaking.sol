// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Staking is Ownable {
    using SafeMath for uint256;

    IERC20 public stakingToken;
    mapping(address => uint256) public stakedBalance;
    uint256 public totalStaked;
    uint256 public rewardRate; // Assuming the reward rate is fixed
    uint256 public lastRewardTime;

    // Event: Triggered when a user stakes tokens
    event Staked(address indexed user, uint256 amount);
    // Event: Triggered when a user withdraws tokens
    event Withdrawn(address indexed user, uint256 amount);
    // Event: Triggered when a user claims rewards
    event RewardClaimed(address indexed user, uint256 reward);

    constructor(address _stakingToken, uint256 _rewardRate) {
        stakingToken = IERC20(_stakingToken);
        rewardRate = _rewardRate;
        lastRewardTime = block.timestamp;
    }

    // Set the reward rate
    function setRewardRate(uint256 _rewardRate) public onlyOwner {
        rewardRate = _rewardRate;
    }

    // Stake function
    function stake(uint256 amount) public {
        require(amount > 0, "Amount must be greater than zero");
        stakingToken.transferFrom(msg.sender, address(this), amount);
        stakedBalance[msg.sender] = stakedBalance[msg.sender].add(amount);
        totalStaked = totalStaked.add(amount);
        lastRewardTime = block.timestamp;
        emit Staked(msg.sender, amount);
    }

    // Withdraw function
    function withdraw(uint256 amount) public {
        require(amount > 0, "Amount must be greater than zero");
        require(stakedBalance[msg.sender] >= amount, "Insufficient balance");
        stakingToken.transfer(msg.sender, amount);
        stakedBalance[msg.sender] = stakedBalance[msg.sender].sub(amount);
        totalStaked = totalStaked.sub(amount);
        lastRewardTime = block.timestamp;
        emit Withdrawn(msg.sender, amount);
    }

    // Claim reward function
    function claimReward() public {
        uint256 reward = calculateReward(msg.sender);
        require(reward > 0, "No reward to claim");
        stakingToken.transfer(msg.sender, reward);
        lastRewardTime = block.timestamp;
        emit RewardClaimed(msg.sender, reward);
    }

    // Calculate reward function
    function calculateReward(address user) public view returns (uint256) {
        uint256 timeElapsed = block.timestamp - lastRewardTime;
        uint256 reward = (stakedBalance[user] * rewardRate * timeElapsed) / 100;
        return reward;
    }
}