import os
import tempfile
import unittest

import main
import operations


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
        


if __name__ == "__main__":
    unittest.main()
