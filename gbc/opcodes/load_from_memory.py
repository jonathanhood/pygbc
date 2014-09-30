from ..core import *

def load_from_memory(op,dest,addr):
    @opcode(op=op,size=1,clocks=8)
    def handler(processor, params):
        high_reg, low_reg = (addr[0], addr[1])
        address = ( processor.registers[high_reg] << 8 ) + processor.registers[low_reg]
        processor.registers[dest] = processor.memory[address]

@opcode(op=0xF2,size=1,clocks=8)
def load_accumulator_from__memory_half(processor, params):
    high, low = ( 0xFF, processor.registers["C"])
    address = ( high << 8 ) + low
    processor.registers["A"] = processor.memory[address]

load_from_memory(op=0x0A,dest="A",addr="BC")
load_from_memory(op=0x1A,dest="A",addr="DE")
load_from_memory(op=0x46,dest="B",addr="HL")
load_from_memory(op=0x4E,dest="C",addr="HL")
load_from_memory(op=0x56,dest="D",addr="HL")
load_from_memory(op=0x5E,dest="E",addr="HL")
load_from_memory(op=0x66,dest="H",addr="HL")
load_from_memory(op=0x6E,dest="L",addr="HL")
load_from_memory(op=0x7E,dest="A",addr="HL")

