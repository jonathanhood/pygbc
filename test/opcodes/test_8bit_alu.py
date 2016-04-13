import pytest
from gbc.core import Processor, run_instruction
import gbc.opcodes.alu.alu_8_bit

@pytest.mark.parametrize("opcode,reg", [
    ("\x87", "A"),
    ("\x80", "B"),
    ("\x81", "C"),
    ("\x82", "D"),
])
def test_basic_add(opcode,reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 5
    processor.registers[reg] = 4
    run_instruction(program,processor)

    if reg == "A":
        assert processor.registers["A"] == 8
    else:
        assert processor.registers["A"] == 9

    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == False

@pytest.mark.parametrize("opcode,reg", [
    ("\x87", "A"),
    ("\x80", "B"),
    ("\x81", "C"),
    ("\x82", "D"),
    ("\x83", "E"),
    ("\x84", "H"),
    ("\x85", "L"),
])
def test_add_half_carry(opcode,reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x08
    processor.registers[reg] = 0x08
    run_instruction(program,processor)

    assert processor.registers["A"] == 0x10
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == True
    assert processor.flags["carry"] == False

@pytest.mark.parametrize("opcode,reg", [
    ("\x87", "A"),
    ("\x80", "B"),
    ("\x81", "C"),
    ("\x82", "D"),
    ("\x83", "E"),
    ("\x84", "H"),
    ("\x85", "L"),
])
def test_add_full_carry(opcode,reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x80
    processor.registers[reg] = 0x80
    run_instruction(program,processor)

    assert processor.registers["A"] == 0
    assert processor.flags["zero"] == True
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True

@pytest.mark.parametrize("opcode,reg", [
    ("\x87", "A"),
    ("\x80", "B"),
    ("\x81", "C"),
    ("\x82", "D"),
    ("\x83", "E"),
    ("\x84", "H"),
    ("\x85", "L"),
])
def test_add_both_carry(opcode,reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x88
    processor.registers[reg] = 0x88
    run_instruction(program, processor)

    assert processor.registers["A"] == 0x10
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == True
    assert processor.flags["carry"] == True

@pytest.mark.parametrize("opcode,reg", [
    ("\x97", "A"),
    ("\x90", "B"),
    ("\x91", "C"),
    ("\x92", "D"),
    ("\x93", "E"),
    ("\x94", "H"),
    ("\x95", "L"),
])
def test_basic_sub(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 6
    processor.registers[reg] = 4
    run_instruction(program, processor)

    if reg == "A":
        assert processor.registers["A"] == 0
    else:
        assert processor.registers["A"] == 2

    assert processor.flags["zero"] == (reg == "A")
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True


@pytest.mark.parametrize("opcode,reg", [
    ("\x90", "B"),
    ("\x91", "C"),
    ("\x92", "D"),
    ("\x93", "E"),
    ("\x94", "H"),
    ("\x95", "L"),
])
def test_sub_full_borrow(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x00
    processor.registers[reg] = 0x01
    run_instruction(program, processor)

    assert processor.registers["A"] == 0x80
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == False


@pytest.mark.parametrize("opcode,reg", [
    ("\x90", "B"),
    ("\x91", "C"),
    ("\x92", "D"),
    ("\x93", "E"),
    ("\x94", "H"),
    ("\x95", "L"),
])
def test_sub_half_borrow(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x10
    processor.registers[reg] = 0x01
    run_instruction(program, processor)

    assert processor.registers["A"] == 0x0F
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True


@pytest.mark.parametrize("opcode,reg", [
    ("\x98", "B"),
    ("\x99", "C"),
    ("\x9A", "D"),
    ("\x9B", "E"),
    ("\x9C", "H"),
    ("\x9D", "L"),
])
def test_sbc_carry_set(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x10
    processor.registers[reg] = 0x01
    processor.flags["carry"] = True
    run_instruction(program, processor)

    assert processor.registers["A"] == 0xE
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True

@pytest.mark.parametrize("opcode,reg", [
    ("\x98", "B"),
    ("\x99", "C"),
    ("\x9A", "D"),
    ("\x9B", "E"),
    ("\x9C", "H"),
    ("\x9D", "L"),
])
def test_sbc_carry_set(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x10
    processor.registers[reg] = 0x01
    processor.flags["carry"] = True
    run_instruction(program, processor)

    assert processor.registers["A"] == 0xE
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True

@pytest.mark.parametrize("opcode,reg", [
    ("\x98", "B"),
    ("\x99", "C"),
    ("\x9A", "D"),
    ("\x9B", "E"),
    ("\x9C", "H"),
    ("\x9D", "L"),
])
def test_sbc_carry_cleared(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x10
    processor.registers[reg] = 0x01
    processor.flags["carry"] = False
    run_instruction(program, processor)

    assert processor.registers["A"] == 0xF
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True

@pytest.mark.parametrize("opcode,reg", [
    ("\xA0", "B"),
    ("\xA1", "C"),
    ("\xA2", "D"),
    ("\xA3", "E"),
    ("\xA4", "H"),
    ("\xA5", "L"),
])
def test_8bit_and(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x10
    processor.registers[reg] = 0x11
    run_instruction(program, processor)

    assert processor.registers["A"] == 0x10
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == True
    assert processor.flags["carry"] == False

@pytest.mark.parametrize("opcode,reg", [
    ("\xB0", "B"),
    ("\xB1", "C"),
    ("\xB2", "D"),
    ("\xB3", "E"),
    ("\xB4", "H"),
    ("\xB5", "L"),
])
def test_8bit_or(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x10
    processor.registers[reg] = 0x11
    run_instruction(program, processor)

    assert processor.registers["A"] == 0x11
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == False


@pytest.mark.parametrize("opcode,reg", [
    ("\xA8", "B"),
    ("\xA9", "C"),
    ("\xAA", "D"),
    ("\xAB", "E"),
    ("\xAC", "H"),
    ("\xAD", "L"),
])
def test_8bit_xor(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x10
    processor.registers[reg] = 0x11
    run_instruction(program, processor)

    assert processor.registers["A"] == 0x01
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == False


@pytest.mark.parametrize("opcode,reg", [
    ("\xB8", "B"),
    ("\xB9", "C"),
    ("\xBA", "D"),
    ("\xBB", "E"),
    ("\xBC", "H"),
    ("\xBD", "L"),
])
def test_8bit_cp(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers["A"] = 0x01
    processor.registers[reg] = 0x01
    run_instruction(program, processor)

    assert processor.flags["zero"] == True
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True


@pytest.mark.parametrize("opcode,reg", [
    ("\x04", "B"),
    ("\x0C", "C"),
    ("\x14", "D"),
    ("\x1C", "E"),
    ("\x24", "H"),
    ("\x2C", "L"),
])
def test_8bit_increment(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers[reg] = 0x01
    run_instruction(program, processor)

    assert processor.registers[reg] == 0x02
    assert processor.flags["zero"] == False
    assert processor.flags["subtract"] == False
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == False

@pytest.mark.parametrize("opcode,reg", [
    ("\x05", "B"),
    ("\x0D", "C"),
    ("\x15", "D"),
    ("\x1D", "E"),
    ("\x25", "H"),
    ("\x2D", "L"),
])
def test_8bit_decrement(opcode, reg):
    program = opcode
    processor = Processor()
    processor.registers[reg] = 0x01
    run_instruction(program, processor)

    assert processor.registers[reg] == 0
    assert processor.flags["zero"] == True
    assert processor.flags["subtract"] == True
    assert processor.flags["half_carry"] == False
    assert processor.flags["carry"] == True