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
            for reg,op 
            in zip(registers,range(base_opcode,base_opcode + len(registers))) 
    ]

@pytest.mark.parametrize("opcode,src,dest", chain.from_iterable( [
    [("\x7F","A","A")],
    register_copy_params("A", 0x78),
    register_copy_params("B", 0x40),
    register_copy_params("C", 0x48)
]))
def test_register_copies(opcode,src,dest):
    processor = gbc.Processor()
    processor.registers[src] = 100
    gbc.run_instruction(opcode, processor)
    assert processor.program_counter == 1
    assert processor.registers[src] == 100
    assert processor.registers[dest] == 100

