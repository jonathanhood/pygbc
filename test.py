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

class TestRegisterLoads(unittest.TestCase):
    def test_load_A_to_A(self):
        program = "\x7F"
        processor = gbc.Processor()
        processor.registers["A"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        pass
    
    def test_load_A_to_B(self):
        program = "\x78"
        processor = gbc.Processor()
        processor.registers["A"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["B"], 100)
        pass
    
    def test_load_A_to_C(self):
        program = "\x79"
        processor = gbc.Processor()
        processor.registers["A"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["C"], 100)
        pass
    
    def test_load_A_to_D(self):
        program = "\x7A"
        processor = gbc.Processor()
        processor.registers["A"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["D"], 100)
        pass
    
    def test_load_A_to_E(self):
        program = "\x7B"
        processor = gbc.Processor()
        processor.registers["A"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["E"], 100)
        pass
    
    def test_load_A_to_H(self):
        program = "\x7C"
        processor = gbc.Processor()
        processor.registers["A"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["H"], 100)
        pass
    
    def test_load_A_to_L(self):
        program = "\x7D"
        processor = gbc.Processor()
        processor.registers["A"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["L"], 100)
        pass

if __name__ == "__main__":
    unittest.main()
