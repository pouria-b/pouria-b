"""Executable SRTF example replacing the original plot-on-import script.

Run test_scheduling.py with unittest for correctness tests.
"""
from scheduling import srtf_scheduling, print_schedule

if __name__ == '__main__':
    print_schedule(srtf_scheduling(['P1','P2','P3','P4'], [1,7,9,25], [6,10,2,3], context_switch=2))
