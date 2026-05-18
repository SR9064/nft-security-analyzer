pragma solidity ^0.8.0;

contract A {
    B b;

    function withdraw() public {
        b.fallbackCall();
    }
}

contract B {
    C c;

    function fallbackCall() public {
        c.attack();
    }
}

contract C {
    A a;

    function attack() public {
        a.withdraw();
    }
}
