import pytest
from gbc.core import Registers, Flags, print_opcodes

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

def test_throw_on_bad_flag_read():
    flags = Flags()
    with pytest.raises(IndexError):
        foo = flags["something"]

def test_throw_on_bad_flag_write():
    flags = Flags()
    with pytest.raises(IndexError):
        flags["something"] = False
    with pytest.raises(ValueError):
        flags["zero"] = "hello"

