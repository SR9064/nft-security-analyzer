contract A {
    B b;
    function withdraw() public { b.trigger(); }
}

contract B {
    C c;
    function trigger() public { c.execute(); }
}

contract C {
    A a;
    function execute() public { a.withdraw(); }
}
