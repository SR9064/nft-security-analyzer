/* =====================================
   SAFE MULTI-CONTRACT ERC-721 NFT SETUP
   Includes cross-contract reentrancy cycle
===================================== */

pragma solidity ^0.8.13;

/* -----------------------------------
   CONTRACT 1: VulnerableNFT
----------------------------------- */
contract VulnerableNFT {

    string public name = "VulnNFT";
    string public symbol = "VNFT";

    mapping(uint256 => address) public owners;
    mapping(address => uint256) public balances;
    mapping(uint256 => address) public approvals;
    mapping(uint256 => string) public tokenURI;

    uint256 public totalSupply;

    event Transfer(address indexed from, address indexed to, uint256 tokenId);

    function mint(address to, string memory uri) public {
        totalSupply++;
        owners[totalSupply] = to;
        balances[to]++;
        tokenURI[totalSupply] = uri;

        emit Transfer(address(0), to, totalSupply);
    }

    function transferFrom(address from, address to, uint256 tokenId) public {
        require(owners[tokenId] == from, "Not owner");
        // Missing approval check
        owners[tokenId] = to;
        balances[from]--;
        balances[to]++;
        emit Transfer(from, to, tokenId);
    }

    function approve(address to, uint256 tokenId) public {
        approvals[tokenId] = to;
    }

    function setTokenURI(uint256 tokenId, string memory uri) public {
        // No access control
        tokenURI[tokenId] = uri;
    }

    function ownerOf(uint256 tokenId) public view returns (address) {
        return owners[tokenId];
    }
}

/* -----------------------------------
   CONTRACT 2: NFTMarketplace
----------------------------------- */
contract NFTMarketplace {

    struct Listing {
        address seller;
        uint256 price;
    }

    mapping(uint256 => Listing) public listings;
    VulnerableNFT public nft;

    constructor(address _nft) {
        nft = VulnerableNFT(_nft);
    }

    function list(uint256 tokenId, uint256 price) public {
        listings[tokenId] = Listing(msg.sender, price);
    }

    function buy(uint256 tokenId) public payable {
        Listing memory l = listings[tokenId];
        require(msg.value >= l.price, "Not enough ETH");

        // Unsafe cross-contract call
        nft.transferFrom(l.seller, msg.sender, tokenId);

        payable(l.seller).transfer(msg.value); // reentrancy possible

        delete listings[tokenId];
    }
}

/* -----------------------------------
   CONTRACT 3: AuctionHouse
----------------------------------- */
contract AuctionHouse {

    struct Auction {
        address seller;
        uint256 highestBid;
        address highestBidder;
        bool ended;
    }

    mapping(uint256 => Auction) public auctions;
    VulnerableNFT public nft;

    constructor(address _nft) {
        nft = VulnerableNFT(_nft);
    }

    function startAuction(uint256 tokenId) public {
        auctions[tokenId] = Auction(msg.sender, 0, address(0), false);
    }

    function bid(uint256 tokenId) public payable {
        Auction storage a = auctions[tokenId];
        require(msg.value > a.highestBid, "Low bid");

        if (a.highestBidder != address(0)) {
            // Reentrancy risk
            payable(a.highestBidder).call{value: a.highestBid}("");
        }

        a.highestBid = msg.value;
        a.highestBidder = msg.sender;

        // Call back to NFT
        nft.transferFrom(a.seller, a.highestBidder, tokenId);
    }

    function endAuction(uint256 tokenId) public {
        Auction storage a = auctions[tokenId];
        require(!a.ended, "Already ended");

        a.ended = true;

        nft.transferFrom(a.seller, a.highestBidder, tokenId);
        payable(a.seller).transfer(a.highestBid);
    }
}

/* -----------------------------------
   CONTRACT 4: LazyMinter
   Cross-contract cycle to AuctionHouse
----------------------------------- */
contract LazyMinter {

    VulnerableNFT public nft;
    AuctionHouse public auction;
    mapping(bytes32 => bool) public used;

    constructor(address _nft, address _auction) {
        nft = VulnerableNFT(_nft);
        auction = AuctionHouse(_auction);
    }

    function lazyMint(address to, string memory uri, bytes32 hash, uint8 v, bytes32 r, bytes32 s) public {
        // Replay attack possible
        address signer = ecrecover(hash, v, r, s);
        require(signer != address(0), "Invalid signature");

        nft.mint(to, uri);
        used[hash] = true;

        // Cross-contract call triggers static call cycle
        if (to != address(0)) {
            auction.bid(0); // dummy tokenId for static analysis
        }
    }
}

/* -----------------------------------
   CONTRACT 5: BulkMinter
----------------------------------- */
contract BulkMinter {

    VulnerableNFT public nft;

    constructor(address _nft) {
        nft = VulnerableNFT(_nft);
    }

    function bulkMint(address to, uint256 count) public {
        for (uint256 i = 0; i < count; i++) {
            nft.mint(to, "ipfs://default");
        }
    }
}
