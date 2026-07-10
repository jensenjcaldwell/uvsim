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
    def __init__(self, registers,accumulator):

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
    def write(self,operand):
      _validate_address(operand)
      printing_word = _get_memory_val(self.registers.get(operand, 0))

      print(printing_word)


    # LOAD
    def load(self,operand):
      _validate_address(operand)
      self.accumulator = _get_memory_val(self.registers.get(operand, 0))


    # STORE
    def store(self,operand):
        _validate_address(operand)
        self.registers[operand] = self.accumulator


    # ADD
    def add(self, operand):
      _validate_address(operand)
      memory_val = _get_memory_val(self.registers.get(operand, 0))
      self.accumulator = _truncate(self.accumulator + memory_val)


    # SUBTRACT
    def subtract(self,operand):
      _validate_address(operand)
      memory_val = _get_memory_val(self.registers.get(operand, 0))
      self.accumulator = _truncate(self.accumulator - memory_val)


    # MULTIPLY
    def multiply(self,operand):
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
