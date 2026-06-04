UVsim
Simple overview of use/purpose: A software simulator for executing machine language programs written in BasicML.

Description
UVSim is a basic virtual machine that is designed to help computer science students learn machine language and computer architecture. The simulator features a CPU, an accumulator, and a 100-word addressable memory array. It interprets BasicML, a basic machine language where all instructions and data are represented as signed four-digit decimal numbers ( +1007, -3008, -1045). This program can load BasicML programs from a text file, execute standard I/O and arithmetic operations, and handle memory management and control branching.

Getting Started
Dependencies
• Python 3.10 or newer. This is required since the program uses match statements in the code.
• Operating System: Windows, MacOS, Linux

Installing
• Download or clone the project repository containing the source code files.

Executing program
You can run this program from your computer’s terminal

Instructions:
• Open your terminal.
• Navigate to the folder that has the source code files.
• Run the program using either method:
	• Passing the file as an argument (python main.py Test1.txt)
	• Launching the program without a file argument (python main.py). The program will show the 	following: Console Output: Enter the filename: (Type your filename here, Ex: Test1.txt, and 	press Enter)

Once the program is running, it will automatically parse the file and begin executing instructions line by line.

Examples of what it can read and do:
• If the program encounters a READ (10) instruction, it will prompt you in the console to insert a number:. You must enter a valid signed integer (e.g., 1234).
• If the program encounters a WRITE (11) instruction, it will print the value stored in the specified memory address directly to your console.
• The execution finishes when the program reaches a HALT (43) command, printing "Program halted."

Authors
Jensen Caldwell
Andres Acosta Suarez
Cole Gillespie
Erick Roquel
