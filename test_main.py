import io
import os
import tempfile
import unittest
from unittest.mock import patch

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
        self.assertIsInstance(registers[2], main.Instruction)
        self.assertEqual(registers[2].code, 43)

    def test_execute_program_halts_on_halt_instruction(self):
        registers = {i: 0 for i in range(100)}
        registers[0] = main.Instruction("+", 43, 0)
        registers[1] = main.Instruction("+", 99, 0)

        # If HALT works, opcode 99 is never executed.
        main.execute_program(registers)

    def test_execute_program_raises_on_invalid_instruction(self):
        registers = {i: 0 for i in range(100)}
        registers[0] = main.Instruction("+", 99, 0)

        with patch("sys.stdout", new=io.StringIO()) as output:
            main.execute_program(registers)
        console_text = output.getvalue()
        
        # Verify the try/except block caught it and printed the clean error
        self.assertIn("RUNTIME ERROR", console_text)
        self.assertIn("Unknown opcode", console_text)
        

    def test_read_program_missing_file_raises_error(self):
        # Checks if trying to read a non-existent file properly triggers a FileNotFoundError
        registers = {i: 0 for i in range(100)}
        with self.assertRaises(FileNotFoundError):
            main.read_program("this_file_does_not_exist.txt", registers)

    def test_split_instruction_malformed_format_raises_error(self):
        # Checks if passing bad text (like letters or wrong lengths) triggers a ValueError
        with self.assertRaises(ValueError):
            main.split_instruction("INVALID")
        with self.assertRaises(ValueError):
            main.split_instruction("+ABCD")
        with self.assertRaises(ValueError):
            main.split_instruction("123456") # Too long            


class TestOperations(unittest.TestCase):
    def setUp(self):
        self.registers = {i: 0 for i in range(100)}

    def test_read_success(self):
        with patch("builtins.input", return_value="+0055"):
            operations.read(7, self.registers)
        self.assertEqual(self.registers[7], 55)

    def test_read_retries_after_invalid_input(self):
        with patch("builtins.input", side_effect=["abc", "+0055"]):
            operations.read(7, self.registers)
        self.assertEqual(self.registers[7], 55)

    def test_write_success(self):
        self.registers[7] = 55
        with patch("sys.stdout", new=io.StringIO()) as output:
            operations.write(7, self.registers)
        self.assertEqual(output.getvalue(), "55\n")

    def test_write_zero_value(self):
        self.registers[8] = 0
        with patch("sys.stdout", new=io.StringIO()) as output:
            operations.write(8, self.registers)
        self.assertEqual(output.getvalue(), "0\n")

    def test_load_success(self):
        self.registers[5] = 42
        result = operations.load(5, self.registers)
        self.assertEqual(result, 42)

    def test_load_instruction_word(self):
        self.registers[5] = main.Instruction("+", 43, 0)
        result = operations.load(5, self.registers)
        self.assertEqual(result, 4300)

    def test_add_success(self):
        self.registers[7] = 15
        result = operations.add(7, 35, self.registers)
        self.assertEqual(result, 50)

    def test_store_success(self):
        operations.store(9, 1234, self.registers)
        self.assertEqual(self.registers[9], 1234)

    def test_subtract_success(self):
        self.registers[6] = 3
        result = operations.subtract(6, 10, self.registers)
        self.assertEqual(result, 7)

    def test_add_raises_on_non_numeric_register_content(self):
        self.registers[7] = "school"
        with self.assertRaises(ValueError):
            operations.add(7, 10, self.registers)

    def test_multiply_success(self):
        self.registers[10] = 6
        result = operations.multiply(10, 5, self.registers)
        self.assertEqual(result, 30)

    def test_multiply_negative(self):
        self.registers[10] = 5
        result = operations.multiply(10, -4, self.registers)
        self.assertEqual(result, -20)

    def test_divide_two_numbers(self):
        self.registers[0] = 5
        result = operations.divide(0, 10, self.registers)
        self.assertEqual(result, 2)

    def test_divide_by_zero_raises(self):
        self.registers[4] = 0
        with self.assertRaises(ZeroDivisionError):
            operations.divide(4, 10, self.registers)

    def test_branch_returns_operand_as_new_pointer(self):
        self.assertEqual(operations.branch(12), 12)

    def test_branch_neg_jumps_on_negative_accumulator(self):
        self.assertEqual(operations.branch_neg(22, -1), 22)
        self.assertIsNone(operations.branch_neg(22, 5))

    def test_branch_zero_jumps_when_accumulator_is_zero(self):
        self.assertEqual(operations.branch_zero(15, 0), 15)
        self.assertIsNone(operations.branch_zero(15, 3))

    def test_branch_raises_on_invalid_address(self):
        with self.assertRaises(ValueError):
            operations.branch(100)

    def test_halt_returns_false(self):
        self.assertFalse(operations.halt())

    def test_invalid_memory_access_raises(self):
        with self.assertRaises(ValueError):
            operations.read(100, self.registers)


    def test_add_overflow_truncation(self):
        # Setup: 8000 + 5000 = 13000. It should chop off the 1 and leave 3000.
        self.registers[7] = 8000
        starting_acc = 5000
        result = operations.add(7, starting_acc, self.registers)
        self.assertEqual(result, 3000)

    def test_multiply_overflow_truncation(self):
        # Setup: 500 * 500 = 250,000. It should truncate the higher digits and leave 0000.
        self.registers[8] = 500
        starting_acc = 500
        result = operations.multiply(8, starting_acc, self.registers)
        self.assertEqual(result, 0)


    def test_subtract_negative_math_pemdas(self):
        #reconstructed memory values apply the negative sign correctly
        instruction = main.Instruction('-', 10, 50) # Represents the word -1050
        self.registers[7] = instruction
        starting_acc = 0
        
        # Math: 0 - (-1050) = 1050
        result = operations.subtract(7, starting_acc, self.registers)
        self.assertEqual(result, 1050)

    def test_branch_zero_regression(self):
        # Verify it successfully jumps ONLY when the accumulator is exactly zero
        self.assertEqual(operations.branch_zero(15, 0), 15) # Should return 15 (Jump!)
        self.assertIsNone(operations.branch_zero(15, 99))   # Should return None (Don't jump)

    def test_branch_neg_regression(self):
        # Verify it successfully jumps ONLY when the accumulator is negative
        self.assertEqual(operations.branch_neg(22, -50), 22) # Should return 22 (Jump!)
        self.assertIsNone(operations.branch_neg(22, 50))     # Should return None (Don't jump)


if __name__ == "__main__":
    unittest.main()
