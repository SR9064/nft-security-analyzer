pragma solidity ^0.8.0;

contract Test {

    address owner;

    function mint() public {

        require(tx.origin == owner);

    }
}