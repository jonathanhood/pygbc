
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

class Registers:
    def __init__(self):
        self.reg = {
            "A" : 0,
            "B" : 0,
            "C" : 0,
            "D" : 0,
            "E" : 0,
            "H" : 0,
            "L" : 0
        }

    def __setitem__(self,key,value):
        self.reg[key] = value

    def __getitem__(self,key):
        if key in self.reg:
            return self.reg[key]
        elif all(k in self.reg for k in key):
            # Get the values, but reverse the key order to
            # deal with endianness
            values = [self.reg[k] for k in key[::-1]]

            # Accumulate the 8-bit values into a single
            # larger value
            shift_accumulate = lambda x, y: (x << 8) + y
            return reduce(shift_accumulate,values)
        else:
            raise IndexError("{} is not a valid register".format(key))


class Processor:
    def __init__(self):
        self.program_counter = 0
        self.registers = Registers()
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
    
