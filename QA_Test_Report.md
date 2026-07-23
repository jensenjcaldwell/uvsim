# QA Test Report

## Unit Tests

Unit tests were run with:

```bash
python -m unittest test_main
```

Result:

```text
32/32 tests passing
```

## End-to-End Test Results

The following BasicML test files were run through the simulator.

| File | READs | Result |
|---|---:|---|
| test1.txt | 2 | Passed — HALTED, accumulator = 35, output 35 |
| test2.txt | 2 | Passed — HALTED, accumulator = -105, output 100 |
| Test3.txt | 2 | Passed — HALTED, accumulator = -334, correct multi-line output |
| Test4.txt | 0 | Passed — HALTED, accumulator = -4444, correct multi-line output |
| test3_arithmetic_full.txt | 2 | Passed — HALTED, correct output |
| test4_branchzero.txt | 1 | Passed — HALTED, branch taken correctly |
| test5_branch.txt | 1 | Passed — HALTED, unconditional branch correct |
| test6_branchneg.txt | 2 | Passed — HALTED, negative branch correct |
| test7_divide_by_zero.txt | 1 | Passed — correctly raises runtime error, no crash |
| test8_invalid_opcode.txt | 0 | Passed — correctly raises runtime error for unknown opcode 99, no crash |

## READ Format Regression Test

The READ input fix was tested with the following values:

```text
+1234
-0042
1234
0042
```

All four values were accepted and stored/echoed correctly. This confirms unsigned input now works end-to-end, not just in the GUI validation.

## Static Checks

The following files parse cleanly with no syntax errors:

```text
UVsimUI.py
operations.py
```

## Known Issue

A small CLI-only issue was found in `operations.read()`: after repeated invalid input, the CLI retry loop may fall through to a blocking real `input()` call.

This issue is not reachable from the GUI because the popup validates the input before passing it to the simulator. It is being listed as a known issue and was not introduced by the recent GUI READ fix.

## Not Tested Live in Sandbox

The following GUI features were reviewed by reading the implementation, but were not clicked through live in the sandbox because there was no display available:

- Color theme
- Open file dialog
- Save file dialog
- Code editor use

These should be manually verified on a local machine before final submission.
