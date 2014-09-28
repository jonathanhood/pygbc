
OPERATIONS = {}

def opcode(op, size, clocks):
    def deco(func):
        OPERATIONS[op] = {
            "opcode"    : op,
            "size"      : size,
            "clocks"    : clocks,
            "handler"   : func
        }
        return func
    return deco

class Processor:
    def __init__(self):
        self.program_counter = 0
        self.registers = {
            "A" : 0,
            "B" : 0,
            "C" : 0,
            "D" : 0,
            "E" : 0,
            "H" : 0,
            "L" : 0
        }

@opcode(op=0x06,size=2,clocks=8)
def LD_b_8bit(processor,params):
    processor.registers["B"] = params[0]

@opcode(op=0x0E,size=2,clocks=8)
def LD_c_8bit(processor,params):
    processor.registers["C"] = params[0]

@opcode(op=0x16,size=2,clocks=8)
def LD_d_8bit(processor,params):
    processor.registers["D"] = params[0]

@opcode(op=0x1E,size=2,clocks=8)
def LD_e_8bit(processor,params):
    processor.registers["E"] = params[0]

@opcode(op=0x26,size=2,clocks=8)
def LD_h_8bit(processor,params):
    processor.registers["H"] = params[0]

@opcode(op=0x2E,size=2,clocks=8)
def LD_l_8bit(processor,params):
    processor.registers["L"] = params[0]

@opcode(op=0x40,size=1,clocks=4)
def LD_B_into_B(processor,params):
    pass

@opcode(op=0x41,size=1,clocks=4)
def LD_C_into_B(processor,params):
    processor.registers["B"] = processor.registers["C"]
    pass

@opcode(op=0x42,size=1,clocks=4)
def LD_D_into_B(processor,params):
    processor.registers["B"] = processor.registers["D"]
    pass

@opcode(op=0x43,size=1,clocks=4)
def LD_E_into_B(processor,params):
    processor.registers["B"] = processor.registers["E"]
    pass

@opcode(op=0x44,size=1,clocks=4)
def LD_H_into_B(processor,params):
    processor.registers["B"] = processor.registers["H"]
    pass

@opcode(op=0x45,size=1,clocks=4)
def LD_L_into_B(processor,params):
    processor.registers["B"] = processor.registers["L"]
    pass

@opcode(op=0x45,size=1,clocks=8)
def LD_HL_into_B(processor,params):
    processor.registers["B"] = processor.registers["L"]
    pass

@opcode(op=0x7F,size=1,clocks=4)
def LD_A_into_A(processor,params):
    pass

@opcode(op=0x78,size=1,clocks=4)
def LD_B_into_A(processor,params):
    processor.registers["A"] = processor.registers["B"]
    pass

@opcode(op=0x79,size=1,clocks=4)
def LD_C_into_A(processor,params):
    processor.registers["A"] = processor.registers["C"]
    pass

@opcode(op=0x7A,size=1,clocks=4)
def LD_D_into_A(processor,params):
    processor.registers["A"] = processor.registers["D"]
    pass

@opcode(op=0x7B,size=1,clocks=4)
def LD_E_into_A(processor,params):
    processor.registers["A"] = processor.registers["E"]
    pass

@opcode(op=0x7C,size=1,clocks=4)
def LD_H_into_A(processor,params):
    processor.registers["A"] = processor.registers["H"]
    pass

@opcode(op=0x7D,size=1,clocks=4)
def LD_L_into_A(processor,params):
    processor.registers["A"] = processor.registers["L"]
    pass

@opcode(op=0x7E,size=1,clocks=4)
def LD_HL_into_A(processor,params):
    processor.registers["A"] = processor.registers["L"]
    pass

def run_instruction(program, processor):
    opcode = program[processor.program_counter]
    opcode_info = OPERATIONS[ord(opcode)]
    params = [ ord(p) for p in 
                program[processor.program_counter + 1 
                    : processor.program_counter + opcode_info["size"] 
             ]]
    processor.program_counter += opcode_info["size"]
    opcode_info["handler"](processor,params)
    
if __name__ == "__main__":
   print "Hello World"
 
