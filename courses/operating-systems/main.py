"""Run a reproducible scheduling example; plotting is opt-in."""
import argparse
from scheduling import simulate, print_schedule, draw_gantt_chart


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', choices=['fcfs','rr','spn','srtf','hrrn','mlfq'], default='rr')
    parser.add_argument('--quantum', type=int, default=5)
    parser.add_argument('--context-switch', type=int, default=2)
    parser.add_argument('--plot', action='store_true')
    parser.add_argument('--output', help='Save a Gantt chart instead of opening a window')
    args = parser.parse_args()
    result = simulate(['P1','P2','P3','P4'], [1,7,9,25], [6,10,2,3],
                      args.policy, quantum=args.quantum, context_switch=args.context_switch)
    print_schedule(result)
    print('Timeline:', result.gantt_chart)
    if args.plot or args.output:
        draw_gantt_chart(result, title=args.policy.upper(), output=args.output)


if __name__ == '__main__':
    main()
