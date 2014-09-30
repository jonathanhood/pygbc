from ..core import *

def load_from_memory_half_addr(op,dest,addr): 
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        low_reg = processor.registers[addr]
        address = 0xFF00 + low_reg
        processor.registers[dest] = processor.memory[address]

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
    

copy_immediate_to_memory(op=0x36)
copy_to_memory_half_addr(op=0xE2,src="A",addr="C")
load_from_memory_half_addr(op=0xF2,dest="A",addr="C")
copy_from_immediate_address(op=0xFA,dest="A")
 
