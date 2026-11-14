from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Union
import numpy as np

Array = np.ndarray

@dataclass
class Problem:
    name: str
    fn: Callable[[Array], float]
    low: Union[Array, float]
    high: Union[Array, float]
    fixed_dim: Optional[int]      # None => n-dimensional
    category: str                 # "unimodal" or "multimodal"

    def dim_of(self, n_if_var: int) -> int:
        return self.fixed_dim if self.fixed_dim is not None else n_if_var

    def bounds_of(self, dim: int) -> Tuple[Array, Array]:
        lo, hi = self.low, self.high
        lo_arr = np.full(dim, lo, dtype=float) if np.isscalar(lo) else np.asarray(lo, dtype=float)
        hi_arr = np.full(dim, hi, dtype=float) if np.isscalar(hi) else np.asarray(hi, dtype=float)
        assert lo_arr.shape == (dim,) and hi_arr.shape == (dim,)
        return lo_arr, hi_arr


def clamp(x: Array, lo: Array, hi: Array) -> Array:
    return np.minimum(np.maximum(x, lo), hi)


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def with_budget(fn: Callable[[Array], float], budget: int):
    used = {"used": 0}
    def wrapped(x: Array) -> float:
        if used["used"] >= budget:
            raise RuntimeError("Budget exhausted")
        used["used"] += 1
        return float(fn(x))
    return wrapped, used


def stats(values: Array):
    values = np.asarray(values, dtype=float)
    return float(values.min()), float(values.mean()), float(values.std(ddof=1))
