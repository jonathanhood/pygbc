import pytest
from gbc.core import Registers

def test_throw_on_bad_write():
    regs = Registers()
    with pytest.raises(IndexError):
        regs["xy"] = 0

def test_throw_on_bad_read():
    regs = Registers()
    with pytest.raises(IndexError):
        foo = regs["xy"]
