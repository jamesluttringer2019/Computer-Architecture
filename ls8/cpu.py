"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.pc = 0
        self.fl = 0
        self.register = [0]*8
        self.register[7] = 0xf4
        self.sp = self.register[7]
        self.table = {1:self.hlt, 2:self.ldi, 7:self.prn, 4:self.jmp, 6:self.jne, 5:self.jeq}
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

    def alu(self, op, r1, r2):
        """ALU operations."""
        v1 = self.register[r1]
        v2 = self.register[r2]
        if op == 2: #MULT
            self.register[r1] = v1*v2
        elif op == 7: #CMP 
            if v1 == v2:
                self.fl = 1
            elif v1 > v2:
                self.fl = 2
            elif v2 > v1:
                self.fl = 4
        else:
            raise Exception("Unsupported ALU operation")
        self.pc += 3
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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            x = None
            y = None
            ir = self.ram[self.pc]
            op = int(ir[-4:],2)
            args = int(ir[:2],2)
            al = int(ir[2])
            if args > 0:
                x = int(self.ram[self.pc+1], 2)
                if args > 1:
                    y = int(self.ram[self.pc+2], 2)
            if al == 1:
                self.alu(op, x, y)
            else:
                self.table[op](x,y)


    def ldi(self, r, i):
        self.register[r] = i
        self.pc += 3
    def prn(self, r, y):
        print(f'Value at register {r}: {self.register[r]}')
        self.pc += 2
    def hlt(self, x, y):
        sys.exit()
    def push(self, r, y):
        self.sp -= 1
        val = self.register[r]
        self.ram[self.sp] = val
        self.pc += 2
    def pop(self, r, y):
        val = self.ram[self.sp]
        self.register[r] = val
        self.sp += 1
        self.pc += 2
    def jmp(self, r, y):
        address = self.register[r]
        self.pc = address
    def jeq(self, r, y):
        if self.fl == 1:
            self.jmp(r, y)
        else:
            self.pc += 2
    def jne(self, r, y):
        if self.fl != 1:
            self.jmp(r,y)
        else:
            self.pc += 2