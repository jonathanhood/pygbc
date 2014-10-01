import pytest
import gbc
from itertools import chain

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
    processor = gbc.Processor()
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 2
    assert processor.registers[reg] == 0x21

@pytest.mark.parametrize("opcode,reg", [
    ("\x01", "BC"),
    ("\x11", "DE"),
    ("\x21", "HL"),
])
def test_16bit_loads(opcode, reg):
    program = "{}\x10\x01".format(opcode)
    processor = gbc.Processor()
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 3
    assert processor.registers[reg[0]] == 0x10
    assert processor.registers[reg[1]] == 0x01
    

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
    processor = gbc.Processor()
    processor.registers[src] = 100
    gbc.run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[src] == 100
    assert processor.registers[dest] == 100


@pytest.mark.parametrize("opcode,dest,high,low", [
    ("\x0A", "A", "B", "C"),
    ("\x1A", "A", "D", "E"),
    ("\x46", "B", "H", "L"),
    ("\x4E", "C", "H", "L"),
    ("\x56", "D", "H", "L"),
    ("\x5E", "E", "H", "L"),
    ("\x66", "H", "H", "L"),
    ("\x6E", "L", "H", "L"),
    ("\x7E", "A", "H", "L")
])
def test_load_from_memory(opcode,dest,high,low):
    processor = gbc.Processor()
    processor.memory[0x0110] = 0x5A
    processor.registers[high] = 0x10
    processor.registers[low] = 0x01
    gbc.run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[dest] == 0x5A

@pytest.mark.parametrize("opcode,dest,low", [
    ("\xF2", "A", "C"),
])
def test_load_from_memory_half_addr(opcode,dest,low):
    processor = gbc.Processor()
    processor.memory[0xFF10] = 0x5A
    processor.registers[low] = 0x10
    gbc.run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[dest] == 0x5A

@pytest.mark.parametrize("opcode,src,high,low", [
    ("\x02", "A", "B", "C"),
    ("\x12", "A", "D", "E"),
    ("\x70", "B", "H", "L"),
    ("\x71", "C", "H", "L"),
    ("\x72", "D", "H", "L"),
    ("\x73", "E", "H", "L"),
    ("\x74", "H", "H", "L"),
    ("\x75", "L", "H", "L"),
    ("\x77", "A", "H", "L")
])
def test_load_to_memory(opcode,src,high,low):
    processor = gbc.Processor()
    processor.registers[src] = 0x5A
    processor.registers[high] = 0x10
    processor.registers[low] = 0x01
    gbc.run_instruction(opcode, processor)
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
    processor = gbc.Processor()
    processor.registers[src] = 0x5A
    processor.registers[addr] = 0x01
    gbc.run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.memory[0xFF01] == 0x5A

def test_copy_immediate_to_memory():
    program = "\x36\x5A"
    processor = gbc.Processor()
    processor.registers["H"] = 0x10
    processor.registers["L"] = 0x01
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 2
    assert processor.memory[0x0110] == 0x5A

def test_copy_from_immediate_address():
    program = "\xFA\x10\x01"
    processor = gbc.Processor()
    processor.memory[0x0110] = 0x5A
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 3
    assert processor.registers["A"] == 0x5A

def test_copy_to_accum_and_decrement_addr():
    program = "\x3A"
    processor = gbc.Processor()
    processor.registers["H"] = 0x10
    processor.registers["L"] = 0x01
    processor.memory[0x0110] = 0x5A
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["A"] == 0x5A
    assert processor.registers["H"] == 0x0F
    assert processor.registers["L"] == 0x01

def test_copy_to_accum_and_increment_addr():
    program = "\x2A"
    processor = gbc.Processor()
    processor.registers["H"] = 0x10
    processor.registers["L"] = 0x01
    processor.memory[0x0110] = 0x5A
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["A"] == 0x5A
    assert processor.registers["H"] == 0x11
    assert processor.registers["L"] == 0x01

def test_copy_to_mem_and_decrement_addr():
    program = "\x32"
    processor = gbc.Processor()
    processor.registers["H"] = 0x10
    processor.registers["L"] = 0x01
    processor.registers["A"] = 0x5A
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["H"] == 0x0F
    assert processor.registers["L"] == 0x01
    assert processor.memory[0x0110] == 0x5A

def test_copy_to_mem_and_increment_addr():
    program = "\x22"
    processor = gbc.Processor()
    processor.registers["H"] = 0x10
    processor.registers["L"] = 0x01
    processor.registers["A"] = 0x5A
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 1
    assert processor.registers["H"] == 0x11
    assert processor.registers["L"] == 0x01
    assert processor.memory[0x0110] == 0x5A

def test_copy_to_mem_immediate_address():
    program = "\xE0\x11"
    processor = gbc.Processor()
    processor.registers["A"] = 0xA5
    gbc.run_instruction(program,processor)
    assert processor.program_counter == 2
    assert processor.memory[0xFF11] == 0xA5

def test_copy_from_mem_immediate_address():
    program = "\xF0\x11"
    processor = gbc.Processor()
    processor.memory[0xFF11] = 0xA5
    gbc.run_instruction(program,processor)
    assert processor.program_counter == 2
    assert processor.registers["A"] == 0xA5
