// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // 或者你实际使用的 ^0.8.x 版本

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyERC721Token is ERC721, Ownable {
    constructor(
        string memory name,
        string memory symbol,
        address initialOwner // 新增参数
    )
        ERC721(name, symbol)
        Ownable(initialOwner) // 调用 Ownable 构造函数
    {}

    function mint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
    }
}