from ..core import *
 
@opcode(op=0x36,size=2,clocks=12)
def copy_immediate_to_memory(processor, params):
    address = ( processor.registers["H"] << 8 ) + processor.registers["L"]
    processor.memory[address] = params[0]

@opcode(op=0xE2,size=1,clocks=8)
def copy_to_memory_half_addr(processor, params):
    address = 0xFF00 + processor.registers["C"]
    processor.memory[address] = processor.registers["A"]
    
@opcode(op=0xF2,size=1,clocks=8)
def load_from_memory_half_addr(processor, params):
    low_reg = processor.registers["C"]
    address = 0xFF00 + low_reg
    processor.registers["A"] = processor.memory[address]

@opcode(op=0xFA,size=3,clocks=16)
def handler(processor, params):
    address = ( params[1] << 8 ) + params[0]
    processor.registers["A"] = processor.memory[address]
 
