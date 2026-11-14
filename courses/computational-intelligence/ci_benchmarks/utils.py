"""Validation, bounds and evaluation-budget helpers."""
from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Union
import numpy as np
Array = np.ndarray


def positive_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f'{name} must be a positive integer')
    return value


@dataclass
class Problem:
    name: str
    fn: Callable[[Array], float]
    low: Union[Array, float]
    high: Union[Array, float]
    fixed_dim: Optional[int]
    category: str
    min_dim: int = 1

    def dim_of(self, n_if_var):
        dim = self.fixed_dim if self.fixed_dim is not None else n_if_var
        positive_int(dim, 'dimension')
        if dim < self.min_dim:
            raise ValueError(f'{self.name} requires dimension >= {self.min_dim}')
        return dim

    def bounds_of(self, dim) -> Tuple[Array, Array]:
        positive_int(dim, 'dimension')
        if (self.fixed_dim is not None and dim != self.fixed_dim) or dim < self.min_dim:
            raise ValueError(f'invalid dimension for {self.name}')
        lo, hi = np.broadcast_to(np.asarray(self.low,dtype=float),(dim,)).copy(), np.broadcast_to(np.asarray(self.high,dtype=float),(dim,)).copy()
        if not np.all(np.isfinite(lo)) or not np.all(np.isfinite(hi)) or np.any(lo >= hi):
            raise ValueError('bounds must be finite and low < high')
        return lo, hi


def clamp(x, lo, hi):
    if np.any(np.asarray(lo) > np.asarray(hi)):
        raise ValueError('low must not exceed high')
    return np.clip(x, lo, hi)


def rng(seed):
    return np.random.default_rng(seed)


def with_budget(fn, budget):
    positive_int(budget, 'budget')
    used = {'used': 0}
    def wrapped(x):
        if used['used'] >= budget:
            raise RuntimeError('Budget exhausted')
        used['used'] += 1  # Failed objective calls still consume an evaluation.
        value = float(fn(x))
        if not np.isfinite(value):
            raise ValueError('objective returned a nonfinite value')
        return value
    return wrapped, used


def stats(values):
    values = np.asarray(values,dtype=float)
    if values.ndim != 1 or not values.size or not np.all(np.isfinite(values)):
        raise ValueError('values must be a nonempty finite vector')
    return float(values.min()), float(values.mean()), float(values.std(ddof=1)) if values.size > 1 else 0.0
