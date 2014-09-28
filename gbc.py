
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

def load_8bit_immediate(op, dest):
    @opcode(op=op,size=2,clocks=8)
    def handler(processor, params):
        processor.registers[dest] = params[0]

load_8bit_immediate(op=0x06,dest="B")
load_8bit_immediate(op=0x0E,dest="C")
load_8bit_immediate(op=0x16,dest="D")
load_8bit_immediate(op=0x1E,dest="E")
load_8bit_immediate(op=0x26,dest="H")
load_8bit_immediate(op=0x2E,dest="L")

def copy_register(op, src, dest):
    @opcode(op=op,size=1,clocks=4)
    def handler(processor, params):
        processor.registers[dest] = processor.registers[src]

copy_register(op=0x40,src="B",dest="B")
copy_register(op=0x41,src="C",dest="B")
copy_register(op=0x42,src="D",dest="B")
copy_register(op=0x43,src="E",dest="B")
copy_register(op=0x44,src="H",dest="B")
copy_register(op=0x45,src="L",dest="B")

copy_register(op=0x48,src="B",dest="C")
copy_register(op=0x49,src="C",dest="C")
copy_register(op=0x4A,src="D",dest="C")
copy_register(op=0x4B,src="E",dest="C")
copy_register(op=0x4C,src="H",dest="C")
copy_register(op=0x4D,src="L",dest="C")

copy_register(op=0x78,src="B",dest="A")
copy_register(op=0x79,src="C",dest="A")
copy_register(op=0x7A,src="D",dest="A")
copy_register(op=0x7B,src="E",dest="A")
copy_register(op=0x7C,src="H",dest="A")
copy_register(op=0x7D,src="L",dest="A")
copy_register(op=0x7F,src="A",dest="A")


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
 
