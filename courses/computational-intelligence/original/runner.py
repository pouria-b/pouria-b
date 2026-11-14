import os, csv, numpy as np
from .problems import UNIMODAL, MULTIMODAL
from .algos.pso import run_pso
from .algos.ga import run_ga
from .utils import Problem

# Assignment protocol
POP = 50
BUDGET = 40000
RUNS = 20
N_IF_VAR = 30

# Requested output filenames
INFO_UNI = "bench_unimodal_info.csv"
INFO_MULTI = "bench_multimodal_info.csv"
RES_UNI = "perf_unimodal_stats.csv"
RES_MULTI = "perf_multimodal_stats.csv"


def _write_info(path: str, benches: list[Problem]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Function", "Range", "Dim"])
        for b in benches:
            dim = b.dim_of(N_IF_VAR)
            lo, hi = b.bounds_of(dim)
            if np.allclose(lo, lo[0]) and np.allclose(hi, hi[0]):
                rng_str = f"[{lo[0]:g}, {hi[0]:g}]"
            else:
                rng_str = f"{list(lo)} to {list(hi)}"
            w.writerow([b.name, rng_str, dim])


def _ensure_header(path: str):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["Function","PSO_Best","PSO_Mean","PSO_Std","GA_Best","GA_Mean","GA_Std"])


def _load_done(path: str) -> set[str]:
    done = set()
    if not os.path.exists(path): return done
    with open(path, "r", encoding="utf-8") as f:
        rdr = csv.reader(f); next(rdr, None)
        for row in rdr:
            if row and row[0]: done.add(row[0])
    return done


def _run_group(outfile: str, benches: list[Problem]):
    _ensure_header(outfile)
    done = _load_done(outfile)
    total = len(benches)
    for i, b in enumerate(benches, 1):
        if b.name in done:
            print(f"[SKIP] {b.name} (already in {outfile})")
            continue
        dim = b.dim_of(N_IF_VAR)
        lo, hi = b.bounds_of(dim)
        print(f"[{i}/{total}] {b.name} | dim={dim} | runs={RUNS} | pop={POP} | budget={BUDGET}")

        # run PSO & GA
        stats = {}
        for algo_name, algo in {
            "PSO": lambda seed: run_pso(b.fn, dim, (lo, hi), pop=POP, budget=BUDGET, seed=seed),
            "GA":  lambda seed: run_ga(b.fn, dim, (lo, hi), pop=POP, budget=BUDGET, seed=seed),
        }.items():
            vals = []
            for r in range(RUNS):
                seed = 1000*r + (0 if algo_name=="PSO" else 1)
                best_val, used = algo(seed)
                vals.append(best_val)
            vals = np.array(vals, dtype=float)
            stats[algo_name] = (vals.min(), vals.mean(), vals.std(ddof=1))
            print(f"  {algo_name}: best={stats[algo_name][0]:.6g}  mean={stats[algo_name][1]:.6g}  std={stats[algo_name][2]:.6g}")

        with open(outfile, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                b.name,
                *[f"{x:.6g}" for x in stats["PSO"]],
                *[f"{x:.6g}" for x in stats["GA"]],
            ])
            f.flush()


def run_all(out_dir: str = "."):
    os.makedirs(out_dir, exist_ok=True)
    info_uni = os.path.join(out_dir, INFO_UNI)
    info_multi = os.path.join(out_dir, INFO_MULTI)
    res_uni = os.path.join(out_dir, RES_UNI)
    res_multi = os.path.join(out_dir, RES_MULTI)

    print("Writing info tables...")
    _write_info(info_uni, UNIMODAL)
    _write_info(info_multi, MULTIMODAL)

    print("Running unimodal benchmarks...")
    _run_group(res_uni, UNIMODAL)

    print("Running multimodal benchmarks...")
    _run_group(res_multi, MULTIMODAL)

    print("Done.")
    print(f"Generated:\n  {info_uni}\n  {info_multi}\n  {res_uni}\n  {res_multi}")
