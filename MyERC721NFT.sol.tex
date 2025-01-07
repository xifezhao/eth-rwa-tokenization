// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract MyNFT is ERC721, Ownable {
    
    // Event: Triggered when a new NFT is minted
    event NFTMinted(address indexed to, uint256 tokenId, string tokenURI);

    uint256 private _tokenIdCounter;
    string private _baseURI;

    constructor(string memory name, string memory symbol, string memory baseURI) ERC721(name, symbol) {
        _baseURI = baseURI;
    }

    // Set the base URI
    function setBaseURI(string memory baseURI) public onlyOwner {
        _baseURI = baseURI;
    }

    // Mint function: Only the contract owner can call, used to create new NFTs
    function mint(address to, string memory tokenURI) public onlyOwner {
        require(to != address(0), "Mint to the zero address");
        _tokenIdCounter++;
        _safeMint(to, _tokenIdCounter);
        _setTokenURI(_tokenIdCounter, tokenURI);
        emit NFTMinted(to, _tokenIdCounter, tokenURI);
    }

    // Override the tokenURI function to use the base URI
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        return string(abi.encodePacked(_baseURI, Strings.toString(tokenId)));
    }
}