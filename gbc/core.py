
class OpcodeFramework(type):
    handlers = {}

    @staticmethod
    def make_handler(opcode):
        return OpcodeFramework.handlers[opcode]()

    def __new__(cls, name, bases, attrs):
        result = super(OpcodeFramework, cls).__new__(cls, name, bases, attrs)
        OpcodeFramework.handlers[attrs["opcode"]] = result
        return result

def opcode(op, size, clocks):
    def deco(func):
        # Define a new Opcode Handler
        class OpcodeHandler:
            __metaclass__ = OpcodeFramework
            opcode = op
            instruction_width = size
            number_of_clocks = clocks
            def opcode_handler(self,processor,params):
                return func(processor,params) 

        # Return the function by convention. It will
        # never actually be used though
        return func
    return deco

class Processor:
    def __init__(self):
        self.program_counter = 0
        self.registers = {
            "A" : 0,
            "B" : 0,
            "C" : 0,
            "D" : 0,
            "E" : 0,
            "H" : 0,
            "L" : 0
        }
        self.memory = [0 for _ in range(0,0xFFFF)]

def run_instruction(program, processor):
    opcode = program[processor.program_counter]
    opcode_info = OpcodeFramework.make_handler( ord(opcode) )
    params = [ ord(p) for p in 
                program[processor.program_counter + 1 
                    : processor.program_counter + opcode_info.instruction_width
             ]]
    processor.program_counter += opcode_info.instruction_width
    opcode_info.opcode_handler(processor,params)
    
