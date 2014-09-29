
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
        self.memory = [0 for _ in range(0,0xFFFF)]

def load_8bit_immediate(op, dest):
    @opcode(op=op,size=2,clocks=8)
    def handler(processor, params):
        processor.registers[dest] = params[0]

def copy_register(op, src, dest):
    @opcode(op=op,size=1,clocks=4)
    def handler(processor, params):
        processor.registers[dest] = processor.registers[src]

def load_from_memory(op,dest,addr):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        high_reg, low_reg = (addr[0], addr[1])
        address = ( processor.registers[high_reg] << 8 ) + processor.registers[low_reg]
        processor.registers[dest] = processor.memory[address]

def load_from_memory_half_addr(op,dest,addr): 
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        low_reg = processor.registers[addr]
        address = 0xFF00 + low_reg
        processor.registers[dest] = processor.memory[address]

def copy_to_memory(op,src):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        address = ( processor.registers["H"] << 8 ) + processor.registers["L"]
        processor.memory[address] = processor.registers[src]

def copy_to_memory_half_addr(op,src,addr):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        address = 0xFF00 + processor.registers[addr]
        processor.memory[address] = processor.registers[src]

def copy_immediate_to_memory(op):
    @opcode(op=op,size=2,clocks=12)
    def handler(processor, params):
        address = ( processor.registers["H"] << 8 ) + processor.registers["L"]
        processor.memory[address] = params[0]

def copy_from_immediate_address(op,dest):
    @opcode(op=op,size=3,clocks=16)
    def handler(processor, params):
        address = ( params[1] << 8 ) + params[0]
        processor.registers[dest] = processor.memory[address]
    

# Opcode Table

load_8bit_immediate(op=0x06,dest="B")
load_from_memory(op=0x0A,dest="A",addr="BC")
load_8bit_immediate(op=0x0E,dest="C")
load_from_memory(op=0x1A,dest="A",addr="DE")
load_8bit_immediate(op=0x16,dest="D")
load_8bit_immediate(op=0x1E,dest="E")
load_8bit_immediate(op=0x26,dest="H")
load_8bit_immediate(op=0x2E,dest="L")

copy_immediate_to_memory(op=0x36)

load_8bit_immediate(op=0x3E,dest="A")

copy_register(op=0x40,src="B",dest="B")
copy_register(op=0x41,src="C",dest="B")
copy_register(op=0x42,src="D",dest="B")
copy_register(op=0x43,src="E",dest="B")
copy_register(op=0x44,src="H",dest="B")
copy_register(op=0x45,src="L",dest="B")
load_from_memory(op=0x46,dest="B",addr="HL")

copy_register(op=0x48,src="B",dest="C")
copy_register(op=0x49,src="C",dest="C")
copy_register(op=0x4A,src="D",dest="C")
copy_register(op=0x4B,src="E",dest="C")
copy_register(op=0x4C,src="H",dest="C")
copy_register(op=0x4D,src="L",dest="C")
load_from_memory(op=0x4E,dest="C",addr="HL")

copy_register(op=0x50,src="B",dest="D")
copy_register(op=0x51,src="C",dest="D")
copy_register(op=0x52,src="D",dest="D")
copy_register(op=0x53,src="E",dest="D")
copy_register(op=0x54,src="H",dest="D")
copy_register(op=0x55,src="L",dest="D")
load_from_memory(op=0x56,dest="D",addr="HL")

copy_register(op=0x58,src="B",dest="E")
copy_register(op=0x59,src="C",dest="E")
copy_register(op=0x5A,src="D",dest="E")
copy_register(op=0x5B,src="E",dest="E")
copy_register(op=0x5C,src="H",dest="E")
copy_register(op=0x5D,src="L",dest="E")
load_from_memory(op=0x5E,dest="E",addr="HL")

copy_register(op=0x60,src="B",dest="H")
copy_register(op=0x61,src="C",dest="H")
copy_register(op=0x62,src="D",dest="H")
copy_register(op=0x63,src="E",dest="H")
copy_register(op=0x64,src="H",dest="H")
copy_register(op=0x65,src="L",dest="H")
load_from_memory(op=0x66,dest="H",addr="HL")

copy_register(op=0x68,src="B",dest="L")
copy_register(op=0x69,src="C",dest="L")
copy_register(op=0x6A,src="D",dest="L")
copy_register(op=0x6B,src="E",dest="L")
copy_register(op=0x6C,src="H",dest="L")
copy_register(op=0x6D,src="L",dest="L")
load_from_memory(op=0x6E,dest="L",addr="HL")

copy_to_memory(op=0x70,src="B")
copy_to_memory(op=0x71,src="C")
copy_to_memory(op=0x72,src="D")
copy_to_memory(op=0x73,src="E")
copy_to_memory(op=0x74,src="H")
copy_to_memory(op=0x75,src="L")

copy_register(op=0x78,src="B",dest="A")
copy_register(op=0x79,src="C",dest="A")
copy_register(op=0x7A,src="D",dest="A")
copy_register(op=0x7B,src="E",dest="A")
copy_register(op=0x7C,src="H",dest="A")
copy_register(op=0x7D,src="L",dest="A")
load_from_memory(op=0x7E,dest="A",addr="HL")
copy_register(op=0x7F,src="A",dest="A")

copy_to_memory_half_addr(op=0xE2,src="A",addr="C")

load_from_memory_half_addr(op=0xF2,dest="A",addr="C")
copy_from_immediate_address(op=0xFA,dest="A")


def run_instruction(program, processor):
    opcode = program[processor.program_counter]
    opcode_info = OPERATIONS[ord(opcode)]
    params = [ ord(p) for p in 
                program[processor.program_counter + 1 
                    : processor.program_counter + opcode_info["size"] 
             ]]
    processor.program_counter += opcode_info["size"]
    opcode_info["handler"](processor,params)
    
 
