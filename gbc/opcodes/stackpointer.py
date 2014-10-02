from ..core import *

def push(op,reg):
    @opcode(op=op,clocks=16,size=1)
    def handler(processor,registers):
        processor.memory[processor.registers["SP"]] = processor.registers[reg]
        processor.registers["SP"] -= 2

def pop(op,reg):
    @opcode(op=op,clocks=12,size=1)
    def handler(processor,registers):
        processor.registers[reg] = processor.memory[processor.registers["SP"]]
        processor.registers["SP"] += 2

pop(op=0xC1,reg="BC")
pop(op=0xD1,reg="DE")
pop(op=0xE1,reg="HL")
pop(op=0xF1,reg="AF")

push(op=0xC5,reg="BC")
push(op=0xD5,reg="DE")
push(op=0xE5,reg="HL")
push(op=0xF5,reg="AF")

