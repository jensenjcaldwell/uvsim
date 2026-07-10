# UVSim Software Requirements Specification (SRS)

## 1. Functional Requirements

FR-1: The app shall be able to load a BasicML program from a text file. In the GUI, the user should be able to choose the file with the "Open File" button instead of typing a fixed file path.

FR-2: The app shall let the user view and edit BasicML code inside the GUI before running the program.

FR-3: The app shall run BasicML instructions in order, one instruction at a time, until it reaches a HALT instruction or an error.

FR-4: The app shall show WRITE output to the user. In the GUI, WRITE output should appear in the scrolling Program Output box. In the CLI version, WRITE output should print to the terminal.

FR-5: The app shall support arithmetic instructions, including ADD, SUBTRACT, MULTIPLY, and DIVIDE.

FR-6: The app shall support branching instructions, including BRANCH, BRANCHNEG, and BRANCHZERO.

FR-7: The app shall support the READ instruction. READ should accept a 4-digit number with or without a sign, so values like `1234`, `0042`, `+1234`, and `-0042` are valid.

FR-8: The app shall support LOAD and STORE instructions for moving values between memory and the accumulator.

FR-9: The app shall support the HALT instruction to end the program.

FR-10: The app shall detect runtime errors without crashing. This includes things like dividing by zero, using an invalid opcode, or trying to access an invalid memory address.

FR-11: The app shall use the UVU color scheme by default, with UVU green `#4C721D` as the primary color and white `#FFFFFF` as the off-color.

FR-12: The app shall let the user change the color theme from the GUI without changing the source code.

FR-13: The app shall save the user's selected color theme so the app can use it again later.

FR-14: The app shall let the user save the current BasicML code from the editor to a text file by using the "Save As" button.

FR-15: The app shall keep the BasicML memory limit at 100 entries, from memory locations `00` through `99`.

FR-16: The app shall stop the user from running a program if the editor contains more than 100 non-blank lines.


## 2. Use Cases

### Use Case: Change Color Theme

**Actor:** User

**Preconditions:** The GUI app is open.

**Main Flow:**
1. The user clicks the "Color Theme" button.
2. The app opens a color settings window.
3. The user enters a primary color and an off-color using hex values.
4. The user clicks "Save".
5. The app checks that the entered colors are valid hex colors.
6. The app applies the new colors to the GUI.
7. The app saves the colors so they can be used again later.

**Alternate Flow — Invalid Color Value:**
1. If the user enters an invalid color value, the app shows an error message.
2. The app does not save the invalid color scheme.

**Alternate Flow — Reset Colors:**
1. The user clicks the reset option.
2. The app restores the default UVU green and white color scheme.

**Postconditions:** The GUI uses the selected color scheme, and the saved color settings are available the next time the app starts.


---

### Use Case: Open Program with File Dialog

**Actor:** User

**Preconditions:** The GUI app is open.

**Main Flow:**
1. The user clicks the "Open File" button.
2. The app opens a file selection window.
3. The user chooses a `.txt` file from any folder on their computer.
4. The app reads the file.
5. The app loads the file contents into the code editor.

**Alternate Flow — User Cancels:**
1. If the user cancels the file dialog, the app does not change the code editor.

**Postconditions:** The selected program is shown in the code editor and can be viewed, changed, saved, or run.


---

### Use Case: Save Program with File Dialog

**Actor:** User

**Preconditions:** The GUI app is open and the code editor has BasicML code in it.

**Main Flow:**
1. The user edits or enters BasicML code in the code editor.
2. The user clicks the "Save As" button.
3. The app opens a save-file window.
4. The user chooses the file name and folder location.
5. The app saves the current code editor contents as a `.txt` file.

**Alternate Flow — User Cancels:**
1. If the user cancels the save dialog, the app does not save a file.

**Postconditions:** The current BasicML code is saved to the location the user picked.


---

### Use Case: Edit Program in Code Editor

**Actor:** User

**Preconditions:** The GUI app is open.

**Main Flow:**
1. The user loads a BasicML file or types code directly into the code editor.
2. The user can add, delete, copy, paste, or manually change the BasicML lines.
3. The user clicks "Run Code".
4. The app reads the code from the editor, not from the original file path.
5. The app runs the edited code.

**Alternate Flow — Too Many Lines:**
1. If the editor has more than 100 non-blank lines, the app shows an error.
2. The app does not run the program until the line count is fixed.

**Alternate Flow — Bad Instruction Format:**
1. If a line is not a valid BasicML instruction, the app reports the problem.
2. The app stops instead of continuing with bad code.

**Postconditions:** The app runs the version of the program currently shown in the editor.


---

### Use Case: Run Program and View WRITE Output

**Actor:** User

**Preconditions:** The GUI app is open and the code editor contains a BasicML program.

**Main Flow:**
1. The user clicks "Run Code".
2. The app loads the code from the editor.
3. The app runs the program.
4. When the program reaches a WRITE instruction, the app displays the output in the Program Output box.
5. The Program Output box scrolls as more output is added.

**Alternate Flow — Runtime Error:**
1. If the program hits a runtime error, the app reports the error.
2. The app stops running the program.

**Postconditions:** The user can see the program output in the GUI instead of needing to check the terminal.


---

### Use Case: READ Input

**Actor:** User

**Preconditions:** The GUI app is running a BasicML program that reaches a READ instruction.

**Main Flow:**
1. The program reaches a READ instruction.
2. The app asks the user to enter a 4-digit number.
3. The user enters a number such as `1234`, `0042`, `+1234`, or `-0042`.
4. The app validates the input.
5. The app stores the number in the correct memory location.

**Alternate Flow — Invalid Input:**
1. If the user enters an invalid value, the app shows an error.
2. The user must enter a valid 4-digit number before the program continues.

**Postconditions:** The user's input is stored in memory and the program continues running.


## 3. Requirement Numbering Notes

In the previous version, math and branching were grouped together too much. They are now split into two separate requirements:

- FR-5 covers arithmetic instructions.
- FR-6 covers branching instructions.

This makes the requirements easier to test and easier to connect back to the code.

The READ requirement was also updated because the app now accepts unsigned 4-digit input like `1234`, not only signed input like `+1234`.

The new GUI requirements also cover the color theme, file dialog loading, saving files, and editing code directly inside the app.