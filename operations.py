def _validate_address(operand):
    if not (0 <= operand <= 99):
        raise ValueError(f"Invalid memory address {operand}")


# READ
def read(operand, registers):
    _validate_address(operand)
    while True:
        try:
            read_input = int(input("insert a number: "))
            break
        except ValueError:
            print("not a number, try again.")
    registers[operand] = read_input


# WRITE
def write(operand, registers):
    _validate_address(operand)
    printing_word = registers[operand]
    print(printing_word)


# LOAD
def load(operand, registers):
    _validate_address(operand)
    memory_content = registers.get(operand, 0)

    if hasattr(memory_content, "sign"):
        sign_multiplier = 1 if memory_content.sign == "+" else -1
        value = (memory_content.code * 100) + memory_content.operand
        return value * sign_multiplier

    return int(memory_content)


# STORE
def store(operand, val, registers):
    _validate_address(operand)
    registers[operand] = val


# ADD
def add(operand, val, registers):
    _validate_address(operand)
    memory_content = registers.get(operand, 0)

    if hasattr(memory_content, "sign"):
        sign_multiplier = 1 if memory_content.sign == "+" else -1
        memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
    else:
        memory_val = int(memory_content)

    return val + memory_val


# SUBTRACT
def subtract(operand, val, registers):
    _validate_address(operand)
    memory_content = registers.get(operand, 0)

    if hasattr(memory_content, "sign"):
        sign_multiplier = 1 if memory_content.sign == "+" else -1
        memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
    else:
        memory_val = int(memory_content)

    return val - memory_val


# MULTIPLY
def multiply(operand, val, registers):
    _validate_address(operand)
    memory_content = registers.get(operand, 0)

    if hasattr(memory_content, "sign"):
        sign_multiplier = 1 if memory_content.sign == "+" else -1
        memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
    else:
        memory_val = int(memory_content)

    return val * memory_val


# DIVIDE
def divide(operand, val, registers):
    _validate_address(operand)
    memory_content = registers.get(operand, 0)

    if hasattr(memory_content, "sign"):
        sign_multiplier = 1 if memory_content.sign == "+" else -1
        memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
    else:
        memory_val = int(memory_content)

    if memory_val == 0:
        raise ZeroDivisionError("DIVIDE: divisor is zero")

    return val // memory_val


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
