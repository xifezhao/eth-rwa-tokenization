// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    
    // Event: Triggered when new tokens are minted
    event Minted(address indexed to, uint256 amount);

    // Event: Triggered when tokens are burned
    event Burned(address indexed from, uint256 amount);

    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

    // Mint function: Only the contract owner can call, used to create new tokens
    function mint(address to, uint256 amount) public onlyOwner {
        require(to != address(0), "Mint to the zero address");
        require(amount > 0, "Mint amount must be greater than zero");
        _mint(to, amount);
        emit Minted(to, amount);
    }

    // Burn function: Allows token holders to burn their own tokens
    function burn(uint256 amount) public {
        require(amount > 0, "Burn amount must be greater than zero");
        _burn(_msgSender(), amount);
        emit Burned(_msgSender(), amount);
    }
}
