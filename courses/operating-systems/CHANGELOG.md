# Code review and corrections

## Findings in the three uploaded files

- FCFS ran in input order and assumed arrival-sorted data.
- Round Robin added switch overhead after every slice, including the final completion and single-process continuation.
- SRTF in Untitled-1.py ran for a full quantum before reconsidering arrivals; test.py reconsidered per tick but still charged overhead on every tick.
- Several policies charged overhead even when the next event was an idle gap.
- MLFQ moved jobs based on remaining burst rather than consumed queue budget, left its bottom queue effectively unreachable, and did not properly preempt lower queues on new arrivals.
- Invalid bursts/quantum could cause nontermination or invalid metrics; inputs were not checked.
- Importing each original file ran a demo and opened a Matplotlib plot.
- Scheduling functions printed/visualized results but did not return structured data.

## Updated implementation

- Consolidated six schedulers into a tested, integer-time engine with explicit tie rules and dispatch-overhead semantics.
- Added true tick-level SRTF and a documented three-level RR(q)/RR(2q)/FCFS MLFQ variant. The latter is an intentional replacement of the ambiguous hybrid policy.
- Added input validation, idle timeline segments, response times and immutable results in original input order.
- Kept original wrapper names and RR argument order. Made printing/plotting opt-in and Matplotlib optional.
- Added a CLI and 13 automated tests, including randomized conservation checks and an independent SRTF reference.
- Retained all three source uploads unchanged under original/.
