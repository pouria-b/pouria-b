"""Benchmark runner; requires the original missing PSO and GA modules."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from .problems import BENCHMARKS, UNIMODAL, MULTIMODAL, objective_for
from .utils import positive_int, stats, with_budget

POP, BUDGET, RUNS, N_IF_VAR = 50, 40000, 20, 30
HEADER = ['Function','PSO_Best','PSO_Mean','PSO_Std','GA_Best','GA_Mean','GA_Std']


def load_algorithms():
    try:
        from .algos.pso import run_pso
        from .algos.ga import run_ga
    except ModuleNotFoundError as exc:
        if exc.name and exc.name.startswith('ci_benchmarks.algos'):
            raise RuntimeError('Missing original algos/pso.py and algos/ga.py. Add them under ci_benchmarks/algos/ before running experiments. --check works without them.') from exc
        raise
    return {'PSO':run_pso, 'GA':run_ga}


def _done(path, allowed):
    if not path.exists():
        return set()
    with path.open(newline='',encoding='utf-8') as f:
        reader = csv.reader(f)
        if next(reader,None) != HEADER:
            raise ValueError(f'invalid CSV header: {path}')
        done = set()
        for row in reader:
            if len(row)!=7 or row[0] not in allowed or row[0] in done:
                raise ValueError(f'invalid or duplicate row in {path}')
            vals = np.asarray(row[1:], dtype=float)
            if not np.all(np.isfinite(vals)):
                raise ValueError(f'nonfinite statistics in {path}')
            done.add(row[0])
    return done


def run_all(out_dir='results', *, pop=POP, budget=BUDGET, runs=RUNS, dimension=N_IF_VAR, algorithms=None):
    for name,value in [('population',pop),('budget',budget),('runs',runs),('dimension',dimension)]:
        positive_int(value,name)
    if budget < pop:
        raise ValueError('budget must cover at least the initial population')
    for b in BENCHMARKS:
        b.bounds_of(b.dim_of(dimension))
    algorithms = load_algorithms() if algorithms is None else algorithms
    if set(algorithms) != {'PSO','GA'}:
        raise ValueError('algorithms must contain PSO and GA')
    out = Path(out_dir)
    config = {'format_version':2,'pop':pop,'budget':budget,'runs':runs,'dimension':dimension,
              'seed_rule':'optimizer=1000*r+algorithm_index; noise=1000000+r',
              'functions':[b.name for b in BENCHMARKS]}
    manifest = out/'config.json'
    if out.exists() and any(out.iterdir()):
        if not manifest.exists() or json.loads(manifest.read_text()) != config:
            raise ValueError('output directory has missing/different configuration; choose a fresh directory')
    # Check both groups before any writes so malformed old results do not resume.
    done = {kind:_done(out/f'perf_{kind}_stats.csv',{b.name for b in group})
            for kind,group in [('unimodal',UNIMODAL),('multimodal',MULTIMODAL)]}
    out.mkdir(parents=True,exist_ok=True)
    manifest.write_text(json.dumps(config,indent=2)+'\n')
    for kind, group in [('unimodal',UNIMODAL),('multimodal',MULTIMODAL)]:
        with (out/f'bench_{kind}_info.csv').open('w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f);writer.writerow(['Function','Range','Dim'])
            for b in group:
                dim=b.dim_of(dimension);lo,hi=b.bounds_of(dim)
                writer.writerow([b.name,json.dumps({'low':lo.tolist(),'high':hi.tolist()}),dim])
        target=out/f'perf_{kind}_stats.csv'
        if not target.exists():
            with target.open('w',newline='',encoding='utf-8') as f:csv.writer(f).writerow(HEADER)
        for b in group:
            if b.name in done[kind]:
                continue
            dim=b.dim_of(dimension);bounds=b.bounds_of(dim);row=[b.name]
            for ai,name in enumerate(('PSO','GA')):
                values=[]
                for r in range(runs):
                    objective,counter=with_budget(objective_for(b,dim,1000000+r),budget)
                    best,used=algorithms[name](objective,dim,tuple(a.copy() for a in bounds),pop=pop,budget=budget,seed=1000*r+ai)
                    best=float(best)
                    if not np.isfinite(best) or not counter['used'] or used != counter['used']:
                        raise ValueError(f'{name} must return a finite best value and accurate evaluation count')
                    values.append(best)
                row.extend(stats(values))
            with target.open('a',newline='',encoding='utf-8') as f:csv.writer(f).writerow(row)
            print(f'Completed {b.name}')


def check(dimension=30):
    for b in BENCHMARKS:
        dim=b.dim_of(dimension);lo,hi=b.bounds_of(dim)
        value=objective_for(b,dim,123)((lo+hi)/2)
        if not np.isfinite(value):
            raise ValueError(f'nonfinite midpoint objective: {b.name}')
    print(f'Validated {len(BENCHMARKS)} objectives; PSO/GA experiments not run.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--out',default='results')
    parser.add_argument('--pop',type=int,default=POP)
    parser.add_argument('--budget',type=int,default=BUDGET)
    parser.add_argument('--runs',type=int,default=RUNS)
    parser.add_argument('--dimension',type=int,default=N_IF_VAR)
    args=parser.parse_args()
    if args.check:
        check(args.dimension)
    else:
        try:run_all(args.out,pop=args.pop,budget=args.budget,runs=args.runs,dimension=args.dimension)
        except RuntimeError as exc:parser.exit(2,str(exc)+'\n')


if __name__=='__main__':
    main()
