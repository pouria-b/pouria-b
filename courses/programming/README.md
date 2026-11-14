# Programming Coursework — Hill Cipher and Sudoku

C++ coursework collected by **Pouria Babaei**, University of Guilan. Includes a reviewed Hill Cipher encryption program and Sudoku solver, original uploaded sources, sample input, and automated tests.

## Build

A C++17 compiler is required. No third-party C++ libraries are used.

```bash
cd courses/programming
g++ -std=c++17 -Wall -Wextra -Wpedantic hill_cipher.cpp -o hill_cipher
g++ -std=c++17 -Wall -Wextra -Wpedantic sudoku.cpp -o sudoku
```

Alternatively:

```bash
cmake -S . -B build
cmake --build build
```

On Windows, the executable filenames normally end in `.exe`; run those names from the build output directory. The uploaded prebuilt `hill cipher.exe` is not part of this source distribution and was not executed. Build executables from the reviewed source.

## Hill Cipher

A 3×3 key matrix encrypts blocks of three letters over integers modulo 26. Letters map as A=0 through Z=25; key letters fill rows from left to right. Each message block is a column vector, so encryption computes `c = K × p mod 26`.

```bash
./hill_cipher GYBNQKURP ACT
# POH
./hill_cipher gybnqkurp actact
# POHPOH
```

Run `./hill_cipher` without arguments for interactive input. Enter a nine-letter key once, then multiple messages; `!!!` quits. EOF also ends input cleanly.

### Input rules

- Key: exactly nine ASCII letters. Its determinant must be coprime with 26 so the matrix is invertible modulo 26.
- Message: a nonempty sequence of ASCII letters with length divisible by three. Multiple three-letter blocks are supported.
- Lowercase is converted to uppercase. Spaces, punctuation and digits are rejected, not silently removed.
- No automatic padding and no decryption are implemented. CLI errors return status 1; interactive invalid messages report an error and permit another attempt.

This is a classical cryptography teaching example, not encryption for protecting real secrets. Invertibility is validated even though this project exposes encryption only. For fixed 3×3 keys, encryption takes O(n) time and O(n) output storage for n input letters.

### Corrections to the upload

The original accessed the first nine key characters and first three message characters without checking length, used `% 65` instead of an explicit alphabet conversion, and returned from inside the message loop after the first encryption. The reviewed version checks input, validates invertibility, uses explicit A–Z mapping, handles EOF and supports repeated messages and multiple blocks.

## Sudoku

Solve a 9×9 puzzle from a file or standard input:

```bash
./sudoku examples/sudoku.dat
./sudoku < examples/sudoku.dat
```

Input must contain exactly **81 whitespace-separated single digits**, each between 0 and 9. `0` means an empty cell. Nine lines of nine digits are recommended; line boundaries are not significant. Dot notation, comments, compact 81-character strings and extra trailing data are not accepted.

The program validates the given clues, then uses recursive backtracking with a minimum-remaining-values choice: select an empty cell with the fewest legal candidates. Ties use row-major order and candidates are tried in ascending order. Rows, columns and 3×3 boxes must each contain digits 1 through 9 in the completed grid.

| Exit status | Meaning |
| --- | --- |
| 0 | A solution was printed |
| 1 | Invalid input, conflicting clues, missing file or invalid arguments |
| 2 | Clues are locally consistent but no solution exists |

Only the first solution is returned. Multiple-solution puzzles, including an empty board, may have many valid completions; uniqueness is not checked. No partial board is printed on failure. Backtracking has exponential worst-case search cost in the number of empty cells; MRV reduces practical branching but is not a polynomial-time guarantee. Maximum recursion depth is bounded by 81 cells.

### Corrections and provenance

The uploaded `sudoku.cpp` and `main.cpp` contain overlapping Sudoku implementations. They use unchecked reads from a fixed `sudoku.dat` path, permit unsafe indexing for out-of-range digits, have potentially uninitialized result variables, use limited-depth guessing, and call Windows-specific `system("pause")`. The leading comment in `sudoku.cpp` also swallows its include directives.

The runnable version is an explicitly documented replacement solver with checked input and complete backtracking, rather than a claim that the original three-method implementation was fully repaired without redesign. Both uploads are preserved unchanged under `original/`.

