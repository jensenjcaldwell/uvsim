UVsim
Simple overview of use/purpose: A software simulator for executing machine language programs written in BasicML.

Description
UVSim is a basic virtual machine that is designed to help computer science students learn machine language and computer architecture. The simulator features a CPU, an accumulator, and a 100-word addressable memory array. It interprets BasicML, a basic machine language where all instructions and data are represented as signed four-digit integers ( +1007, -3008, -1045). 
This program features a newly implemented Graphical User Interface (GUI) and a modular Object-Oriented architecture. It allows users to easily load BasicML programs from a text file, execute standard I/O and arithmetic operations, visually monitor memory registers, and handle control branching.


Getting Started

Dependencies
• Python 3.10 or newer. This is required since the program uses match statements in the code.
• Tkinter: This is included in the Python library. No installation needed.
• Operating System: Windows, MacOS, Linux

Installing
• Download or clone the project repository containing the source code files.
• Make sure UVsimUI.py, main.py, classes.py, & operations.py are in the same directory.

Executing program
You can choose to run the simulator using our Graphical User Interface (GUI) or the classic Command-Line Interface (CLI).

Option 1: Launching the GUI (Recommended)
This is the primary way to interact with UVSim. It features a full visual memory grid, a built-in console, and interactive buttons.
1. Open your terminal.
2. Navigate to the folder containing the source code files.
3. Run the command: python UVsimUI.py
4. The UVSim Graphical User Interface will appear on your screen.

How to Use the GUI:
• Loading Existing Code: Click the "Open File" button and choose any BasicML .txt file to load it into the built-in editor.
• Using the New Code Editor: Write or edit BasicML instructions directly in the "BasicML Code Editor" text area. Enter one signed 4-digit instruction per line (example: +1007, +2008, +4300).
• Saving Code from the Editor: Click "Save As", choose a file name and location, then save as a .txt file. This exports exactly what is currently in the editor.
• Running the Code: After loading or writing code in the editor, click the "Run Code" button to begin execution.
• Providing Input (Read): If the program encounters a Read command, a dialog box will pop up on your screen. You must type a valid 4-digit integer (1234) into the box and click submit.
• Viewing Output (Write): If the program encounters a Write command, the result will be printed to the accumulator output display area on the interface as well as save the value on the accumulator to the targeted memory address.
• Resetting: Once completed, click "Reset" to clear simulator state before running another program.

Option 2: Launching the CLI
If you prefer to run the simulator entirely inside your terminal without any external windows, you can use the CLI tool.
1. Open your terminal.
2. Navigate to the folder that has the source code files.
3. Run the program using either method:
  • Passing the file as an argument (python main.py Test1.txt)
  • Launching the program without a file argument (python main.py). The program will show the following: Console Output: Enter the filename: (Type your filename here, ex: test1.txt, and press Enter)
Once the program is running, it will automatically parse the file and begin executing instructions line by line.

Authors
Jensen Caldwell
Andres Acosta Suarez
Cole Gillespie
Erick Roquel
