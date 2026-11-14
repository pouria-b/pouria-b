import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from ci_benchmarks.utils import Problem, stats, with_budget
from ci_benchmarks.problems import BENCHMARKS, sphere, booth_2d, rosenbrock, objective_for
from ci_benchmarks.runner import check, run_all


def stub(fn,dim,bounds,*,pop,budget,seed):
    """Test adapter only: midpoint evaluation, NOT a PSO or GA implementation."""
    return fn((bounds[0]+bounds[1])/2),1


class Tests(unittest.TestCase):
    def test_catalog(self):
        self.assertEqual(len(BENCHMARKS),27)
        self.assertEqual(len({b.name for b in BENCHMARKS}),27)
        check()
    def test_reference_values(self):
        self.assertEqual(sphere(np.zeros(3)),0)
        self.assertEqual(booth_2d(np.array([1.,3.])),0)
        self.assertEqual(rosenbrock(np.ones(4)),0)
    def test_noise_sequence(self):
        p=next(b for b in BENCHMARKS if b.name=='Quartic+Noise')
        a,b=objective_for(p,3,8),objective_for(p,3,8)
        va=[a(np.zeros(3)) for _ in range(5)]
        self.assertEqual(va,[b(np.zeros(3)) for _ in range(5)])
        self.assertGreater(len(set(va)),1)
        self.assertTrue(all(0<=x<1 for x in va))
    def test_dimensions(self):
        p=next(b for b in BENCHMARKS if b.name=='Rosenbrock')
        with self.assertRaises(ValueError):p.dim_of(1)
        p=next(b for b in BENCHMARKS if b.name=='Booth (2D)')
        with self.assertRaises(ValueError):p.bounds_of(3)
        with self.assertRaises(ValueError):objective_for(p,2,1)([1,2,3])
        with self.assertRaises(ValueError):Problem('bad',sphere,2,1,None,'test').bounds_of(2)
    def test_budget(self):
        fn,count=with_budget(sphere,2)
        fn(np.zeros(2));fn(np.zeros(2))
        with self.assertRaises(RuntimeError):fn(np.zeros(2))
        self.assertEqual(count['used'],2)
        with self.assertRaises(ValueError):with_budget(sphere,0)
    def test_stats(self):
        self.assertEqual(stats([2]),(2.,2.,0.))
        self.assertAlmostEqual(stats([1,3])[2],np.sqrt(2))
        for x in ([],[float('nan')]):
            with self.assertRaises(ValueError):stats(x)
    def test_runner_resume_and_config(self):
        small=BENCHMARKS[:1]
        with tempfile.TemporaryDirectory() as folder,patch('ci_benchmarks.runner.BENCHMARKS',small),patch('ci_benchmarks.runner.UNIMODAL',small),patch('ci_benchmarks.runner.MULTIMODAL',[]):
            args=dict(pop=2,budget=4,runs=1,dimension=2,algorithms={'PSO':stub,'GA':stub})
            run_all(folder,**args);run_all(folder,**args)
            with (Path(folder)/'perf_unimodal_stats.csv').open() as f:
                rows=list(csv.reader(f))
            self.assertEqual(len(rows),2)
            with self.assertRaises(ValueError):run_all(folder,**dict(args,runs=2))
            with (Path(folder)/'perf_unimodal_stats.csv').open('a') as f:f.write('broken\n')
            with self.assertRaises(ValueError):run_all(folder,**args)
    def test_count_contract(self):
        def bad(fn,dim,bounds,**kw):return fn(np.zeros(dim)),99
        with tempfile.TemporaryDirectory() as folder,patch('ci_benchmarks.runner.BENCHMARKS',BENCHMARKS[:1]),patch('ci_benchmarks.runner.UNIMODAL',BENCHMARKS[:1]),patch('ci_benchmarks.runner.MULTIMODAL',[]):
            with self.assertRaises(ValueError):run_all(folder,pop=2,budget=4,runs=1,dimension=2,algorithms={'PSO':bad,'GA':stub})


if __name__=='__main__':unittest.main()
