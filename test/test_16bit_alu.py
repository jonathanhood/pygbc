import pytest
from gbc.core import Processor, run_instruction
import gbc.opcodes.alu.alu_16_bit

@pytest.mark.parametrize("opcode,reg", [
    ("\x09", "BC"),
    ("\x19", "DE"),
    ("\x29", "HL"),
    ("\x39", "SP"),
])
def test_16bit_adds(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["HL"] = 0x8888
    processor.registers[reg] = 0x8888
    run_instruction(program, processor)

    assert processor.registers["HL"] == 0x1110
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == True
    assert processor.flags["carry"] == True


def test_stackpointer_immediate_add():
    program = '\xE8\x10'
    processor = Processor()
    processor.registers["SP"] = 0x8888
    run_instruction(program, processor)

    assert processor.registers["SP"] == 0x8898
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == False


@pytest.mark.parametrize("opcode,reg", [
    ("\x03", "BC"),
    ("\x13", "DE"),
    ("\x23", "HL"),
    ("\x33", "SP"),
])
def test_16bit_increments(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers[reg] = 0x8888
    run_instruction(program, processor)

    assert processor.registers[reg] == 0x8889


@pytest.mark.parametrize("opcode,reg", [
    ("\x0B", "BC"),
    ("\x1B", "DE"),
    ("\x2B", "HL"),
    ("\x3B", "SP"),
])
def test_16bit_decrements(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers[reg] = 0x8888
    run_instruction(program, processor)

    assert processor.registers[reg] == 0x8887
