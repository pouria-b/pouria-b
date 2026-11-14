"""DFA for binary strings whose third symbol from the right is 1.

States store the last three symbols, in chronological order, left-padded
with zeros. This representation matches the labels in the supplied diagram.
"""
from dataclasses import dataclass
from itertools import product

STATES = tuple(''.join(bits) for bits in product('01', repeat=3))
INITIAL_STATE = '000'
ACCEPTING_STATES = frozenset(s for s in STATES if s[0] == '1')
TRANSITIONS = {state: {symbol: state[1:] + symbol for symbol in '01'} for state in STATES}


def transition(state, symbol):
    if not isinstance(state, str) or state not in TRANSITIONS:
        raise ValueError('state must be a three-bit string')
    if not isinstance(symbol, str) or symbol not in ('0', '1'):
        raise ValueError('symbol must be 0 or 1')
    return TRANSITIONS[state][symbol]


@dataclass
class Automaton:
    """Input history plus derived state; invalid input leaves history unchanged."""
    _text: str = ''

    def __post_init__(self):
        self._validate(self._text)

    @staticmethod
    def _validate(text):
        if not isinstance(text, str) or any(ch not in '01' for ch in text):
            raise ValueError('input must be a binary string')

    @property
    def text(self):
        return self._text

    @property
    def state(self):
        return self._text[-3:].rjust(3, '0')

    @property
    def accepted(self):
        return self.state in ACCEPTING_STATES

    def feed(self, text):
        self._validate(text)
        # Explicit transitions also check the table against the history convention.
        state = self.state
        for symbol in text:
            state = transition(state, symbol)
        self._text += text
        return state

    def reset(self):
        self._text = ''

    def backspace(self):
        self._text = self._text[:-1]


def accepts(text):
    """Recognize a complete string in O(n) time and O(1) auxiliary space."""
    Automaton._validate(text)
    state = INITIAL_STATE
    for symbol in text:
        state = transition(state, symbol)
    return state in ACCEPTING_STATES
