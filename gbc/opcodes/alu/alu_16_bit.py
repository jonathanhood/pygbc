from gbc.core import opcode
from util import perform_addition_16bit


def alu_16bit_add(op, src):
    @opcode(op=op, size=1, clocks=8)
    def handler(processor, params):
        accum = processor.registers["HL"]
        value = processor.registers[src]
        result = perform_addition_16bit(accum, value)
        processor.registers["HL"] = result.value
        processor.flags["zero"] = result.zero
        processor.flags["carry"] = result.carry
        processor.flags["half_carry"] = result.half_carry
        processor.flags["subtract"] = False

def alu_16bit_increment(op, reg):
    @opcode(op=op, size=1, clocks=8)
    def handler(processor, params):
        accum = processor.registers[reg]
        result = perform_addition_16bit(accum, 1)
        processor.registers[reg] = result.value

alu_16bit_add(0x09, "BC")
alu_16bit_add(0x19, "DE")
alu_16bit_add(0x29, "HL")
alu_16bit_add(0x39, "SP")

alu_16bit_increment(0x03, "BC")
alu_16bit_increment(0x13, "DE")
alu_16bit_increment(0x23, "HL")
alu_16bit_increment(0x33, "SP")


@opcode(op=0xE8, size=2, clocks=16)
def stackpointer_immediate_add(processor, params):
    accum = processor.registers["SP"]
    result = perform_addition_16bit(accum, params[0])
    processor.registers["SP"] = result.value
    processor.flags["zero"] = False
    processor.flags["carry"] = False
    processor.flags["half_carry"] = False
    processor.flags["subtract"] = False

