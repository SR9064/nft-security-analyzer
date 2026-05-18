// SPDX-License-Identifier: MIT
// Always use a modern, secure pragma.
pragma solidity ^0.8.20;

contract Greeter {
    address public admin;

    // The modern 'constructor' keyword prevents naming mistakes.
    constructor() {
        admin = msg.sender;
    }

    // Explicitly set visibility to 'public'. 'pure' is used because
    // it doesn't read from or write to the blockchain state.
    function greet(string calldata input) public pure returns (string memory) {
        // Solidity 0.8+ has built-in string comparison.
        if (keccak256(abi.encodePacked(input)) == keccak256(abi.encodePacked(""))) {
            return "Hello, World";
        }
        return input;
    }

    // The function to destroy the contract and send funds to the admin.
    // It is 'external' and correctly protected to be callable only by the admin.
    function kill() external {
        // Only the admin can call this function.
        require(msg.sender == admin, "Only the admin can call this function");
        selfdestruct(payable(admin));
    }
}
