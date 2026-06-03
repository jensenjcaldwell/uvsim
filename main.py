import operations
import sys

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
    global accumulator
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
                operations.read(instruction.operand, registers)
            case 11:  # WRITE:
                operations.write(instruction.operand,registers)     
            case 20:  # LOAD:
                
                accumulator = operations.load(instruction.operand, registers)

                print(f"\nLOAD successful! The accumulator is now: {accumulator}")
                
            case 21:  # STORE:
                
                operations.store(instruction.operand, accumulator, registers)

                print(f"\nSTORE successful! Saved {accumulator} to register {instruction.operand}\n")
                
            case 30:  # ADD:
                
                accumulator = operations.add(instruction.operand, accumulator, registers)

                print(f"\nADD successful! New accumulator value is: {accumulator}")

            case 31:  # SUBTRACT:
                
                accumulator = operations.subtract(instruction.operand, accumulator, registers)

                print(f"\nSUBTRACT successful! Subtracted {instruction.operand} located in register from the accumulator")

            case 32:  # DIVIDE:
                
                accumulator = operations.divide(instruction.operand, accumulator, registers)

                print(f"\nDIVIDE successful! Divided the accumulator by {instruction.operand} located in register")

            case 33:  # MULTIPLY:
                
                accumulator = operations.multiply(instruction.operand, accumulator, registers)

                print(f"\nMULTIPLY successful! Multiplied the accumulator by {instruction.operand} located in register")            
            
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

    if sys.argv[1:]:
        filename = sys.argv[1]    
    else:
        filename = input("Enter the filename: ")


    read_program(filename, registers)

    execute_program(registers)


if __name__ == "__main__":
    main()
