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

def alu_8bit_sbc(op, src):
    @opcode(op=op, size=1, clocks=4)
    def handler(processor, params):
        accum = processor.registers["A"]
        value = processor.registers[src]
        if processor.flags["carry"]:
            value += 1
        result = perform_subtraction_8bit(accum, value)
        processor.registers["A"] = result.value
        processor.flags["zero"] = result.zero
        processor.flags["carry"] = result.carry
        processor.flags["half_carry"] = result.half_carry
        processor.flags["subtract"] = True


def alu_8bit_and(op, src):
    @opcode(op=op, size=1, clocks=4)
    def handler(processor, params):
        accum = processor.registers["A"]
        value = processor.registers[src]
        result = accum & value

        processor.registers["A"] = result
        processor.flags["zero"] = result == 0
        processor.flags["carry"] = False
        processor.flags["half_carry"] = True
        processor.flags["subtract"] = False

def alu_8bit_or(op, src):
    @opcode(op=op, size=1, clocks=4)
    def handler(processor, params):
        accum = processor.registers["A"]
        value = processor.registers[src]
        result = accum | value

        processor.registers["A"] = result
        processor.flags["zero"] = result == 0
        processor.flags["carry"] = False
        processor.flags["half_carry"] = False
        processor.flags["subtract"] = False

def alu_8bit_xor(op, src):
    @opcode(op=op, size=1, clocks=4)
    def handler(processor, params):
        accum = processor.registers["A"]
        value = processor.registers[src]
        result = accum ^ value

        processor.registers["A"] = result
        processor.flags["zero"] = result == 0
        processor.flags["carry"] = False
        processor.flags["half_carry"] = False
        processor.flags["subtract"] = False

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

alu_8bit_sbc(0x98, "B")
alu_8bit_sbc(0x99, "C")
alu_8bit_sbc(0x9A, "D")
alu_8bit_sbc(0x9B, "E")
alu_8bit_sbc(0x9C, "H")
alu_8bit_sbc(0x9D, "L")
alu_8bit_sbc(0x9F, "A")

alu_8bit_and(0xA0, "B")
alu_8bit_and(0xA1, "C")
alu_8bit_and(0xA2, "D")
alu_8bit_and(0xA3, "E")
alu_8bit_and(0xA4, "H")
alu_8bit_and(0xA5, "L")
alu_8bit_and(0xA7, "A")

alu_8bit_or(0xB0, "B")
alu_8bit_or(0xB1, "C")
alu_8bit_or(0xB2, "D")
alu_8bit_or(0xB3, "E")
alu_8bit_or(0xB4, "H")
alu_8bit_or(0xB5, "L")
alu_8bit_or(0xB7, "A")

alu_8bit_xor(0xA8, "B")
alu_8bit_xor(0xA9, "C")
alu_8bit_xor(0xAA, "D")
alu_8bit_xor(0xAB, "E")
alu_8bit_xor(0xAC, "H")
alu_8bit_xor(0xAD, "L")
alu_8bit_xor(0xAF, "A")
