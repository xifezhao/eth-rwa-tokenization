// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // 或者你实际使用的 ^0.8.x 版本

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract RWAManager is Ownable {
    IERC20 public rewardToken;
    uint256 public totalRewardsDeposited;
    mapping(address => uint256) public rewardsClaimed; // 仅作示例记录，实际应用中可能不需要

    constructor(
        address _rewardTokenAddress,
        address initialOwner // 新增参数
    )
        Ownable(initialOwner) // 调用 Ownable 构造函数
    {
        rewardToken = IERC20(_rewardTokenAddress);
    }

    function depositRewardTokens(uint256 amount) public onlyOwner {
        // 确保调用者 (owner) 已经 approve 了这个合约来转移 token
        require(rewardToken.transferFrom(msg.sender, address(this), amount), "Reward token deposit failed");
        totalRewardsDeposited += amount;
    }

    // 简化版：平均分配给传入的地址列表
    // 真实场景会更复杂，例如基于持有的 RWA 代币数量或快照
    function distributeRewards(address[] memory recipients) public onlyOwner {
        uint256 numRecipients = recipients.length;
        require(numRecipients > 0, "No recipients provided");

        uint256 contractBalance = rewardToken.balanceOf(address(this));
        require(contractBalance > 0, "No rewards to distribute");

        uint256 sharePerRecipient = contractBalance / numRecipients;

        // 如果不够给每个接收者至少1 wei，则只分配给第一个接收者所有余额
        // (这是一个简化的处理方式，实际可能需要更复杂的逻辑)
        if (sharePerRecipient == 0) {
            require(rewardToken.transfer(recipients[0], contractBalance), "Transfer to first recipient failed");
            rewardsClaimed[recipients[0]] += contractBalance; // 示例记录
            return;
        }

        for (uint i = 0; i < numRecipients; i++) {
            // 再次检查余额以防万一，虽然理论上应该够
            if (rewardToken.balanceOf(address(this)) >= sharePerRecipient) {
                require(rewardToken.transfer(recipients[i], sharePerRecipient), "Reward transfer failed");
                rewardsClaimed[recipients[i]] += sharePerRecipient; // 示例记录
            } else {
                // 如果出现这种情况，说明之前的计算有误或余额不足，应停止分配
                // 或者将剩余的分配给当前用户，但这会使分配不均
                break;
            }
        }
    }
}