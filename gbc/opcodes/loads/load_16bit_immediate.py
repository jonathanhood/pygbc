from gbc.core import opcode


def load_16bit_immediate(op, dest):
    @opcode(op=op,size=3,clocks=12)
    def handler(processor, params):
        processor.registers[dest] = (params[1] << 8 ) + params[0]

load_16bit_immediate(op=0x01,dest="BC")
load_16bit_immediate(op=0x11,dest="DE")
load_16bit_immediate(op=0x21,dest="HL")
load_16bit_immediate(op=0x31,dest="SP")

