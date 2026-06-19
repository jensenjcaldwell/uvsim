import sys

import classes


def run_program(filename):
  sim = classes.simulator()
  sim.read_program(filename)

  steps = 0
  max_steps = 100000

  while True:
    status = sim.advance()

    if status == "INPUT_NEEDED" and sim.input_flag:
      # Use terminal input for READ instructions in CLI mode.
      sim.inputval = input("Insert a signed 4-digit number (e.g., +1234): ").strip()
      sim.input_flag = True
      continue

    if status == "RUNTIME_ERROR":
      return 1

    if status == "HALTED":
      print("Program halted.")
      print(f"Final state of accumulator  : {sim.accumulator}")
      return 0

    if isinstance(status, str) and status.startswith("Error"):
      print(status)
      return 1

    steps += 1
    if steps > max_steps:
      print("Error: Execution exceeded max step limit.")
      return 1


def main():
  if sys.argv[1:]:
    filename = sys.argv[1]
  else:
    filename = input("Enter the filename: ")

  try:
    return run_program(filename)
  except FileNotFoundError:
    print(f"\n[!] ERROR: The file '{filename}' could not be found.")
    print("    Please check the spelling and ensure it is in the correct folder.")
    return 1
  except ValueError as e:
    print("\n[!] LOAD ERROR: The file contains invalid BasicML code.")
    print(f"    Details: {e}")
    return 1


if __name__ == "__main__":
  raise SystemExit(main())
