registers = {i: 0 for i in range(100)}
accumulator = 0

class Instruction:
    def __init__(self, sign, code, operand):
        self.sign = sign
        self.code = code
        self.operand = operand

def split_instruction(string):
    # Parse a signed 4-digit word like +4300 into opcode + operand parts.
    output = Instruction(None, None, None)
    output.sign = string[0]
    output.code = int(string[1:3])
    output.operand = int(string[3:])
    return output


def read_program(filename, registers):
    with open(filename, 'r') as f:
        # Program words are loaded by memory address (line index), not operand value.
        for address, line in enumerate(f):
            instruction = split_instruction(line.strip())
            registers[address] = instruction

def execute_program(registers):
    pointer = 0
    while True:
        # check for invalid word before decoding an instruction.
        if pointer < 0 or pointer >= len(registers):
            print("Error: Pointer out of bounds.")
            break
        if not isinstance(registers[pointer], Instruction):
            print("Error: No instruction at pointer.")
            break
        instruction = registers[pointer]

        match instruction.code:
            case 10:  # READ:
                pass
            case 11:  # WRITE:
                pass    
            case 20:  # LOAD:
                pass
            case 21:  # STORE:
                pass
            case 30:  # ADD:
                pass
            case 31:  # SUBTRACT:
                pass
            case 32:  # DIVIDE:
                pass
            case 33:  # MULTIPLY:
                pass
            case 40:  # BRANCH:
                pass
            case 41:  # BRANCHNEG:
                pass
            case 42:  # BRANCHZERO:
                pass
            case 43:  # HALT:
                print("Program halted.")
                break
        # Default behavior: move to next sequential instruction.
        pointer += 1

def main():
    read_program('test1.txt', registers)
    for i in range(100):
        if isinstance(registers[i], Instruction):
            print(f"Register {i}: {registers[i].sign}{registers[i].code:02d}{registers[i].operand:02d}")
        else:
            print(f"Register {i}: {registers[i]}")
    execute_program(registers)

if __name__ == "__main__":
    main()