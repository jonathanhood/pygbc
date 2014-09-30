from ..core import *

def copy_to_memory(op,src):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        address = ( processor.registers["H"] << 8 ) + processor.registers["L"]
        processor.memory[address] = processor.registers[src]


copy_to_memory(op=0x70,src="B")
copy_to_memory(op=0x71,src="C")
copy_to_memory(op=0x72,src="D")
copy_to_memory(op=0x73,src="E")
copy_to_memory(op=0x74,src="H")
copy_to_memory(op=0x75,src="L")

