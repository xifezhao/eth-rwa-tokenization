// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // 或者你实际使用的 ^0.8.x 版本, 比如 ^0.8.20

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyERC20Token is ERC20, Ownable {
    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply,
        address initialOwner // 新增参数
    )
        ERC20(name, symbol)
        Ownable(initialOwner) // 调用 Ownable 构造函数
    {
        // 通常 initialSupply 是给部署者的，如果 initialOwner 是部署者，这样写没问题
        // 如果希望 initialSupply 给指定的 initialOwner，则 _mint(initialOwner, initialSupply);
        _mint(msg.sender, initialSupply);
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}