from ...core import *

def copy_to_memory(op,src,dest):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        high, low = dest[1], dest[0]
        address = ( processor.registers[high] << 8 ) + processor.registers[low]
        processor.memory[address] = processor.registers[src]

@opcode(op=0x36,size=2,clocks=12)
def copy_immediate_to_memory(processor, params):
    address = processor.registers["HL"]
    processor.memory[address] = params[0]

@opcode(op=0xE2,size=1,clocks=8)
def load_memory_from_accumulator_half(processor, params):
    address = 0xFF00 + processor.registers["C"]
    processor.memory[address] = processor.registers["A"]

@opcode(0xE0,size=2,clocks=12)
def load_memory_immediate_address(processor, params):
    addr = 0xFF00 + params[0]
    processor.memory[addr] = processor.registers["A"]

def load_to_memory_modify_addr(op,func):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor,params):
        addr = processor.registers["HL"]
        processor.memory[addr] = processor.registers["A"]
        addr = func(addr)
        processor.registers["HL"] = addr

@opcode(op=0x08,size=3,clocks=20)
def copy_stackpointer(processor,params):
    addr = (params[1] << 8) + params[0]
    processor.memory[addr] = processor.registers["SP"]

load_to_memory_modify_addr(0x22,lambda x: x + 1)
load_to_memory_modify_addr(0x32,lambda x: x - 1)

copy_to_memory(op=0x02,src="A",dest="BC")
copy_to_memory(op=0x12,src="A",dest="DE")

copy_to_memory(op=0x70,src="B",dest="HL")
copy_to_memory(op=0x71,src="C",dest="HL")
copy_to_memory(op=0x72,src="D",dest="HL")
copy_to_memory(op=0x73,src="E",dest="HL")
copy_to_memory(op=0x74,src="H",dest="HL")
copy_to_memory(op=0x75,src="L",dest="HL")
copy_to_memory(op=0x77,src="A",dest="HL")

