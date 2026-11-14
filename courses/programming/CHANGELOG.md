# Review and changes

## Hill Cipher

- Added explicit ASCII letter conversion, key/message lengths and modulo-26 invertibility validation.
- Removed unchecked key/message indexing and the premature return inside the interactive loop.
- Added EOF handling, multiple-block encryption and noninteractive CLI arguments.
- Preserved the uploaded source; the prebuilt Windows .exe is not executed or distributed here.

## Sudoku

- Consolidated duplicate project versions into a reviewed standalone program.
- Replaced limited-depth methods with MRV backtracking and explicit success/failure results.
- Validated file opening, all 81 digit tokens, value ranges, duplicate clues and trailing input.
- Removed uninitialized result paths, unsafe value indexing and Windows-only pause calls.
- Kept the AG/April 2007 provenance in original source and documented that attribution is unresolved.

## Packaging

- Added sample input, C++17 build instructions, optional CMake config, and nine passing compiled regression tests.
- All three original C++ files retained byte-for-byte under original/.
