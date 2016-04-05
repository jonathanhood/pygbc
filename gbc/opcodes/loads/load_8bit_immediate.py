from ...core import *


def load_8bit_immediate(op, dest):
    @opcode(op=op, size=2, clocks=8)
    def handler(processor, params):
        processor.registers[dest] = params[0]

load_8bit_immediate(op=0x06, dest="B")
load_8bit_immediate(op=0x0E, dest="C")
load_8bit_immediate(op=0x16, dest="D")
load_8bit_immediate(op=0x1E, dest="E")
load_8bit_immediate(op=0x26, dest="H")
load_8bit_immediate(op=0x2E, dest="L")
load_8bit_immediate(op=0x3E, dest="A")
