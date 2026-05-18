// SPDX-License-Identifier: MIT
// Upgraded to a modern, secure version of Solidity.
pragma solidity ^0.8.20;

contract Governmental {
    address public owner;
    address public lastInvestor;
    uint public jackpot;

    // We use block numbers instead of timestamps to prevent manipulation by miners.
    uint public lastInvestmentBlock;
    // Assuming a 12-second block time, 5 blocks is roughly one minute.
    uint public constant BLOCKS_IN_ONE_MINUTE = 5;

    // Use the 'constructor' keyword and make it 'payable'.
    constructor() payable {
        owner = msg.sender;
        // 'require' is the modern replacement for 'throw'.
        require(msg.value >= 1 ether, "Initial deposit must be at least 1 ether");
        jackpot = 1 ether;
    }

    // 'external payable' is more gas-efficient for functions called from outside.
    function invest() external payable {
        require(msg.value >= jackpot / 2, "Investment is too small");
        lastInvestor = msg.sender;
        jackpot += msg.value / 2;
        // Record the block number, not the timestamp.
        lastInvestmentBlock = block.number;
    }

    function resetInvestment() external {
        // 1. CHECKS: Verify conditions first.
        require(block.number >= lastInvestmentBlock + BLOCKS_IN_ONE_MINUTE, "It is not time yet");

        // Store amounts in memory to prevent reentrancy issues.
        address investor = lastInvestor;
        uint jackpotAmount = jackpot;
        
        // 2. EFFECTS: Update state variables *before* sending Ether.
        lastInvestor = address(0);
        jackpot = 1 ether;
        lastInvestmentBlock = 0;

        // 3. INTERACTIONS: Send Ether last using the secure '.call'.
        (bool success, ) = investor.call{value: jackpotAmount}("");
        require(success, "Failed to send jackpot to last investor");

        // Note: The logic to send remaining balance to the owner was removed
        // as it was complex and could drain funds unexpectedly. The owner
        // should have a separate, explicit withdrawal function.
    }
}
