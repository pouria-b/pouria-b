# Operating Systems — CPU Scheduling Simulator

University coursework by **Pouria Babaei**, University of Guilan. A Python simulation of six CPU scheduling policies, with scheduling metrics and optional Gantt charts.

## Quick start

Python 3.9 or later recommended. The simulator and tests use only the standard library.

```bash
cd courses/operating-systems
python main.py --policy rr --quantum 5 --context-switch 2
python main.py --policy srtf --context-switch 0
python main.py --policy mlfq --quantum 2
python -m unittest discover -s . -p test_scheduling.py -v
```

For optional plotting:

```bash
python -m pip install -r requirements.txt
python main.py --policy mlfq --quantum 2 --output gantt.png
python main.py --policy fcfs --plot
```

`--output` saves an image without opening a window. In a headless environment, set `MPLBACKEND=Agg`. Imports never run a simulation or open a plot.

## Policies

| CLI policy | Algorithm | Dispatch rule |
| --- | --- | --- |
| `fcfs` | First Come, First Served | Earliest arrival; non-preemptive |
| `rr` | Round Robin | FIFO ready queue, bounded by a positive quantum |
| `spn` | Shortest Process Next / non-preemptive SJF | Shortest original burst among ready processes |
| `srtf` | Shortest Remaining Time First | Reevaluate after each integer tick; preempt for a strictly shorter remaining job |
| `hrrn` | Highest Response Ratio Next | Largest (waiting + burst) / burst; non-preemptive |
| `mlfq` | Multilevel Feedback Queue | Three priority queues: RR(q), RR(2q), then FCFS |

### MLFQ policy chosen for this corrected version

The uploaded version mixed RR, SRTF and FCFS but did not implement valid demotion between its queues. Because MLFQ has multiple variants, the corrected version uses an explicit, reproducible policy:

- All arrivals enter the highest-priority queue Q0.
- Q0 receives a total CPU budget of q; Q1 receives 2q. Unfinished processes move down when their budget is exhausted.
- Q2 runs FCFS without a time-slice limit.
- A newly ready higher-priority job preempts a lower-priority job at the next integer boundary. The interrupted job keeps its remaining budget and queue position.
- No priority boosts, aging or I/O blocking. Sustained high-priority arrivals can starve lower queues; the supplied finite workloads still complete.

## Time and context-switch convention

All arrival times, bursts, quantum values and switch durations are integers in abstract time units. Arrivals must be nonnegative, bursts and quantum strictly positive, and context-switch duration nonnegative. Zero-length bursts are rejected rather than silently dropped. Unsorted arrival arrays are supported. Process names must be unique, nonempty strings; `CS` and `IDLE` are reserved timeline labels.

A context switch is charged only when the CPU directly changes from one process to a different ready process. No overhead is charged for initial dispatch, returning from an idle interval, continuing the same process, or after the final completion. This convention deliberately omits dispatch-to-idle overhead.

Arrivals during overhead are admitted before the next dispatch; the destination is reevaluated, with no second charge for that dispatch. A switch already started is not refunded if the destination changes. Arrival and quantum-boundary events are handled before dispatch; new arrivals precede a just-expired RR process when it rejoins the queue.

Ties use arrival time then input order for FCFS, SPN and HRRN. SRTF keeps the current job on a remaining-time tie, then uses arrival time and input order. RR and MLFQ use queue order; simultaneous arrivals use input order.

## Python API

```python
from scheduling import simulate

result = simulate(['A', 'B'], [0, 1], [8, 1], 'srtf')
assert result.completion_time == (9, 2)
assert result.gantt_chart == ((0, 1, 'A'), (1, 2, 'B'), (2, 9, 'A'))
```

Results are immutable `ScheduleResult` objects. Metric tuples retain the original input order. Timeline entries are `(start, end, label)` and include explicit `IDLE` and `CS` segments. Adjacent entries for the same label are merged, so quantum or priority-level boundaries may be invisible when the same process continues.

- Completion time: time of the final executed CPU unit.
- Turnaround time: completion − arrival.
- Waiting time: turnaround − burst, including time spent waiting during switch overhead.
- Response time: first execution − arrival.

`fcfs_scheduling`, `round_robin_scheduling`, `spn_scheduling`, `srtf_scheduling`, `hrrn_scheduling`, and `mlfq` are available as wrappers. The original RR positional order `(processes, burst_time, arrival_time, quantum, context_switch)` is retained. Other wrappers take arrivals before bursts. For SRTF, the legacy `quantum` argument is accepted and validated but has no effect: true tick-level SRTF is not time-sliced RR.

The corrected functions **return results**; printing and plotting are explicit via `print_schedule(result)` and `draw_gantt_chart(result)`. This is an intentional change from the original print-and-plot-only behavior.

## Files

| File | Purpose |
| --- | --- |
| `scheduling.py` | Scheduling engine, result model, wrappers, printing and lazy plotting |
| `main.py` | Command-line runner using the supplied four-process example |
| `mlfq.py` | Compatibility import and executable MLFQ example |
| `test.py` | Executable SRTF example; the original was a demo, not an automated test |
| `test_scheduling.py` | Assertion-based regression tests |
| `requirements.txt` | Optional Matplotlib dependency |
| `original/` | All three uploaded files preserved byte-for-byte |
| `CHANGELOG.md` | Review findings and changes |

The original `Untitled-1.py` algorithms are consolidated into `scheduling.py`; original filenames and code remain under `original/`.

## Verification

13 automated tests cover unsorted arrivals, idle intervals, overhead, RR ordering, true SRTF preemption, arrivals during switches, SPN/HRRN decisions, MLFQ demotion and preemption, and invalid inputs. They also include 240 seeded workload invariant checks and 80 comparisons against a separate zero-overhead SRTF reference.

## Scope and limitations

This is a teaching simulator, not a real OS scheduler. It models one CPU, a single CPU burst per process, deterministic arrivals and integer time. No I/O, threads, multicore execution, priority boosts or real-time deadlines are modeled. Tick simulation scans processes repeatedly, so runtime scales with workload duration and process count; it is not intended for huge traces. Most dispatch selection is O(n) per tick; HRRN may sort ready jobs at dispatch, O(n log n). Timeline storage scales with the number of segments.

No instructor, semester or project grade is claimed. The portfolio can include future course projects alongside this one.
