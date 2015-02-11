
class OpcodeHandler:
    all_handlers = {}

    def __init__(self, opcode, width, clocks, handler):
        self.opcode = opcode
        self.instruction_width = width 
        self.number_of_clocks = clocks
        self.handler = handler
        OpcodeHandler.all_handlers[opcode] = self

    def opcode_handler(self,processor,params):
        return self.handler(processor,params)

    def __str__(self):
        return "<GBC Opcode {} Width {} Clocks {}>".format(
                    self.opcode,
                    self.instruction_width,
                    self.number_of_clocks
                )

def opcode(op, size, clocks):
    def deco(func):
        # Define a new Opcode Handler
        OpcodeHandler(op,size,clocks,func)

        # Return the function by convention. It will
        # never actually be used though
        return func
    return deco

class Flags:
    def __init__(self):
        self.flags = {
            "zero" : False,
            "carry" : False,
            "half_carry" : False,
            "subtract" : False
        }

    def __setitem__(self,key,value):
        if type(value) is not bool:
            raise ValueError("{} is not a boolean value".format(value))

        if key in self.flags:
            self.flags[key] = value
        else:
            raise IndexError("{} is not a valid flag".format(key))
    
    def __getitem__(self,key):
        if key in self.flags:
            return self.flags[key]
        else:
            raise IndexError("{} is not a valid flag".format(key))
            
class Registers:
    def __init__(self):
        self.reg = {
            "A"  : 0,
            "F"  : 0,
            "B"  : 0,
            "C"  : 0,
            "D"  : 0,
            "E"  : 0,
            "H"  : 0,
            "L"  : 0,
            "SP" : 0
        }

    def __setitem__(self,key,value):
        if key in self.reg:
            self.reg[key] = value
        elif all(k in self.reg for k in key):
            # Copy the value into registers
            # 8-bits at a time. The leftmost
            # item in the key points to the
            # least-significant byte (little-endian)
            for k in key:
                self.reg[k] = value & 0x0FF
                value = value >> 8
        else:
            raise IndexError("{} is not a valid register".format(key))

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
        self.flags = Flags()
        self.memory = [0 for _ in range(0,0xFFFF)]

def run_instruction(program, processor):
    opcode = program[processor.program_counter]
    opcode_info = OpcodeHandler.all_handlers[ ord(opcode) ]
    params = [ ord(p) for p in 
                program[processor.program_counter + 1 
                    : processor.program_counter + opcode_info.instruction_width
             ]]
    processor.program_counter += opcode_info.instruction_width
    opcode_info.opcode_handler(processor,params)

def print_opcodes():
    sorted_opcodes = [opcode for opcode in OpcodeHandler.all_handlers.iterkeys()]
    sorted_opcodes.sort()
    opcode_meta = [OpcodeHandler.all_handlers[op] for op in sorted_opcodes]
    for meta in opcode_meta:
        print meta

