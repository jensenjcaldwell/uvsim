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

    def execute_instruction(self, instruction = None):
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
                operations.write(instruction.operand,self.registers)
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
