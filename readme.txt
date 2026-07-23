UVsim
Simple overview of use/purpose: A software simulator for executing machine language programs written in BasicML.

Description
UVSim is a basic virtual machine that is designed to help computer science students learn machine language and computer architecture. The simulator features a CPU, an accumulator, and a 100-word addressable memory array. It interprets BasicML, a basic machine language where all instructions and data are represented as four-digit integers.
This program features a Graphical User Interface (GUI), a modular Object-Oriented architecture, a built-in code editor, file loading and saving, configurable color themes, and a program output box. It allows users to load BasicML programs from a text file, view and edit the code before running it, execute standard I/O and arithmetic operations, view WRITE output, monitor the accumulator, and handle control branching.

Getting Started

Dependencies
• Python 3.10 or newer. This is required since the program uses match statements in the code.
• Tkinter: This is included in the Python library. No installation needed.
• Operating System: Windows, MacOS, Linux

Installing
• Download or clone the project repository containing the source code files.
• Make sure UVsimUI.py, main.py, classes.py, operations.py, and color_scheme.txt are in the same directory.

Executing program
You can choose to run the simulator using our Graphical User Interface (GUI) or the classic Command-Line Interface (CLI).

Option 1: Launching the GUI (Recommended)
This is the primary way to interact with UVSim. It features a code editor, a program output box, file buttons, color theme settings, and interactive buttons.
1. Open your terminal.
2. Navigate to the folder containing the source code files.
3. Run the command: python UVsimUI.py
4. The UVSim Graphical User Interface will appear on your screen.

How to Use the GUI:
• Loading the .txt File: Click the "Open File" button and choose a BasicML .txt file from any folder on your computer. The file contents will load into the code editor.
• Editing the Code: After loading a file, you can view and edit the BasicML code directly in the code editor before running it. You can add, delete, copy, paste, or manually change the code.
• Running the Code: Click the "Run Code" button to run the code currently shown in the editor.
• Line Limit: UVSim memory supports 100 entries, from 00 through 99. If the editor has more than 100 non-blank lines, the program will not run until the line count is fixed.
• Providing Input (Read): If the program encounters a READ command, a dialog box will pop up on your screen. You can type a valid 4-digit number with or without a sign. Examples: 1234, 0042, +1234, -0042.
• Viewing Output (Write): If the program encounters a WRITE command, the result will appear in the scrolling Program Output box in the GUI.
• Monitoring the Accumulator: As the program runs, you can view the live, updated value of the Accumulator in the GUI's CPU Status panel.
• Saving Code: Click the "Save As" button to save the current code editor contents to a .txt file. You can choose the file name and folder location.
• Changing Colors: Click the "Color Theme" button to change the app's primary color and off-color. The default colors are UVU green (#4C721D) and white (#FFFFFF). The selected colors are saved so they can be used again later.
• Resetting: Once completed, you can reset the simulator and run another BasicML program.

Option 2: Launching the CLI
If you prefer to run the simulator entirely inside your terminal without any external windows, you can use the CLI tool.
1. Open your terminal.
2. Navigate to the folder that has the source code files.
3. Run the program using either method:
  • Passing the file as an argument (python main.py test1.txt)
  • Launching the program without a file argument (python main.py). The program will show the following: Console Output: Enter the filename: (Type your filename here, ex: test1.txt, and press Enter)
Once the program is running, it will automatically parse the file and begin executing instructions line by line.

Running Tests
To run the unit tests, use:
python -m unittest test_main

Milestone 4 Manual Test Checklist
These GUI behaviors are not covered by the automated unit tests and should be checked by hand after any change to UVsimUI.py:
• Color Settings: Open "Color Theme", enter a valid hex pair, and click "Save" — the window, editor, and output box should recolor immediately. Enter an invalid hex value and confirm the app warns and falls back to the default colors instead of crashing. Click "Reset" and confirm the default UVU green/white scheme is restored. Restart the app and confirm the last saved theme is still applied.
• Saving/Loading: Click "Open File", choose a .txt BasicML program, and confirm it loads into the code editor. Edit the code, click "Save As", save to a new file, and confirm the saved file's contents match the editor. Cancel each dialog and confirm nothing changes.
• Editor Execution: Type or edit BasicML instructions directly in the code editor (without loading a file) and click "Run Code" — confirm the program runs the edited text, not a stale copy of any previously loaded file.
• 100-Line Limit: Paste more than 100 non-blank instruction lines into the code editor and click "Run Code" — confirm the app shows a validation error and does not execute the program.

Authors
Jensen Caldwell
Andres Acosta Suarez
Cole Gillespie
Erick Roquel