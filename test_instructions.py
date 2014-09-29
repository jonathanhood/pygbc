import pytest
import gbc
from itertools import chain

@pytest.mark.parametrize("opcode,reg", [
    ("\x06", "B"),
    ("\x0E", "C"),
    ("\x16", "D"),
    ("\x1E", "E"),
    ("\x26", "H"),
    ("\x2E", "L")
])
def test_8bit_loads(opcode, reg):
    program = "{}\x21".format(opcode)
    processor = gbc.Processor()
    gbc.run_instruction(program, processor)
    assert processor.program_counter == 2
    assert processor.registers[reg] == 0x21
    

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
    processor.registers[high] = 0x01
    processor.registers[low] = 0x10
    gbc.run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[dest] == 0x5A

@pytest.mark.parametrize("opcode,src", [
    ("\x70", "B"),
    ("\x71", "C"),
    ("\x72", "D"),
    ("\x73", "E"),
    ("\x74", "H"),
    ("\x75", "L")
])
def test_load_to_memory(opcode,src):
    processor = gbc.Processor()
    processor.registers[src] = 0x5A
    processor.registers["H"] = 0x01
    processor.registers["L"] = 0x10
    gbc.run_instruction(opcode, processor)
    assert processor.program_counter == 1

    if src == "H":
        assert processor.memory[0x0110] == 0x01
    elif src == "L":
        assert processor.memory[0x0110] == 0x10
    else:
        assert processor.memory[0x0110] == 0x5A

def test_copy_immediate_to_memory():
    program = "\x36\x5A"
    processor = gbc.Processor()
    processor.registers["H"] = 0x01
    processor.registers["L"] = 0x10
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
