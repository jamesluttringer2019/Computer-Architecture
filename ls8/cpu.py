"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*255
        self.pc = 0
        self.register = [0]*8
        self.table = {1:self.hlt, 2:self.ldi, 7:self.prn}
    def load(self, file):
        """Load a program into memory."""
        address = 0
        with open(f'examples/{file}.ls8') as f:
            for line in f:
                instruction = line.split('#')[0]
                try:
                    int(instruction)
                except:
                    continue
                self.ram[address] = instruction
                address += 1


    def ram_read(self, pc):
        return self.ram[pc]
    
    def ram_write(self, pc, val):
        self.ram[pc] = val

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            x = None
            y = None
            ir = self.ram[self.pc]
            op = int(ir[-4:],2)
            args = int(ir[:2],2)
            if args > 0:
                x = int(self.ram[self.pc+1], 2)
                if args > 1:
                    y = int(self.ram[self.pc+2], 2)
            
            self.table[op](x,y)


    def ldi(self, r, i):
        self.register[r] = i
        self.pc += 3
    def prn(self, r, y):
        print(f'Value at register {r}: {self.register[r]}')
        self.pc += 2
    def hlt(self, x, y):
        sys.exit()