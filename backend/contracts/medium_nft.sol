pragma solidity ^0.8.0;

contract MediumNFT {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function mint(address to) public onlyOwner {
        // protected mint
    }

    function approve(address to, uint256 id) public {
        // missing ownership check
    }
}
