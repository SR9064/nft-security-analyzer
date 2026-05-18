// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// ----------------------------
// Multi-Contract Reentrancy Setup
// ----------------------------

contract A {
    B public b;
    constructor(B _b) { b = _b; }
    function withdraw() public {
        // 🔥 Calls B → triggers multi-contract cycle
        b.trigger();
    }
}

contract B {
    C public c;
    constructor(C _c) { c = _c; }
    function trigger() public {
        // 🔥 Calls C
        c.execute();
    }
}

contract C {
    A public a;
    constructor(A _a) { a = _a; }
    function execute() public {
        // 🔥 Calls back to A → forms cycle
        a.withdraw();
    }
}

// ----------------------------
// Minimal ERC-721 NFT contract
// ----------------------------
contract NFT is A {
    mapping(uint256 => address) public owners;

    function ownerOf(uint256 tokenId) public view returns(address) {
        return owners[tokenId];
    }

    function safeTransferFrom(address from, address to, uint256 tokenId) public {}
}

// ----------------------------
// ERC-1155 minimal functions
// ----------------------------
contract ERC1155NFT {
    mapping(uint256 => mapping(address => uint256)) public balances;

    function balanceOf(address account, uint256 id) public view returns(uint256) {
        return balances[id][account];
    }

    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes memory data) public {}

    function balanceOfBatch(address[] memory accounts, uint256[] memory ids) public view returns(uint256[] memory) {}

    function safeBatchTransferFrom(address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data) public {}
}

// ----------------------------
// ERC-2981 Royalty minimal
// ----------------------------
contract RoyaltyNFT {
    function royaltyInfo(uint256 tokenId, uint256 salePrice) external pure returns (address receiver, uint256 royaltyAmount) {
        return (address(0), 0);
    }
}
