import operations


class Instruction:
    def __init__(self, sign, code, operand):
        self.sign = sign
        self.code = code
        self.operand = operand


class simulator:
    def __init__(self):
        self.registers = {i: 0 for i in range(100)}
        self.accumulator = 0
        self.DEBUG = False
        self.pointer = 0
        self.input_flag = False
        self.inputval = None
        self.halted = False
        self.last_error = None

    def split_instruction(self, string):
        # Parse a signed 4-digit word like +4300 into opcode + operand parts.
        if not string:
            raise ValueError("Empty instruction line")
        if len(string) != 5 or string[0] not in "+-" or not string[1:].isdigit():
            raise ValueError(f"Invalid instruction format: {string}")

        output = Instruction(None, None, None)
        output.sign = string[0]
        output.code = int(string[1:3])
        output.operand = int(string[3:])
        return output

    def read_program(self, filename):
        with open(filename, 'r') as f:
            # Program words are loaded by memory address (line index), not operand value.
            for address, line in enumerate(f):
                stripped = line.strip()
                if not stripped:
                    continue
                instruction = self.split_instruction(stripped)
                self.registers[address] = instruction

    def advance(self):
        if self.halted:
            return "HALTED"

        # Check current pointer before decoding the next instruction.
        if self.pointer < 0 or self.pointer >= len(self.registers):
            return "Error: Pointer out of bounds."
        if not isinstance(self.registers[self.pointer], Instruction):
            return "Error: No instruction at pointer."

        instruction = self.registers[self.pointer]
        result = self.execute_instruction(instruction)

        if result == "INPUT_NEEDED":
            return "INPUT_NEEDED"
        if result == "RUNTIME_ERROR":
            return "RUNTIME_ERROR"
        if result == "HALTED":
            return "HALTED"
        if isinstance(result, tuple) and result[0] == "BRANCH":
            self.pointer = result[1]
            return "OK"

        self.pointer += 1
        return "OK"

    def input_needed(self):
        if isinstance(self.registers[self.pointer], Instruction) and self.registers[self.pointer].code == 10:
            return True
        return False

    def execute_instruction(self, instruction=None):
        if instruction is None:
            instruction = self.registers[self.pointer]
        self.last_error = None
        try:
            match instruction.code:
                case 10:  # READ:
                    if self.inputval is None:
                        self.input_flag = True
                        return "INPUT_NEEDED"
                    operations.read(instruction.operand, self.registers, self.inputval)
                    if self.DEBUG: print(f"\nREAD successful! Value stored in register: {self.registers[instruction.operand]}")
                    self.input_flag = False
                    self.inputval = None
                    return "OK"
                case 11:  # WRITE:
                    operations.write(instruction.operand, self.registers)
                    return "OK"
                case 20:  # LOAD:
                    self.accumulator = operations.load(instruction.operand, self.registers)
                    if self.DEBUG: print(f"\nLOAD successful! The accumulator is now: {self.accumulator}")
                    return "OK"
                case 21:  # STORE:
                    operations.store(instruction.operand, self.accumulator, self.registers)
                    if self.DEBUG: print(f"\nSTORE successful! Saved {self.accumulator} to register.\n")
                    return "OK"
                case 30:  # ADD:
                    self.accumulator = operations.add(instruction.operand, self.accumulator, self.registers)
                    if self.DEBUG: print(f"\nADD successful! New accumulator value is: {self.accumulator}")
                    return "OK"
                case 31:  # SUBTRACT:
                    self.accumulator = operations.subtract(instruction.operand, self.accumulator, self.registers)
                    if self.DEBUG: print(f"\nSUBTRACT successful! Subtracted {instruction.operand} located in register from the accumulator")
                    return "OK"
                case 32:  # DIVIDE:
                    self.accumulator = operations.divide(instruction.operand, self.accumulator, self.registers)
                    if self.DEBUG: print(f"\nDIVIDE successful! Divided the accumulator by {instruction.operand} located in register")
                    return "OK"
                case 33:  # MULTIPLY:
                    self.accumulator = operations.multiply(instruction.operand, self.accumulator, self.registers)
                    if self.DEBUG: print(f"\nMULTIPLY successful! Multiplied the accumulator by {instruction.operand} located in register")
                    return "OK"
                case 40:  # BRANCH:
                    return ("BRANCH", operations.branch(instruction.operand))
                case 41:  # BRANCHNEG:
                    branch_target = operations.branch_neg(instruction.operand, self.accumulator)
                    if branch_target is not None:
                        return ("BRANCH", branch_target)
                    return "OK"
                case 42:  # BRANCHZERO:
                    branch_target = operations.branch_zero(instruction.operand, self.accumulator)
                    if branch_target is not None:
                        return ("BRANCH", branch_target)
                    return "OK"
                case 43:  # HALT:
                    self.halted = True
                    operations.halt()
                    return "HALTED"
                case _:
                    raise ValueError(f"Unknown opcode: {instruction.code}")

        except Exception as e:
            # If any error happens during a match case (ex: division by zero), it gets caught here.
            self.last_error = f"[!] RUNTIME ERROR at memory address {self.pointer:02d}: {e}"
            print(f"\n{self.last_error}")
            print("    Program execution aborted.")
            self.halted = True
            return "RUNTIME_ERROR"