The uploaded `sudoku.cpp` carries an **AG / April 2007** header. That provenance is retained; the original third-party author's identity, original publication source and license have not been established. This collection does not claim that headered code was written entirely by Pouria. No new license is assigned on the author's behalf.

## Tests

Python 3.9+ and `g++` are required for the test runner:

```bash
python -m unittest discover -s . -p test_programs.py -v
```

Nine tests compile both reviewed programs with C++17 and `-Wall -Wextra -Wpedantic -Werror`. They cover:

- Hill Cipher known vector ACT → POH, identity key, lowercase normalization, multiple blocks and repeated interactive messages.
- Invalid lengths, characters, singular keys and EOF.
- Sudoku input from file and stdin, solved/empty boards, preservation of clues, and row/column/box validity.
- Missing files, malformed input, contradictory clues, and a locally consistent unsatisfiable puzzle.

Tests build in a temporary directory; generated binaries are not committed. Verification was performed with GCC 14.2 on Linux. Native Windows execution and a CMake build were not separately tested.

## Files

- `hill_cipher.cpp`: reviewed 3×3 encryption program.
- `sudoku.cpp`: reviewed backtracking solver.
- `examples/sudoku.dat`: runnable sample puzzle.
- `test_programs.py`: compilation and behavior tests.
- `CMakeLists.txt`: optional build configuration.
- `original/`: uploaded `hill cipher.cpp`, `sudoku.cpp` and `main.cpp`, unchanged.
- `CHANGELOG.md`: review summary.

## Python exercises

Two additional uploads are included under `python/`. They use the standard library only and need Python 3.9+.

```bash
python python/final_project.py
python python/email_regex.py email 'name+tag@example.com'
python python/email_regex.py phone '09123456789'
python -m unittest discover -s python -p test_python_programs.py -v
```

### final_project.py

A ten-option menu covers number comparison, a text histogram, factorial, Fibonacci, geometry, vowel counts, shared-bill allocation, Unicode code-point encoding/decoding, a string-search exercise, and SMS keypad press totals. Type `back` to return or `end` to exit. EOF and keyboard interruption terminate cleanly. Importing the module does not prompt for input.

Corrections include the unreachable `decode` branch, accidental lowercasing of encoded text, the duplicate keypad key 3 (wxyz now uses key 9), invalid keypad indexing, negative factorial/Fibonacci input and geometric dimensions, and the recursive Fibonacci implementation (now iterative). Code-point encoding is a reversible text representation, not encryption. SMS reports total key presses per digit for the supplied English-letter/punctuation mapping; it does not send messages or model pauses between repeated keys.

The upload's special exceptions for 10 < y < 20, factorial input 5 and Fibonacci count 8 are retained rather than silently assuming they were unwanted. The histogram still prints `4444` on its fourth row. The search exercise also retains its original behavior: it reports one-based positions of the letter `f`, using the entered text when its length is at least 10 and otherwise a fixed sample string. These unusual conditions may reflect assignment requirements; they are not general-purpose mathematical restrictions. Unsupported geometry/mode choices can still return without a calculation. Shared-bill allocation uses the original fixed household counts and floating-point amounts; it is a classroom arithmetic exercise.

### email_regex.py

`validate_email(text)` and `validate_phone(text)` return booleans without printing. The CLI prints the boolean result. Full-string matching rejects trailing newlines and unwanted suffixes. Email validation implements a documented ASCII subset: dotted local-part segments containing letters, digits, underscore, plus, percent and hyphen; DNS-style domain labels; and an alphabetic final label of 2–63 characters. It allows digits including zero, subdomains and variable-length suffixes. Local-part and total lengths are limited to 64 and 254 characters. Quoted local parts, many other permitted special characters and internationalized addresses are not supported. It is a practical classroom format check, not complete email-standard compliance or mailbox verification.

Mobile validation accepts ASCII digits in exactly these three shapes: `09` + nine digits, `+989` + nine digits, and `00989` + nine digits. Other types/lengths return False. Spaces, separators and Persian digits are not normalized. No claim is made about active operator prefixes, allocation or reachability.

Eight Python tests cover formats, return types, code-point round-trips, factorial/Fibonacci, keypad totals, geometry, retained exercise conditions and clean imports/EOF. Both original Python uploads are preserved unchanged under `python/original/`.

No course grade, instructor or semester has been supplied.
