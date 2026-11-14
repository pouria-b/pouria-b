import itertools
import unittest
from automaton import Automaton, accepts, transition, STATES, ACCEPTING_STATES


class AutomatonTests(unittest.TestCase):
    def test_examples(self):
        for text in ('100','101','110','111','0100','11100'):
            self.assertTrue(accepts(text),text)
        for text in ('','0','1','11','000','001','010','011','1000'):
            self.assertFalse(accepts(text),text)

    def test_all_short_strings_against_language_rule(self):
        for length in range(13):
            for bits in itertools.product('01',repeat=length):
                text=''.join(bits)
                self.assertEqual(accepts(text),len(text)>=3 and text[-3]=='1',text)

    def test_all_transitions(self):
        self.assertEqual(len(STATES),8)
        self.assertEqual(ACCEPTING_STATES,{'100','101','110','111'})
        for state in STATES:
            for bit in '01':
                self.assertEqual(transition(state,bit),state[1:]+bit)

    def test_incremental_history_and_state(self):
        m=Automaton()
        for bit in '1001101':
            returned=m.feed(bit)
            self.assertEqual(returned,m.state)
            self.assertEqual(m.accepted,accepts(m.text))
        self.assertEqual(m.state,'101')

    def test_reset_and_undo(self):
        m=Automaton('100');self.assertTrue(m.accepted)
        m.backspace();self.assertEqual(m.text,'10');self.assertFalse(m.accepted)
        m.reset();self.assertEqual(m.state,'000');self.assertFalse(m.accepted)
        m.backspace();self.assertEqual(m.text,'')

    def test_invalid_input_is_atomic(self):
        m=Automaton('100')
        for value in ('10x','2',' ',None,1):
            with self.assertRaises(ValueError):m.feed(value)
            self.assertEqual(m.text,'100')
        with self.assertRaises(ValueError):transition('000','01')
        with self.assertRaises(ValueError):transition('invalid','1')

    def test_import_does_not_require_pygame(self):
        import Automata
        self.assertTrue(callable(Automata.main))


if __name__=='__main__':
    unittest.main()
