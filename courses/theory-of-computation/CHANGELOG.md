# Review and changes

- Replaced intertwined reversed-string lookups with a pure transition table using chronological three-bit state labels.
- Added explicit accepting states and binary-input validation; no claim that the original reversal convention alone was a language-recognition bug.
- Separated logic from Pygame, removed import-time GUI execution, and added CLI checks.
- Resolved at.png relative to the script instead of the current working directory.
- Added reset, undo, visible acceptance status, bounded displayed input, a visible state ring, and clean shutdown.
- Added seven correctness tests, including exhaustive recognition for binary strings through length 12.
- Preserved original Automata.py and at.png unchanged.
- GUI execution remains unverified here because Pygame is unavailable.
