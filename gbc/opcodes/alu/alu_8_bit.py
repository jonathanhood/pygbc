from ...core import *

class AluResult:
    def __init__(self,value,carry,half_carry,zero):
        self.value = value
        self.carry = carry
        self.half_carry = half_carry
        self.zero = zero

def perform_addition_8bit(left,right):
    new_value = (left & 0x0FF) + (right & 0x0FF)
    half_carry = (((left & 0x0F) + (right & 0x0F)) & 0x10) == 0x10
    carry = (new_value & 0x100) == 0x100
    new_value = new_value & 0x0FF 
    return AluResult(new_value,carry,half_carry,new_value == 0)

def alu_8bit_add(op,src):
    @opcode(op=op,size=1,clocks=4)
    def handler(processor, params):
        accum = processor.registers["A"]
        value = processor.registers[src]
        result = perform_addition_8bit(accum,value)
        processor.registers["A"] = result.value
        processor.flags["zero"] = result.zero
        processor.flags["carry"] = result.carry
        processor.flags["half_carry"] = result.half_carry
        processor.flags["subtract"] = False        

alu_8bit_add(0x80, "B") 
alu_8bit_add(0x81, "C") 
alu_8bit_add(0x82, "D") 
alu_8bit_add(0x83, "E") 
alu_8bit_add(0x84, "H") 
alu_8bit_add(0x85, "L") 
alu_8bit_add(0x87, "A") 