from gbc.core import opcode
from util import perform_addition_8bit, perform_subtraction_8bit


def alu_8bit_add(op, src):
    @opcode(op=op, size=1, clocks=4)
    def handler(processor, params):
        accum = processor.registers["A"]
        value = processor.registers[src]
        result = perform_addition_8bit(accum, value)
        processor.registers["A"] = result.value
        processor.flags["zero"] = result.zero
        processor.flags["carry"] = result.carry
        processor.flags["half_carry"] = result.half_carry
        processor.flags["subtract"] = False


def alu_8bit_sub(op, src):
    @opcode(op=op, size=1, clocks=4)
    def handler(processor, params):
        accum = processor.registers["A"]
        value = processor.registers[src]
        result = perform_subtraction_8bit(accum, value)
        processor.registers["A"] = result.value
        processor.flags["zero"] = result.zero
        processor.flags["carry"] = result.carry
        processor.flags["half_carry"] = result.half_carry
        processor.flags["subtract"] = True


alu_8bit_add(0x80, "B") 
alu_8bit_add(0x81, "C") 
alu_8bit_add(0x82, "D") 
alu_8bit_add(0x83, "E") 
alu_8bit_add(0x84, "H") 
alu_8bit_add(0x85, "L") 
alu_8bit_add(0x87, "A")

alu_8bit_sub(0x90, "B")
alu_8bit_sub(0x91, "C")
alu_8bit_sub(0x92, "D")
alu_8bit_sub(0x93, "E")
alu_8bit_sub(0x94, "H")
alu_8bit_sub(0x95, "L")
alu_8bit_sub(0x97, "A")
