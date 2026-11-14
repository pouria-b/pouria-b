"""Compatibility import for the corrected MLFQ scheduler; see README.md."""
from scheduling import mlfq, draw_gantt_chart, print_schedule

if __name__ == '__main__':
    print_schedule(mlfq(['P1','P2','P3','P4'], [1,7,9,25], [6,10,2,3], 5, 2))
