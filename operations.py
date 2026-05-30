#READ

#WRITE

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

#SUBTRACT

#MULTIPLY

#DIVIDE
