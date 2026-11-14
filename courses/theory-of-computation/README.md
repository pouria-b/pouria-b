# Theory of Computation — Binary DFA Visualizer

University coursework by **Pouria Babaei**, University of Guilan. An interactive deterministic finite automaton for binary strings whose **third symbol from the right is 1**, using the supplied eight-state diagram.

## Language and states

Alphabet: {0, 1}. A string is accepted exactly when its length is at least three and `text[-3] == '1'`.

The state stores the last three input symbols in chronological order, padded on the left with zeros for short input. Initial state: `000`. Reading a symbol discards the old first bit and appends the new symbol: `state[1:] + symbol`. A state `(x,y,z)` on input `b` becomes `(y,z,b)`.

Accepting states are `100`, `101`, `110`, and `111`, matching the double circles in the supplied image. Padding cannot accidentally accept a string shorter than three symbols because its first stored bit is then zero.

| State | Input 0 | Input 1 | Accepting |
| --- | --- | --- | --- |
| 000 | 000 | 001 | No |
| 001 | 010 | 011 | No |
| 010 | 100 | 101 | No |
| 011 | 110 | 111 | No |
| 100 | 000 | 001 | Yes |
| 101 | 010 | 011 | Yes |
| 110 | 100 | 101 | Yes |
| 111 | 110 | 111 | Yes |

Examples: `100`, `101`, `110`, `111`, `0100` are accepted. Empty input, `1`, `11`, `001`, `011` and `1000` are rejected.

## Run

Python 3.9+ recommended. The recognizer, command-line checks and tests need only the standard library.

```bash
cd courses/theory-of-computation
python Automata.py --check 100
python Automata.py --check 1000
python -m unittest discover -s . -p test_automaton.py -v
```

The first check prints `ACCEPTED`; the second prints `REJECTED`. Both valid-input checks exit successfully; invalid symbols produce an error. Importing modules does not open a window.

For the visualizer, install Pygame:

```bash
python -m pip install -r requirements.txt
python Automata.py
```

The image path is resolved relative to the script, so launching from a different working directory is supported. A desktop display is required for the GUI.

### Controls

- `0` or `1`: append a binary symbol and update the highlighted state.
- `Backspace`: remove the most recent symbol.
- `R` or `Delete`: reset input and return to `000`.
- `Esc` or the window close button: quit cleanly.

The interface shows the current state and acceptance status. Long inputs show only the last 40 characters, with total input length; the full history remains stored for undo. Nonbinary text keys are ignored.

## Python API

```python
from automaton import Automaton, accepts

assert accepts('100') is True
assert accepts('1000') is False
machine = Automaton()
machine.feed('10')
machine.feed('1')
assert machine.state == '101'
assert machine.accepted
machine.backspace()
assert machine.text == '10'
assert not machine.accepted
machine.reset()
```

`transition(state, symbol)` exposes the transition function and rejects invalid states or symbols. `feed(text)` validates the complete chunk before changing history. `accepts(text)` recognizes a string in O(n) time with O(1) auxiliary state. The interactive model stores O(n) input history for undo; Python string appends copy history, so long interactive sessions are not a constant-memory stream processor.

## Review and changes

The original transition approach reverses bit order internally. That convention can encode the intended language, but mixing reversed lookup keys, string slices and image coordinates makes the implementation difficult to follow. The revised version uses one chronological state convention and an explicit transition table.

Added acceptance reporting, undo/reset, input validation, guarded entry points, relative asset loading and clean Pygame shutdown. The state ring is drawn after the diagram so it remains visible regardless of image transparency. The original Python file and PNG are preserved byte-for-byte under `original/`; the supplied image is reused unchanged.

## Verification and limits

Seven automated tests passed. Coverage includes all 16 transitions, all 8,191 binary strings of length 0 through 12 against the direct language rule, incremental updates, invalid input, reset and undo. Command-line accepted/rejected examples were also checked.

Pygame is not installed in the review environment, so interactive rendering and keyboard behavior have not been executed there. The GUI code is supplied and documented, but visual alignment is based on the supplied diagram's pixel coordinates and should be checked on a desktop with Pygame installed. These tests validate the recognizer; they do not substitute for an interactive GUI test.

No instructor, semester or project grade has been supplied.

## Files

- `automaton.py`: dependency-free state machine and recognizer.
- `Automata.py`: CLI and optional Pygame visualizer.
- `at.png`: supplied diagram, unchanged.
- `test_automaton.py`: correctness tests.
- `requirements.txt`: optional Pygame dependency.
- `original/`: untouched original source and image.
