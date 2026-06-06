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

        with self.assertRaises(ValueError):
            main.execute_program(registers)


class TestOperations(unittest.TestCase):
    def setUp(self):
        self.registers = {i: 0 for i in range(100)}

    def test_read_success(self):
        with patch("builtins.input", return_value="55"):
            operations.read(7, self.registers)
        self.assertEqual(self.registers[7], 55)

    def test_read_retries_after_invalid_input(self):
        with patch("builtins.input", side_effect=["abc", "55"]):
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


if __name__ == "__main__":
    unittest.main()
