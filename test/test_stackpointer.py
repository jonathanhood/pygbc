import pytest
from gbc.core import Processor, run_instruction
import gbc.opcodes.stackpointer
import gbc.opcodes.misc

def test_copy_sp_and_add_imm():
    program = "\xF8\x02"
    processor = Processor()
    processor.registers["SP"] = 0x03
    run_instruction(program,processor)
    assert processor.program_counter == 2
    assert processor.registers["HL"] == 0x05

def test_copy_sp():
    program = "\x08\x10\x01"
    processor = Processor()
    processor.registers["SP"] = 0x5AA5
    run_instruction(program,processor)
    assert processor.program_counter == 3
    assert processor.memory[0x0110] == 0x5AA5

@pytest.mark.parametrize("opcode,reg", [
    ("\xC5", "BC"),
    ("\xD5", "DE"),
    ("\xE5", "HL"),
    ("\xF5", "AF"),
])
def test_push_stack(opcode,reg):
    program = opcode
    processor = Processor()
    processor.registers["SP"] = 3
    processor.registers[reg] = 0xA55A
    run_instruction(program,processor)
    assert processor.registers["SP"] == 1
    assert processor.memory[3] == 0xA55A

@pytest.mark.parametrize("opcode,reg", [
    ("\xC1", "BC"),
    ("\xD1", "DE"),
    ("\xE1", "HL"),
    ("\xF1", "AF"),
])
def test_pop_stack(opcode,reg):
    program = opcode
    processor = Processor()
    processor.registers["SP"] = 3
    processor.memory[3] = 0xA55A
    run_instruction(program,processor)
    assert processor.registers["SP"] == 5
    assert processor.registers[reg] == 0xA55A

