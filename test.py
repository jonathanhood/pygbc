import unittest
import gbc

class Test8BitLoads(unittest.TestCase):
    def test_load_B(self):
        program = "\x06\x21"
        processor = gbc.Processor()
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 2)
        self.assertEquals(processor.registers["B"], 0x21)
        pass
    
    def test_load_C(self):
        program = "\x0E\x21"
        processor = gbc.Processor()
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 2)
        self.assertEquals(processor.registers["C"], 0x21)
        pass
    
    def test_load_D(self):
        program = "\x16\x21"
        processor = gbc.Processor()
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 2)
        self.assertEquals(processor.registers["D"], 0x21)
        pass
    
    def test_load_E(self):
        program = "\x1E\x21"
        processor = gbc.Processor()
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 2)
        self.assertEquals(processor.registers["E"], 0x21)
        pass
    
    def test_load_H(self):
        program = "\x26\x21"
        processor = gbc.Processor()
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 2)
        self.assertEquals(processor.registers["H"], 0x21)
        pass
    
    def test_load_L(self):
        program = "\x2E\x21"
        processor = gbc.Processor()
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 2)
        self.assertEquals(processor.registers["L"], 0x21)
        pass

if __name__ == "__main__":
    unittest.main()
