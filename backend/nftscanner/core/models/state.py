class EVMState:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.storage = {}
        self.pc = 0
        self.path_constraints = []
        self.call_stack = []
        self.halted = False

    def copy(self):
        new = EVMState()
        new.stack = list(self.stack)
        new.memory = dict(self.memory)
        new.storage = dict(self.storage)
        new.pc = self.pc
        new.path_constraints = list(self.path_constraints)
        new.call_stack = list(self.call_stack)
        new.halted = self.halted
        return new
