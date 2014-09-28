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
    
    def test_load_B_to_A(self):
        program = "\x78"
        processor = gbc.Processor()
        processor.registers["B"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["B"], 100)
        pass
    
    def test_load_C_to_A(self):
        program = "\x79"
        processor = gbc.Processor()
        processor.registers["C"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["C"], 100)
        pass
    
    def test_load_D_to_A(self):
        program = "\x7A"
        processor = gbc.Processor()
        processor.registers["D"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["D"], 100)
        pass
    
    def test_load_E_to_A(self):
        program = "\x7B"
        processor = gbc.Processor()
        processor.registers["E"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["E"], 100)
        pass
    
    def test_load_H_to_A(self):
        program = "\x7C"
        processor = gbc.Processor()
        processor.registers["H"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["H"], 100)
        pass
    
    def test_load_L_to_A(self):
        program = "\x7D"
        processor = gbc.Processor()
        processor.registers["L"] = 100
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["A"], 100)
        self.assertEquals(processor.registers["L"], 100)
        pass
    
    def test_load_HL_to_A(self):
        program = "\x7E"
        processor = gbc.Processor()
        processor.registers["H"] = 0xDE
        processor.registers["L"] = 0xAD
        gbc.run_instruction(program, processor)
        self.assertEquals(processor.program_counter, 1)
        self.assertEquals(processor.registers["H"], 0xDE)
        self.assertEquals(processor.registers["L"], 0xAD)
        self.assertEquals(processor.registers["A"], 0xAD)
        pass

if __name__ == "__main__":
    unittest.main()
