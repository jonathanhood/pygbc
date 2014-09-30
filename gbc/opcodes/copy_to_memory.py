from ..core import *

def copy_to_memory(op,src,dest):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        high, low = dest[0], dest[1]
        address = ( processor.registers[high] << 8 ) + processor.registers[low]
        processor.memory[address] = processor.registers[src]

copy_to_memory(op=0x02,src="A",dest="BC")
copy_to_memory(op=0x12,src="A",dest="DE")

copy_to_memory(op=0x70,src="B",dest="HL")
copy_to_memory(op=0x71,src="C",dest="HL")
copy_to_memory(op=0x72,src="D",dest="HL")
copy_to_memory(op=0x73,src="E",dest="HL")
copy_to_memory(op=0x74,src="H",dest="HL")
copy_to_memory(op=0x75,src="L",dest="HL")
copy_to_memory(op=0x77,src="A",dest="HL")

