from ...core import *

def load_8bit_immediate(op, dest):
    @opcode(op=op,size=3,clocks=12)
    def handler(processor, params):
        low, high = dest[0], dest[1]
        if dest == "SP":
            processor.registers[dest] = (params[0] << 8 ) + params[1]
        processor.registers[low] = params[0]
        processor.registers[high] = params[1]

load_8bit_immediate(op=0x01,dest="BC")
load_8bit_immediate(op=0x11,dest="DE")
load_8bit_immediate(op=0x21,dest="HL")
load_8bit_immediate(op=0x31,dest="SP")

