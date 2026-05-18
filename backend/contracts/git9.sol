// SPDX-License-Identifier: MIT
// By changing the pragma to a version 0.8.0 or higher, the compiler
// automatically adds checks for integer overflows and underflows.
pragma solidity ^0.8.20;

contract Variables {

    // These are state variables, available in the entire contract
    int256  number = -10;
    uint256 anotherNumber = 5;
    uint standardNumber = 10;
    bool boolean = true;
    string aString = "A String";
    address favoriteAddress = 0x8f8e7012F8F974707A8F11C7cfFC5d45EfF5c2Ae;
    bytes32 someBytes = "bunny";

    // state variable visibility
    uint256 public publicNumber = 50;
    uint256 internal internalNumber = 10;
    uint256 private privatelNumber = 100;

    /**
     * @notice This function is now safe from integer overflows.
     * @dev If the calculation `value + _num + 5` were to exceed the maximum value of a uint,
     * the transaction would automatically fail ("revert"), protecting the contract.
     * @param _num A number to add to the local variable.
     * @return The result of the calculation.
     */
    function localVariable(uint _num) public pure returns(uint) {
        uint value = 10;
        value = value + _num + 5;
        return value;
    }


    //structs
    struct PeopleStruct{
        string name;
        uint256 id;
    }

    PeopleStruct public john = PeopleStruct("Jhon" , 20);
}
