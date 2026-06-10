import operations
import sys

registers = {i: 0 for i in range(100)}
accumulator = 0
DEBUG = False

class Instruction:
    def __init__(self, sign, code, operand):
        self.sign = sign
        self.code = code
        self.operand = operand

def split_instruction(string):
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


def read_program(filename, registers):
    with open(filename, 'r') as f:
        # Program words are loaded by memory address (line index), not operand value.
        for address, line in enumerate(f):
            stripped = line.strip()
            if not stripped:
                continue
            instruction = split_instruction(stripped)
            registers[address] = instruction

def execute_program(registers):
    global accumulator
    pointer = 0
    running = True
    while running:
        # check for invalid word before decoding an instruction.
        if pointer < 0 or pointer >= len(registers):
            print("Error: Pointer out of bounds.")
            break
        if not isinstance(registers[pointer], Instruction):
            print("Error: No instruction at pointer.")
            break
        instruction = registers[pointer]
        advance_pointer = True

        try:
          match instruction.code:
            case 10:  # READ:
                operations.read(instruction.operand, registers)
                if DEBUG: print(f"\nREAD successful! Value stored in register: {registers[instruction.operand]}")
            case 11:  # WRITE:
                print("\n" + "=" * 30)
                print("       PROGRAM OUTPUT          ")
                print("=" * 30)
                operations.write(instruction.operand,registers) 
                print("=" * 30 + "\n")    
            case 20:  # LOAD:
                
                accumulator = operations.load(instruction.operand, registers)

                if DEBUG: print(f"\nLOAD successful! The accumulator is now: {accumulator}")
                
            case 21:  # STORE:
                
                operations.store(instruction.operand, accumulator, registers)

                if DEBUG: print(f"\nSTORE successful! Saved {accumulator} to register.\n")
                
            case 30:  # ADD:
                
                accumulator = operations.add(instruction.operand, accumulator, registers)

                if DEBUG: print(f"\nADD successful! New accumulator value is: {accumulator}")

            case 31:  # SUBTRACT:
                
                accumulator = operations.subtract(instruction.operand, accumulator, registers)

                if DEBUG: print(f"\nSUBTRACT successful! Subtracted {instruction.operand} located in register from the accumulator")

            case 32:  # DIVIDE:
                
                accumulator = operations.divide(instruction.operand, accumulator, registers)

                if DEBUG: print(f"\nDIVIDE successful! Divided the accumulator by {instruction.operand} located in register")

            case 33:  # MULTIPLY:
                
                accumulator = operations.multiply(instruction.operand, accumulator, registers)

                if DEBUG: print(f"\nMULTIPLY successful! Multiplied the accumulator by {instruction.operand} located in register")            
            
            case 40:  # BRANCH:
                pointer = operations.branch(instruction.operand)
                advance_pointer = False
            case 41:  # BRANCHNEG:
                branch_target = operations.branch_neg(instruction.operand, accumulator)
                if branch_target is not None:
                    pointer = branch_target
                    advance_pointer = False
            case 42:  # BRANCHZERO:
                branch_target = operations.branch_zero(instruction.operand, accumulator)
                if branch_target is not None:
                    pointer = branch_target
                    advance_pointer = False
            case 43:  # HALT:
                running = operations.halt()
                print("Program halted.")
                print(f"Final state of accumulator  : {accumulator}")
                advance_pointer = False
            case _:
                raise ValueError(f"Unknown opcode: {instruction.code}")

        except Exception as e:
            # If any error happens during a match case (ex: division by zero), it gets caught here.
            print(f"\n[!] RUNTIME ERROR at memory address {pointer:02d}: {e}")
            print("    Program execution aborted.")
            break          

        # Default behavior: move to next sequential instruction.
        if advance_pointer:
            pointer += 1

def main():

    if sys.argv[1:]:
        filename = sys.argv[1] 
    else:
        filename = input("Enter the filename: ")

    try:
      read_program(filename, registers)
      execute_program(registers)
    
    except FileNotFoundError:
      # This will catch if a user types the wrong file name.
      print(f"\n[!] ERROR: The file '{filename}' could not be found.")
      print("    Please check the spelling and ensure it is in the correct folder.")

    except ValueError as e:
      # This will catch if the text file is badly formatted.
      print(f"\n[!] LOAD ERROR: The file contains invalid BasicML code.")
      print(f"    Details: {e}")





if __name__ == "__main__":
    main()