def _validate_address(operand):
    if not (0 <= operand <= 99):
        raise ValueError(f"Invalid memory address {operand}")


def _truncate(value):
    # Overflow handling: chops off higher order digits (12345 -> 2345)
    sign = -1 if value < 0 else 1
    return (abs(value) % 10000) * sign


def _get_memory_val(memory_content):
    # Extracts the integer, fixing the PEMDAS math sign bug
    if hasattr(memory_content, "sign"):
        sign_multiplier = 1 if memory_content.sign == "+" else -1
        return ((memory_content.code * 100) + memory_content.operand) * sign_multiplier
    return int(memory_content)


class operations_machine:
    def __init__(self, registers, accumulator):
        self.registers = registers
        self.accumulator = accumulator

    # READ
    def read(self, operand):
        _validate_address(operand)

        while True:
            raw_input = input("Insert a signed 4-digit number (e.g., +1234): ").strip()

            if len(raw_input) == 5 and raw_input[0] in "+-" and raw_input[1:].isdigit():
                self.registers[operand] = int(raw_input)
                break
            else:
                print("[!] Invalid input. You must include a sign (+ or -) and exactly 4 digits. Try again.")

    # WRITE
    def write(self, operand):
        _validate_address(operand)
        printing_word = _get_memory_val(self.registers.get(operand, 0))
        print(printing_word)

    # LOAD
    def load(self, operand):
        _validate_address(operand)
        self.accumulator = _get_memory_val(self.registers.get(operand, 0))

    # STORE
    def store(self, operand):
        _validate_address(operand)
        self.registers[operand] = self.accumulator

    # ADD
    def add(self, operand):
        _validate_address(operand)
        memory_val = _get_memory_val(self.registers.get(operand, 0))
        self.accumulator = _truncate(self.accumulator + memory_val)

    # SUBTRACT
    def subtract(self, operand):
        _validate_address(operand)
        memory_val = _get_memory_val(self.registers.get(operand, 0))
        self.accumulator = _truncate(self.accumulator - memory_val)

    # MULTIPLY
    def multiply(self, operand):
        _validate_address(operand)
        memory_val = _get_memory_val(self.registers.get(operand, 0))
        self.accumulator = _truncate(self.accumulator * memory_val)

    # DIVIDE
    def divide(self, operand):
        _validate_address(operand)
        memory_val = _get_memory_val(self.registers.get(operand, 0))

        if memory_val == 0:
            raise ZeroDivisionError("DIVIDE: divisor is zero")

        self.accumulator = _truncate(self.accumulator // memory_val)

    def branch(operand):
        _validate_address(operand)
        return operand

    def branch_neg(self, operand):
        _validate_address(operand)
        if self.accumulator < 0:
            return operand
        return None

    def branch_zero(self, operand):
        _validate_address(operand)
        if self.accumulator == 0:
            return operand
        return None

    def halt():
        return False
