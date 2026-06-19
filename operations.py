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


# READ
def read(operand, registers, inputval=None):
    _validate_address(operand)
    while True:
        if inputval is not None:
            raw_input = inputval.strip()
            inputval = None  # Clear after first use to avoid reuse in subsequent READs
        else:
            raw_input = input("Insert a signed 4-digit number (e.g., +1234): ").strip()

        if len(raw_input) == 5 and raw_input[0] in "+-" and raw_input[1:].isdigit():
            registers[operand] = int(raw_input)
            break
        else:
            print("[!] Invalid input. You must include a sign (+ or -) and exactly 4 digits. Try again.")


# WRITE
def write(operand, registers):
  _validate_address(operand)
  printing_word = _get_memory_val(registers.get(operand, 0))

  print(printing_word)


# LOAD
def load(operand, registers):
  _validate_address(operand)
  return _get_memory_val(registers.get(operand, 0))


# STORE
def store(operand, val, registers):
    _validate_address(operand)
    registers[operand] = val


# ADD
def add(operand, val, registers):
  _validate_address(operand)
  memory_val = _get_memory_val(registers.get(operand, 0))
  return _truncate(val + memory_val)


# SUBTRACT
def subtract(operand, val, registers):
  _validate_address(operand)
  memory_val = _get_memory_val(registers.get(operand, 0))
  return _truncate(val - memory_val)


# MULTIPLY
def multiply(operand, val, registers):
  _validate_address(operand)
  memory_val = _get_memory_val(registers.get(operand, 0))
  return _truncate(val * memory_val)


# DIVIDE
def divide(operand, val, registers):
  _validate_address(operand)
  memory_val = _get_memory_val(registers.get(operand, 0))

  if memory_val == 0:
    raise ZeroDivisionError("DIVIDE: divisor is zero")

  return _truncate(val // memory_val)  


def branch(operand):
    _validate_address(operand)
    return operand


def branch_neg(operand, accumulator):
    _validate_address(operand)
    if accumulator < 0:
        return operand
    return None


def branch_zero(operand, accumulator):
    _validate_address(operand)
    if accumulator == 0:
        return operand
    return None


def halt():
    return False
