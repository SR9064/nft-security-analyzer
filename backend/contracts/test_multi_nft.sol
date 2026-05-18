// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// ==================================================
// MONSTER NFT VULNERABLE SETUP
// ==================================================

// ==================================================
// Cycle 1: A → B → C → A (NFT Marketplace)
// ==================================================
contract A {
    B b;
    mapping(uint256 => address) public nftOwner;

    constructor(address _b) { b = B(_b); }

    function buyNFT(uint256 tokenId) public payable {
        address owner = nftOwner[tokenId];
        nftOwner[tokenId] = msg.sender; // ❌ missing ownership check
        b.receivePayment{value: msg.value}(owner);
    }
}

contract B {
    C c;

    constructor(address _c) { c = C(_c); }

    function receivePayment(address to) public payable {
        (bool sent, ) = to.call{value: msg.value}(""); // ❌ reentrancy risk
        require(sent, "Payment failed");
        c.logSale();
    }
}

contract C {
    A a;
    constructor(address _a) { a = A(_a); }

    function logSale() public {
        a.buyNFT(1); // 🔥 multi-contract reentrancy cycle
    }
}

// ==================================================
// Cycle 2: X → Y → Z → X (ERC-721 NFT)
// ==================================================
contract X {
    Y y;
    mapping(uint256 => address) public owners;

    constructor(address _y) { y = Y(_y); }

    function mint(uint256 tokenId) public {
        owners[tokenId] = msg.sender; // ❌ missing zero address check
        y.receiveNFT(tokenId);
    }

    function transfer(uint256 tokenId, address to) public {
        owners[tokenId] = to; // ❌ missing ownership/approval check
    }
}

contract Y {
    Z z;
    constructor(address _z) { z = Z(_z); }

    function receiveNFT(uint256 tokenId) public {
        z.register(tokenId);
    }
}

contract Z {
    X x;
    constructor(address _x) { x = X(_x); }

    function register(uint256 tokenId) public {
        x.transfer(tokenId, msg.sender); // 🔥 cycle reentry
    }
}

// ==================================================
// Cycle 3: M → N → P → M (ERC-1155 NFT)
// ==================================================
contract M {
    N n;
    mapping(uint256 => mapping(address => uint256)) public balances;

    constructor(address _n) { n = N(_n); }

    function deposit(uint256 id, uint256 amount) public {
        balances[id][msg.sender] += amount;
        n.forward(id, amount);
    }
}

contract N {
    P p;
    constructor(address _p) { p = P(_p); }

    function forward(uint256 id, uint256 amount) public {
        p.complete(id, amount);
    }
}

contract P {
    M m;
    constructor(address _m) { m = M(_m); }

    function complete(uint256 id, uint256 amount) public {
        m.deposit(id, amount); // 🔥 multi-contract reentrancy cycle
    }
}

// ==================================================
// Vulnerable ERC-721 NFT
// ==================================================
contract VulnerableERC721 {
    mapping(uint256 => address) public owners;

    function mint(uint256 tokenId) public {
        owners[tokenId] = msg.sender; // ❌ missing zero address check
    }

    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        owners[tokenId] = to; // ❌ missing ownership/approval checks
    }

    function ownerOf(uint256 tokenId) public view returns(address) {
        return owners[tokenId];
    }
}

// ==================================================
// Vulnerable ERC-1155 NFT
// ==================================================
contract VulnerableERC1155 {
    mapping(uint256 => mapping(address => uint256)) public balances;

    function balanceOf(address account, uint256 id) public view returns(uint256) {
        return balances[id][account];
    }

    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes memory) public {
        balances[id][from] -= amount; // ❌ no ownership check
        balances[id][to] += amount;
    }

    function balanceOfBatch(address[] memory accounts, uint256[] memory ids) public view returns(uint256[] memory) {}
    function safeBatchTransferFrom(address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data) public {}
}

// ==================================================
// Vulnerable ERC-2981 Royalty
// ==================================================
contract VulnerableRoyaltyNFT {
    function royaltyInfo(uint256, uint256) external pure returns (address receiver, uint256 royaltyAmount) {
        return (address(0), 0); // ❌ zero address
    }
}
