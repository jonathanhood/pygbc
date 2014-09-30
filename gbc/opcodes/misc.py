from ..core import *
 

@opcode(op=0xFA,size=3,clocks=16)
def handler(processor, params):
    address = ( params[1] << 8 ) + params[0]
    processor.registers["A"] = processor.memory[address]
 
