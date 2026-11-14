"""Deterministic single-CPU scheduling with integer time units.

See README.md for dispatch overhead, tie-breaking and MLFQ policy.
Importing this module never plots or runs examples.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduleResult:
    """Metrics in input order; segments are (start, end, label)."""
    processes: tuple
    arrival_time: tuple
    burst_time: tuple
    completion_time: tuple
    turnaround_time: tuple
    waiting_time: tuple
    response_time: tuple
    gantt_chart: tuple


def _integer(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')


def simulate(processes, arrival_time, burst_time, policy='fcfs', *,
             quantum=2, context_switch=0):
    """Return an immutable result without changing caller-owned inputs.

    Supported policies: fcfs, rr, spn, srtf, hrrn, mlfq.
    Empty input is valid. Names must be unique nonempty strings, excluding
    reserved timeline labels CS and IDLE. Arrivals >= 0; bursts > 0.
    """
    names, arrivals, bursts = tuple(processes), tuple(arrival_time), tuple(burst_time)
    n = len(names)
    if not (n == len(arrivals) == len(bursts)):
        raise ValueError('processes, arrival_time and burst_time must have equal lengths')
    if any(not isinstance(x, str) or not x.strip() or x in ('CS', 'IDLE') for x in names):
        raise ValueError('process names must be nonempty strings other than CS and IDLE')
    if len(set(names)) != n:
        raise ValueError('process names must be unique')
    for value in arrivals:
        _integer(value, 'arrival time', 0)
    for value in bursts:
        _integer(value, 'burst time', 1)
    _integer(context_switch, 'context_switch', 0)
    _integer(quantum, 'quantum', 1)
    policy = policy.lower()
    if policy not in ('fcfs', 'rr', 'spn', 'srtf', 'hrrn', 'mlfq'):
        raise ValueError('unknown policy')
    remaining = list(bursts)
    completion, first = [None] * n, [None] * n
    level, budget = [0] * n, [quantum] * n
    order = [None] * n
    pending = sorted(range(n), key=lambda i: (arrivals[i], i))
    next_arrival = serial = done = time = 0
    active = last = None
    segments = []

    def append(start, end, label):
        if end <= start:
            return
        if segments and segments[-1][1] == start and segments[-1][2] == label:
            segments[-1] = (segments[-1][0], end, label)
        else:
            segments.append((start, end, label))

    def admit():
        nonlocal next_arrival, serial
        while next_arrival < n and arrivals[pending[next_arrival]] <= time:
            i = pending[next_arrival]
            order[i] = serial
            serial += 1
            next_arrival += 1

    def choose(ready):
        if policy in ('fcfs', 'spn', 'hrrn') and active in ready:
            return active
        if policy == 'fcfs':
            return min(ready, key=lambda i: (arrivals[i], i))
        if policy == 'spn':
            return min(ready, key=lambda i: (bursts[i], arrivals[i], i))
        if policy == 'hrrn':
            # Integer cross-products avoid rounding in response-ratio comparison.
            best = min(ready, key=lambda i: (arrivals[i], i))
            for i in sorted(ready, key=lambda i: (arrivals[i], i)):
                if ((time - arrivals[i] + bursts[i]) * bursts[best] >
                        (time - arrivals[best] + bursts[best]) * bursts[i]):
                    best = i
            return best
        if policy == 'srtf':
            shortest = min(remaining[i] for i in ready)
            if active in ready and remaining[active] == shortest:
                return active
            return min(ready, key=lambda i: (remaining[i], arrivals[i], i))
        if policy == 'rr':
            return min(ready, key=lambda i: order[i])
        return min(ready, key=lambda i: (level[i], order[i]))

    while done < n:
        admit()
        ready = [i for i in range(n) if order[i] is not None and remaining[i] > 0]
        if not ready:
            future = arrivals[pending[next_arrival]]
            append(time, future, 'IDLE')
            time = future
            active = last = None
            continue
        i = choose(ready)
        if last is not None and i != last and context_switch:
            # Charge once; jobs arriving during the overhead join before dispatch.
            append(time, time + context_switch, 'CS')
            time += context_switch
            admit()
            ready = [j for j in range(n) if order[j] is not None and remaining[j] > 0]
            i = choose(ready)
        active = i
        if first[i] is None:
            first[i] = time
        append(time, time + 1, names[i])
        time += 1
        remaining[i] -= 1
        last = i
        if policy == 'rr' or (policy == 'mlfq' and level[i] < 2):
            budget[i] -= 1
        # Boundary arrivals precede a job whose quantum just expired.
        admit()
        if remaining[i] == 0:
            completion[i] = time
            done += 1
            active = None
        elif policy in ('rr', 'mlfq') and budget[i] == 0:
            if policy == 'mlfq':
                level[i] = min(2, level[i] + 1)
            budget[i] = quantum if policy == 'rr' else 2 * quantum
            order[i] = serial
            serial += 1
            active = None
    turnaround = tuple(completion[i] - arrivals[i] for i in range(n))
    waiting = tuple(turnaround[i] - bursts[i] for i in range(n))
    response = tuple(first[i] - arrivals[i] for i in range(n))
    return ScheduleResult(names, arrivals, bursts, tuple(completion), turnaround,
                          waiting, response, tuple(segments))


def fcfs_scheduling(processes, arrival_time, burst_time, context_switch=0):
    return simulate(processes, arrival_time, burst_time, 'fcfs', context_switch=context_switch)


def round_robin_scheduling(processes, burst_time, arrival_time, quantum, context_switch=0):
    """Retain the original RR argument order: bursts before arrivals."""
    return simulate(processes, arrival_time, burst_time, 'rr', quantum=quantum, context_switch=context_switch)


def spn_scheduling(processes, arrival_time, burst_time, context_switch=0):
    return simulate(processes, arrival_time, burst_time, 'spn', context_switch=context_switch)


def srtf_scheduling(processes, arrival_time, burst_time, quantum=None, context_switch=0):
    """Legacy quantum argument is validated but does not delay SRTF preemption."""
    if quantum is not None:
        _integer(quantum, 'quantum', 1)
    return simulate(processes, arrival_time, burst_time, 'srtf', context_switch=context_switch)


def hrrn_scheduling(processes, arrival_time, burst_time, context_switch=0):
    return simulate(processes, arrival_time, burst_time, 'hrrn', context_switch=context_switch)


def mlfq(processes, arrival_time, burst_time, quantum=2, context_switch=0):
    return simulate(processes, arrival_time, burst_time, 'mlfq', quantum=quantum, context_switch=context_switch)


def print_schedule(result):
    print('Process | Arrival | Burst | Completion | Turnaround | Waiting | Response')
    for row in zip(result.processes, result.arrival_time, result.burst_time,
                   result.completion_time, result.turnaround_time,
                   result.waiting_time, result.response_time):
        print(' | '.join(str(x) for x in row))


def draw_gantt_chart(result, *, title='CPU scheduling', output=None):
    """Plot a result; Matplotlib is needed only when this function is called."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(12, 3))
    colors = {name: plt.get_cmap('tab20')(i % 20) for i, name in enumerate(result.processes)}
    colors.update(CS='#e79c91', IDLE='#dedede')
    for start, end, name in result.gantt_chart:
        ax.barh(0, end-start, left=start, color=colors[name], edgecolor='black')
        ax.text((start+end)/2, 0, name, ha='center', va='center', fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel('Time units')
    ax.set_title(title)
    ax.set_xlim(0, result.gantt_chart[-1][1] if result.gantt_chart else 1)
    fig.tight_layout()
    if output:
        fig.savefig(output, dpi=160)
    else:
        plt.show()
    plt.close(fig)
