import pytest
from gbc.core import Registers, print_opcodes

def test_printing_all_opcodes():
    print_opcodes()

def test_throw_on_bad_write():
    regs = Registers()
    with pytest.raises(IndexError):
        regs["xy"] = 0

def test_throw_on_bad_read():
    regs = Registers()
    with pytest.raises(IndexError):
        foo = regs["xy"]
