// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/*
    LARGE NFT SYSTEM (HIGH RISK)

    Features:
    - ERC721-like NFT
    - Marketplace
    - Auction
    - Royalty logic

    Vulnerabilities:
    - Reentrancy
    - Cross-contract reentrancy
    - Missing access control
    - Unsafe mint
    - Missing zero address checks
*/

contract NFTCore {

    string public name = "TestNFT";
    string public symbol = "TNFT";

    mapping(uint256 => address) public ownerOf;
    mapping(address => uint256) public balanceOf;
    mapping(uint256 => address) public approvals;

    uint256 public totalSupply;

    // ❌ No access control
    function mint(address to, uint256 tokenId) public {
        ownerOf[tokenId] = to;
        balanceOf[to]++;
        totalSupply++;
    }

    function transfer(address to, uint256 tokenId) public {
        require(ownerOf[tokenId] == msg.sender, "Not owner");

        // ❌ External call risk
        if (to.code.length > 0) {
            INFTReceiver(to).onNFTReceived(msg.sender, tokenId);
        }

        ownerOf[tokenId] = to;
        balanceOf[msg.sender]--;
        balanceOf[to]++;
    }

    function approve(address to, uint256 tokenId) public {
        approvals[tokenId] = to;
    }

    function getApproved(uint256 tokenId) public view returns(address){
        return approvals[tokenId];
    }
}

/*
    MARKETPLACE CONTRACT
*/

contract NFTMarketplace {

    struct Listing {
        address seller;
        uint256 price;
    }

    mapping(uint256 => Listing) public listings;
    address public nft;

    constructor(address _nft) {
        nft = _nft;
    }

    function list(uint256 tokenId, uint256 price) public {
        listings[tokenId] = Listing(msg.sender, price);
    }

    function buy(uint256 tokenId) public payable {
        Listing memory l = listings[tokenId];

        require(msg.value >= l.price);

        // ❌ External call BEFORE state change
        (bool sent, ) = l.seller.call{value: msg.value}("");
        require(sent);

        NFTCore(nft).transfer(msg.sender, tokenId);

        delete listings[tokenId];
    }
}

/*
    AUCTION CONTRACT
*/

contract NFTAuction {

    struct Auction {
        address highestBidder;
        uint256 highestBid;
    }

    mapping(uint256 => Auction) public auctions;
    address public nft;

    constructor(address _nft) {
        nft = _nft;
    }

    function bid(uint256 tokenId) public payable {
        Auction storage a = auctions[tokenId];

        require(msg.value > a.highestBid);

        // ❌ Refund before update → reentrancy risk
        if (a.highestBidder != address(0)) {
            (bool sent, ) = a.highestBidder.call{value: a.highestBid}("");
            require(sent);
        }

        a.highestBidder = msg.sender;
        a.highestBid = msg.value;
    }
}

/*
    ROYALTY CONTRACT
*/

contract NFTRoyalty {

    address public creator;
    uint256 public royaltyPercent = 5;

    constructor() {
        creator = msg.sender;
    }

    function getRoyalty(uint256 price) public view returns(uint256) {
        return (price * royaltyPercent) / 100;
    }
}

/*
    ATTACK CONTRACT (FOR TESTING)
*/

contract AttackReceiver {

    address public marketplace;

    constructor(address _market) {
        marketplace = _market;
    }

    // ❌ Reentrancy attack
    function onNFTReceived(address, uint256 tokenId) public {
        NFTMarketplace(marketplace).buy{value: 1 ether}(tokenId);
    }
}

/*
    EXPANSION: MANY NFT OPERATIONS (REALISTIC SIZE)
*/

contract NFTUtils {

    function batchMint(address nft, address to, uint startId, uint count) public {
        for(uint i=0;i<count;i++){
            NFTCore(nft).mint(to, startId+i);
        }
    }

    function batchTransfer(address nft, address to, uint[] memory ids) public {
        for(uint i=0;i<ids.length;i++){
            NFTCore(nft).transfer(to, ids[i]);
        }
    }

    function dummy1(uint x) public pure returns(uint){ return x+1; }
    function dummy2(uint x) public pure returns(uint){ return x+2; }
    function dummy3(uint x) public pure returns(uint){ return x+3; }
    function dummy4(uint x) public pure returns(uint){ return x+4; }
    function dummy5(uint x) public pure returns(uint){ return x+5; }
    function dummy6(uint x) public pure returns(uint){ return x+6; }
    function dummy7(uint x) public pure returns(uint){ return x+7; }
    function dummy8(uint x) public pure returns(uint){ return x+8; }
    function dummy9(uint x) public pure returns(uint){ return x+9; }
    function dummy10(uint x) public pure returns(uint){ return x+10; }

    function dummy11(uint x) public pure returns(uint){ return x*2; }
    function dummy12(uint x) public pure returns(uint){ return x*3; }
    function dummy13(uint x) public pure returns(uint){ return x*4; }
    function dummy14(uint x) public pure returns(uint){ return x*5; }
    function dummy15(uint x) public pure returns(uint){ return x*6; }
    function dummy16(uint x) public pure returns(uint){ return x*7; }
    function dummy17(uint x) public pure returns(uint){ return x*8; }
    function dummy18(uint x) public pure returns(uint){ return x*9; }
    function dummy19(uint x) public pure returns(uint){ return x*10; }
    function dummy20(uint x) public pure returns(uint){ return x*11; }

    function dummy21(uint x) public pure returns(uint){ return x-1; }
    function dummy22(uint x) public pure returns(uint){ return x-2; }
    function dummy23(uint x) public pure returns(uint){ return x-3; }
    function dummy24(uint x) public pure returns(uint){ return x-4; }
    function dummy25(uint x) public pure returns(uint){ return x-5; }

 }
