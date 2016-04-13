import pytest
from gbc.core import Processor, run_instruction
from itertools import chain
from gbc.opcodes import *

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