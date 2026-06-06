import os
import tempfile
import unittest

import main
import operations

import io
from unittest.mock import patch


class TestMain(unittest.TestCase):
    def test_split_instruction_parses_signed_word(self):
        instruction = main.split_instruction("+4300")

        self.assertEqual(instruction.sign, "+")
        self.assertEqual(instruction.code, 43)
        self.assertEqual(instruction.operand, 0)

    def test_split_instruction_rejects_empty_line(self):
        with self.assertRaises(ValueError):
            main.split_instruction("")

    def test_read_program_skips_blank_lines(self):
        registers = {i: 0 for i in range(100)}
        program = "+1007\n\n+4300\n"

        with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
            tmp.write(program)
            tmp_path = tmp.name

        try:
            main.read_program(tmp_path, registers)
        finally:
            os.unlink(tmp_path)

        self.assertIsInstance(registers[0], main.Instruction)
        self.assertEqual(registers[0].code, 10)

        # The blank line at source line 2 is ignored; line indexing remains stable.
        self.assertIsInstance(registers[2], main.Instruction)
        self.assertEqual(registers[2].code, 43)

class TestDivision(unittest.TestCase):
    def test_divide_two_numbers(self):
        registers = {i: 0 for i in range(100)}
        registers[0] = 10
        registers[100] = 5
        result = operations.divide(0, 100, registers)
        self.assertEqual(result, 2)

class TestOperations(unittest.TestCase):
    def setUp(self):
      self.registers = {i: 0 for i in range(100)}


    #(READ)
def test_read_success(self):
    self.registers[7] = 0

    #adds input automatically
    with patch('builtins.input', return_value='55'):
        operations.read(7, self.registers)

    self.assertEqual(self.registers[7], 55)

def test_read_success_2(self):
    self.registers[7] = 0

    #adds input automatically
    with patch('builtins.input', side_effect=['abc','55']):
        operations.read(7, self.registers)

    self.assertEqual(self.registers[7], 55)


#(WRITE)
def test_write_success(self):
    self.registers[7] = 55

    with patch('sys.stdout', new=io.StringIO()) as output:
        operations.write(7, self.registers)
        
    self.assertEqual(output.getvalue(), "55\n")

def test_write_success_2(self):
    self.registers[7] = 55
    self.registers[8] = 0

    with patch('sys.stdout', new=io.StringIO()) as output:
        operations.write(8, self.registers)

    self.assertEqual(output.getvalue(), "0\n")
    
    #(LOAD)
    def test_load_success(self):
      self.registers[5] = 42

      result = operations.load(5, self.registers)
      self.assertEqual(result, 42)
    
    def test_instuctions(self):
      instruction = main.Instruction('+', 43, 0)

      self.registers[5] = instruction
      result = operations.load(5, self.registers)
      self.assertEqual(result, 4300)
        
    #(ADD)
    def test_add_success(self):
      self.registers[7] = 15

      starting_acc = 35
      result = operations.add(7, starting_acc, self.registers)
      self.assertEqual(result, 50)

    def test_string_error(self):
      self.registers[7] = "school"

      starting_acc = 10
      with self.assertRaises(ValueError):
        operations.add(7, starting_acc, self.registers)

    #(MULTIPLY)
    def test_multiply_success(self):
      self.registers[10] = 6
      starting_accumulator = 5
        
      result = operations.multiply(10, starting_accumulator, self.registers)
      self.assertEqual(result, 30)

    def test_multiply_negative(self):
      self.registers[10] = 5
      starting_accumulator = -4
        
      result = operations.multiply(10, starting_accumulator, self.registers)
      self.assertEqual(result, -20)



if __name__ == "__main__":
    unittest.main()
