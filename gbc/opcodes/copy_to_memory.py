from ..core import *

def copy_to_memory(op,src,dest):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        high, low = dest[0], dest[1]
        address = ( processor.registers[high] << 8 ) + processor.registers[low]
        processor.memory[address] = processor.registers[src]

@opcode(op=0x36,size=2,clocks=12)
def copy_immediate_to_memory(processor, params):
    address = ( processor.registers["H"] << 8 ) + processor.registers["L"]
    processor.memory[address] = params[0]

@opcode(op=0xE2,size=1,clocks=8)
def load_memory_from_accumulator_half(processor, params):
    high, low = ( 0xFF00, processor.registers["C"])
    address = ( high << 8 ) + low
    processor.memory[address] = processor.registers["A"]

copy_to_memory(op=0x02,src="A",dest="BC")
copy_to_memory(op=0x12,src="A",dest="DE")

copy_to_memory(op=0x70,src="B",dest="HL")
copy_to_memory(op=0x71,src="C",dest="HL")
copy_to_memory(op=0x72,src="D",dest="HL")
copy_to_memory(op=0x73,src="E",dest="HL")
copy_to_memory(op=0x74,src="H",dest="HL")
copy_to_memory(op=0x75,src="L",dest="HL")
copy_to_memory(op=0x77,src="A",dest="HL")

