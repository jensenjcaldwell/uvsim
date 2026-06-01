#READ
def read(operand, registers):
    #loop until user gives out a number
    while True:
        try:
            read_input = int(input("insert a number: "))
            break  
        except ValueError:
            print("not a number, try again.")
    #stores the user input into the memory number of the operand
    registers[operand] = read_input

#WRITE
def write(operand, registers):
    # copies a word from the content inside a specific register
    printing_word = registers[operand]
    # writes it to the screen
    print(printing_word)

#LOAD
def load(operand, registers):
  
  # This retrieves whatever is in the specific memory address. Will return 0 if it is missing
  memory_content = registers.get(operand, 0)

  # Checks if the content is an Introduction object.
  if hasattr(memory_content, 'sign'):
    sign_multiplier = 1 if memory_content.sign == '+' else -1
    value = (memory_content.code * 100) + memory_content.operand
    return value * sign_multiplier
  
  # if the info in the memory address is already a raw int, return it.
  return int(memory_content)

#STORE
def store(operand, val, registers):
  registers[operand] = val

#ADD
def add(operand, val, registers):
  memory_content = registers.get(operand, 0)

  if hasattr(memory_content, 'sign'):
    sign_multiplier = 1 if memory_content.sign == '+' else -1
    memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
  else:
    memory_val = int(memory_content)

  return val + memory_val


#SUBTRACT
def subtract(operand, val, registers):
  memory_content = registers.get(operand, 0)

  if hasattr(memory_content, 'sign'):
    sign_multiplier = 1 if memory_content.sign == '+' else -1
    memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
  else:
    memory_val = int(memory_content)

  return val - memory_val

#MULTIPLY
def multiply(operand, val, registers):
  memory_content = registers.get(operand, 0)

  if hasattr(memory_content, 'sign'):
    sign_multiplier = 1 if memory_content.sign == '+' else -1
    memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
  else:
    memory_val = int(memory_content)

  return val * memory_val

#DIVIDE
def divide(operand, val, registers):
  memory_content = registers.get(operand, 0)

  if hasattr(memory_content, 'sign'):
    sign_multiplier = 1 if memory_content.sign == '+' else -1
    memory_val = (memory_content.code * 100) + memory_content.operand * sign_multiplier
  else:
    memory_val = int(memory_content)

  if memory_val == 0:
    print("\nError: Dividing by 0.")

    return val

  return val // memory_val
