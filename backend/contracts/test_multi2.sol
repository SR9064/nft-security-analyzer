pragma solidity ^0.8.0;

// ---------------------------------
// Contract A
// ---------------------------------
contract A {
    B b;

    constructor(address _b) {
        b = B(_b);
    }

    function withdraw() public {
        // External call to B
        b.trigger();
    }
}


// ---------------------------------
// Contract B
// ---------------------------------
contract B {
    C c;

    constructor(address _c) {
        c = C(_c);
    }

    function trigger() public {
        // External call to C
        c.execute();
    }
}


// ---------------------------------
// Contract C
// ---------------------------------
contract C {
    A a;

    constructor(address _a) {
        a = A(_a);
    }

    function execute() public {
        // 🔥 Re-enter A → creates cycle
        a.withdraw();
    }
}
