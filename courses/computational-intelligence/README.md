# Computational Intelligence — Optimization Benchmarks

University coursework by **Pouria Babaei**, University of Guilan. A collection of **27 numerical minimization objectives** and a runner designed to compare Particle Swarm Optimization (PSO) with a Genetic Algorithm (GA).

**Status: benchmark utilities and runner reviewed; original PSO and GA implementations were not supplied. No optimization performance results are claimed.**

## Install and validate

Python 3.9+ recommended. NumPy is the only supplied dependency.

```bash
cd courses/computational-intelligence
python -m pip install -r requirements.txt
python -m ci_benchmarks.runner --check
python -m unittest discover -s . -p test_benchmarks.py -v
```

Use module execution from the course directory: running `runner.py` directly does not support its package-relative imports. The check command evaluates all 27 functions at valid midpoint inputs; it does not run PSO or GA or prove every formula is correct.

## Complete the original experiment

Add the missing original files:

```text
ci_benchmarks/algos/__init__.py
ci_benchmarks/algos/pso.py
ci_benchmarks/algos/ga.py
```

Each must expose `run_pso` or `run_ga`, respectively, with this contract:

```python
best_value, evaluations_used = run_pso(
    objective, dimension, (lower_bounds, upper_bounds),
    pop=50, budget=40000, seed=0,
)
```

The algorithm must minimize the objective, keep candidates within bounds, use its supplied seed, count objective calls accurately, respect the evaluation budget, and return a finite best value. The runner enforces the maximum objective-call count and checks the returned count. It cannot verify algorithm logic, boundary handling or the returned best value without the optimizer source. Both algorithms must use the wrapped objective; do not call benchmark functions behind the wrapper. If an optimizer already wraps the objective, its own call count still needs to match.

Then run:

```bash
python -m ci_benchmarks.runner --out results --pop 50 --budget 40000 --runs 20 --dimension 30
```

These defaults come from the supplied assignment runner. At the full evaluation budget the protocol allows up to 43,200,000 objective calls: 27 functions × 2 algorithms × 20 runs × 40,000. A smaller trial is advisable after the missing implementations are added; no full experiment was run during this review.

## Function catalog

| Group in this coursework | Functions |
| --- | --- |
| Unimodal/base grouping (12) | Sphere; Schwefel 2.22; Schwefel 1.2; SumSquares; Zakharov; Rosenbrock; Dixon–Price; Ellipsoid; Step; Quartic+Noise; Matyas (2D); Booth (2D) |
| Multimodal (15) | Quintic; Three-Hump Camel (2D); Rastrigin; Ackley; Griewank; Schwefel 2.26; Salomon; Alpine N.1; Levy; Beale (2D); Six-Hump Camel (2D); Schaffer N.4 (2D); Branin RCOS (2D); Hartmann 3D; Hartmann 6D |

Fixed-dimensional functions retain their 2D, 3D or 6D size. Others use `--dimension`, default 30. Rosenbrock requires at least two coordinates: the supplied sum-of-pairs expression degenerates to a constant in 1D. The generated info CSVs list the exact coordinate bounds used in this assignment. Bounds are assignment choices, not claims of universally standard ranges.

Quintic and Three-Hump Camel were moved out of the original unimodal list because of their multiple minima. Other group labels retain the assignment's organization and are not a mathematical claim about all dimensions. Quartic+Noise is stochastic; the grouping describes its quartic base. The named formulas are retained except for the changes documented below. This review does not independently certify all 27 against an external benchmark specification.

## Reproducibility and noise

`objective_for(problem, dimension, seed)` validates vector size and finite coordinates. Each noisy run owns a NumPy generator. Unlike the upload, which reset its generator on every call and added the same offset repeatedly, the corrected Quartic+Noise produces a sequence of fresh uniform noise samples.

Optimizer seeds follow the original rule `1000 * run_index + algorithm_index` (PSO=0, GA=1). Noise seeds are `1000000 + run_index`, sharing the same noise sequence across algorithms for the same run index. Results depend on evaluation order. Exact reproducibility also depends on optimizer implementation, NumPy version, platform and parameters. Direct calls to `quartic_noise(x)` are unseeded; use the objective factory for experiments.

Hartmann no longer silently clips inputs internally; boundary handling belongs to the optimizer. The factory checks dimension/finiteness but does not clamp arbitrary out-of-bounds vectors. The `clamp` helper is available. Ellipsoid uses an explicit 1D convention instead of adding an epsilon to every higher-dimensional denominator.

## Output and resume behavior

- `bench_unimodal_info.csv`, `bench_multimodal_info.csv`: function names, coordinate ranges, dimensions.
- `perf_unimodal_stats.csv`, `perf_multimodal_stats.csv`: best, mean and sample standard deviation for PSO/GA.
- `config.json`: experiment settings, seed rule, function list and result-format version.

Smaller objective values are better. Standard deviation uses `ddof=1`; with one run it is reported as zero by an explicit convention. Statistics are retained as full float values rather than six-significant-digit strings.

The runner resumes completed function rows only when the configuration matches. It rejects malformed headers, duplicate/unknown functions, incomplete rows and nonfinite values. Changed settings require a fresh output directory. Configuration does not fingerprint optimizer source or dependency versions: always use a new directory after changing them. Runs are sequential and results are written after both algorithms finish a function; interruption may require repeating that function. Concurrent writers are unsupported. Raw per-run values and convergence histories are not exported in this version.

## Files

- `ci_benchmarks/problems.py`: functions, catalog and seeded objective factory.
- `ci_benchmarks/utils.py`: problem metadata, bounds, clamping, budgets and statistics.
- `ci_benchmarks/runner.py`: CLI, experiment orchestration and CSV validation.
- `test_benchmarks.py`: eight automated tests; runner integration tests use clearly labeled test stubs, not replacement PSO/GA algorithms.
- `original/`: three uploads preserved unchanged.
- `CHANGELOG.md`: findings and corrections.

No instructor, semester, grade, algorithm implementation, or successful PSO/GA comparison is invented.
