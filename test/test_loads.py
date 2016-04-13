import pytest
from gbc.core import Processor, run_instruction
from itertools import chain
import gbc.opcodes.loads

@pytest.mark.parametrize("opcode,reg", [
    ("\x06", "B"),
    ("\x0E", "C"),
    ("\x16", "D"),
    ("\x1E", "E"),
    ("\x26", "H"),
    ("\x2E", "L"),
    ("\x3E", "A")
])
def test_8bit_loads(opcode, reg):
    program = "{}\x21".format(opcode)
    processor = Processor()
    run_instruction(program, processor)
    assert processor.program_counter == 2
    assert processor.registers[reg] == 0x21

@pytest.mark.parametrize("opcode,reg", [
    ("\x01", "BC"),
    ("\x11", "DE"),
    ("\x21", "HL"),
    ("\x31", "SP")
])
def test_16bit_loads(opcode, reg):
    program = "{}\x10\x01".format(opcode)
    processor = Processor()
    run_instruction(program, processor)
    assert processor.program_counter == 3
    assert processor.registers[reg] == 0x0110

def register_copy_params(dest, base_opcode):
    registers = ["B","C","D","E","H","L"]
    return [ (chr(op),reg,dest)
            for op,reg
            in enumerate(registers,base_opcode)
    ]

@pytest.mark.parametrize("opcode,src,dest", chain.from_iterable( [
    [("\x7F","A","A")],
    register_copy_params("A", 0x78),
    register_copy_params("B", 0x40),
    register_copy_params("C", 0x48),
    register_copy_params("D", 0x50),
    register_copy_params("E", 0x58),
    register_copy_params("H", 0x60),
    register_copy_params("L", 0x68)
]))
def test_register_copies(opcode,src,dest):
    processor = Processor()
    processor.registers[src] = 100
    run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[src] == 100
    assert processor.registers[dest] == 100


@pytest.mark.parametrize("opcode,dest,addr", [
    ("\x0A", "A", "BC"),
    ("\x1A", "A", "DE"),
    ("\x46", "B", "HL"),
    ("\x4E", "C", "HL"),
    ("\x56", "D", "HL"),
    ("\x5E", "E", "HL"),
    ("\x66", "H", "HL"),
    ("\x6E", "L", "HL"),
    ("\x7E", "A", "HL")
])
def test_load_from_memory(opcode,dest,addr):
    processor = Processor()
    processor.memory[0x0110] = 0x5A
    processor.registers[addr] = 0x0110
    run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[dest] == 0x5A

@pytest.mark.parametrize("opcode,dest,low", [
    ("\xF2", "A", "C"),
])
def test_load_from_memory_half_addr(opcode,dest,low):
    processor = Processor()
    processor.memory[0xFF10] = 0x5A
    processor.registers[low] = 0x10
    run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[dest] == 0x5A

@pytest.mark.parametrize("opcode,src,addr", [
    ("\x02", "A", "BC"),
    ("\x12", "A", "DE"),
    ("\x70", "B", "HL"),
    ("\x71", "C", "HL"),
    ("\x72", "D", "HL"),
    ("\x73", "E", "HL"),
    ("\x74", "H", "HL"),
    ("\x75", "L", "HL"),
    ("\x77", "A", "HL")
])
def test_load_to_memory(opcode,src,addr):
    processor = Processor()
    processor.registers[src] = 0x5A
    processor.registers[addr] = 0x0110
    run_instruction(opcode, processor)
    assert processor.program_counter == 1

    if src == "H":
        assert processor.memory[0x0110] == 0x10
    elif src == "L":
        assert processor.memory[0x0110] == 0x01
    else:
        assert processor.memory[0x0110] == 0x5A

@pytest.mark.parametrize("opcode,src,addr", [
    ("\xE2", "A", "C"),
])
def test_load_to_memory_half_addr(opcode,src,addr):
    processor = Processor()
    processor.registers[src] = 0x5A
    processor.registers[addr] = 0x01
    run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.memory[0xFF01] == 0x5A

def test_copy_immediate_to_memory():
    program = "\x36\x5A"
    processor = Processor()
    processor.registers["HL"] = 0x0110
    run_instruction(program, processor)
    assert processor.program_counter == 2
    assert processor.memory[0x0110] == 0x5A

def test_copy_from_immediate_address():
    program = "\xFA\x10\x01"
    processor = Processor()
    processor.memory[0x0110] = 0x5A
    run_instruction(program, processor)
    assert processor.program_counter == 3
    assert processor.registers["A"] == 0x5A

def test_copy_to_accum_and_decrement_addr():
    program = "\x3A"
    processor = Processor()
    processor.registers["HL"] = 0x0110
    processor.memory[0x0110] = 0x5A
    run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["A"] == 0x5A
    assert processor.registers["HL"] == 0x010F

def test_copy_to_accum_and_increment_addr():
    program = "\x2A"
    processor = Processor()
    processor.registers["HL"] = 0x0110
    processor.memory[0x0110] = 0x5A
    run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["A"] == 0x5A
    assert processor.registers["HL"] == 0x0111

def test_copy_to_mem_and_decrement_addr():
    program = "\x32"
    processor = Processor()
    processor.registers["HL"] = 0x0110
    processor.registers["A"] = 0x5A
    run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["HL"] == 0x010F
    assert processor.memory[0x0110] == 0x5A

def test_copy_to_mem_and_increment_addr():
    program = "\x22"
    processor = Processor()
    processor.registers["HL"] = 0x0110
    processor.registers["A"] = 0x5A
    run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["HL"] == 0x0111
    assert processor.memory[0x0110] == 0x5A

def test_copy_to_mem_immediate_address():
    program = "\xE0\x11"
    processor = Processor()
    processor.registers["A"] = 0xA5
    run_instruction(program,processor)
    assert processor.program_counter == 2
    assert processor.memory[0xFF11] == 0xA5

def test_copy_from_mem_immediate_address():
    program = "\xF0\x11"
    processor = Processor()
    processor.memory[0xFF11] = 0xA5
    run_instruction(program,processor)
    assert processor.program_counter == 2
    assert processor.registers["A"] == 0xA5