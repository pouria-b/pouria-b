import numpy as np
from .utils import Problem

PI = np.pi
E = np.e

# --------- Unimodal ---------

def sphere(x): return float(np.sum(x**2))

def schwefel_222(x): return float(np.sum(np.abs(x)) + np.prod(np.abs(x)))

def schwefel_12(x):
    s = 0.0; c = 0.0
    for xi in x:
        c += xi
        s += c*c
    return float(s)

def sumsquares(x):
    i = np.arange(1, x.size+1)
    return float(np.sum(i*(x**2)))

def zakharov(x):
    i = np.arange(1, x.size+1)
    s1 = np.sum(x**2)
    s2 = np.sum(0.5*i*x)
    return float(s1 + s2**2 + s2**4)

def rosenbrock(x):
    return float(np.sum(100.0*(x[1:] - x[:-1]**2)**2 + (x[:-1] - 1.0)**2))

def dixon_price(x):
    n = x.size
    s = (x[0]-1)**2
    for i in range(1, n):
        s += (i+1) * (2*x[i]**2 - x[i-1])**2
    return float(s)

def ellipsoid(x):
    i = np.arange(0, x.size)
    return float(np.sum((10**6)**(i/(x.size-1 + 1e-12)) * x**2))

def step(x): return float(np.sum((np.floor(x + 0.5))**2))

def quartic_noise(x):
    rng = np.random.default_rng(12345)  # deterministic noise seed per call-set
    return float(np.sum(np.arange(1, x.size+1) * (x**4)) + rng.random())

def quintic(x):
    return float(np.sum(np.abs(x**5 - 3*x**4 + 4*x**3 + 2*x**2 - 10*x - 4)))

def matyas_2d(x):
    a, b = x[0], x[1]; return float(0.26*(a*a + b*b) - 0.48*a*b)

def booth_2d(x):
    a, b = x[0], x[1]; return float((a + 2*b - 7)**2 + (2*a + b - 5)**2)

def three_hump_camel_2d(x):
    a, b = x[0], x[1]
    return float(2*a*a - 1.05*a**4 + a**6/6 + a*b + b*b)

# --------- Multimodal ---------

def rastrigin(x):
    n = x.size
    return float(10*n + np.sum(x**2 - 10*np.cos(2*PI*x)))

def ackley(x):
    n = x.size
    s1 = np.sum(x**2)
    s2 = np.sum(np.cos(2*PI*x))
    return float(-20*np.exp(-0.2*np.sqrt(s1/n)) - np.exp(s2/n) + 20 + E)

def griewank(x):
    i = np.arange(1, x.size+1)
    return float(np.sum(x**2)/4000.0 - np.prod(np.cos(x/np.sqrt(i))) + 1.0)

def schwefel_226(x):
    return float(418.9829*x.size - np.sum(x*np.sin(np.sqrt(np.abs(x)))))

def salomon(x):
    r = np.sqrt(np.sum(x**2))
    return float(1 - np.cos(2*PI*r) + 0.1*r)

def alpine_n1(x): return float(np.sum(np.abs(x*np.sin(x) + 0.1*x)))

def levy(x):
    w = 1 + (x - 1)/4
    term1 = np.sin(np.pi*w[0])**2
    s = 0.0
    for wi in w[:-1]:
        s += (wi-1)**2 * (1 + 10*np.sin(np.pi*wi+1)**2)
    term3 = (w[-1]-1)**2 * (1 + np.sin(2*np.pi*w[-1])**2)
    return float(term1 + s + term3)

def beale_2d(x):
    a, b = x[0], x[1]
    return float((1.5 - a + a*b)**2 + (2.25 - a + a*b**2)**2 + (2.625 - a + a*b**3)**2)

def six_hump_camel_2d(x):
    a, b = x[0], x[1]
    return float((4-2.1*a*a + a**4/3)*a*a + a*b + (-4+4*b*b)*b*b)

def schaffer_n4_2d(x):
    a, b = x[0], x[1]
    num = np.cos(np.sin(np.abs(a*a - b*b)))**2 - 0.5
    den = (1 + 0.001*(a*a + b*b))**2
    return float(0.5 + num/den)

def branin_rcos_2d(x):
    a = 1.0
    b = 5.1/(4*np.pi**2)
    c = 5/np.pi
    r = 6
    s = 10
    t = 1/(8*np.pi)
    x1, x2 = x[0], x[1]
    return float(a*(x2 - b*x1**2 + c*x1 - r)**2 + s*(1 - t)*np.cos(x1) + s)

# Hartmann 3/6D
A3 = np.array([[3.0, 10, 30], [0.1, 10, 35], [3.0, 10, 30], [0.1, 10, 35]])
P3 = 1e-4*np.array([[3689, 1170, 2673], [4699, 4387, 7470], [1091, 8732, 5547], [381, 5743, 8828]])
alpha3 = np.array([1.0, 1.2, 3.0, 3.2])

def hartmann3(x):
    x = np.clip(x, 0, 1)
    s = 0.0
    for i in range(4):
        s += alpha3[i]*np.exp(-np.sum(A3[i]*(x - P3[i])**2))
    return float(-s)

A6 = np.array([[10, 3, 17, 3.5, 1.7, 8],
               [0.05, 10, 17, 0.1, 8, 14],
               [3, 3.5, 1.7, 10, 17, 8],
               [17, 8, 0.05, 10, 0.1, 14]])
P6 = 1e-4*np.array([[1312, 1696, 5569, 124, 8283, 5886],
                   [2329, 4135, 8307, 3736, 1004, 9991],
                   [2348, 1451, 3522, 2883, 3047, 6650],
                   [4047, 8828, 8732, 5743, 1091, 381]])
alpha6 = np.array([1.0, 1.2, 3.0, 3.2])

def hartmann6(x):
    x = np.clip(x, 0, 1)
    s = 0.0
    for i in range(4):
        s += alpha6[i]*np.exp(-np.sum(A6[i]*(x - P6[i])**2))
    return float(-s)

UNIMODAL = [
    Problem("Sphere", sphere, -100.0, 100.0, None, "unimodal"),
    Problem("Schwefel 2.22", schwefel_222, -100.0, 100.0, None, "unimodal"),
    Problem("Schwefel 1.2", schwefel_12, -100.0, 100.0, None, "unimodal"),
    Problem("SumSquares", sumsquares, -10.0, 10.0, None, "unimodal"),
    Problem("Zakharov", zakharov, -5.0, 10.0, None, "unimodal"),
    Problem("Rosenbrock", rosenbrock, -30.0, 30.0, None, "unimodal"),
    Problem("Dixon-Price", dixon_price, -10.0, 10.0, None, "unimodal"),
    Problem("Ellipsoid", ellipsoid, -100.0, 100.0, None, "unimodal"),
    Problem("Step", step, -100.0, 100.0, None, "unimodal"),
    Problem("Quartic+Noise", quartic_noise, -1.28, 1.28, None, "unimodal"),
    Problem("Quintic", quintic, -10.0, 10.0, None, "unimodal"),
    Problem("Matyas (2D)", matyas_2d, -10.0, 10.0, 2, "unimodal"),
    Problem("Booth (2D)", booth_2d, -10.0, 10.0, 2, "unimodal"),
    Problem("Three-Hump Camel (2D)", three_hump_camel_2d, -5.0, 5.0, 2, "unimodal"),
]

MULTIMODAL = [
    Problem("Rastrigin", rastrigin, -5.12, 5.12, None, "multimodal"),
    Problem("Ackley", ackley, -32.0, 32.0, None, "multimodal"),
    Problem("Griewank", griewank, -100.0, 100.0, None, "multimodal"),
    Problem("Schwefel 2.26", schwefel_226, -500.0, 500.0, None, "multimodal"),
    Problem("Salomon", salomon, -100.0, 100.0, None, "multimodal"),
    Problem("Alpine N.1", alpine_n1, -10.0, 10.0, None, "multimodal"),
    Problem("Levy", levy, -10.0, 10.0, None, "multimodal"),
    Problem("Beale (2D)", beale_2d, -4.5, 4.5, 2, "multimodal"),
    Problem("Six-Hump Camel (2D)", six_hump_camel_2d, np.array([-3.0, -2.0]), np.array([3.0, 2.0]), 2, "multimodal"),
    Problem("Schaffer N.4 (2D)", schaffer_n4_2d, -100.0, 100.0, 2, "multimodal"),
    Problem("Branin RCOS (2D)", branin_rcos_2d, np.array([-5.0, 0.0]), np.array([10.0, 15.0]), 2, "multimodal"),
    Problem("Hartmann 3D", hartmann3, 0.0, 1.0, 3, "multimodal"),
    Problem("Hartmann 6D", hartmann6, 0.0, 1.0, 6, "multimodal"),
]

BENCHMARKS = UNIMODAL + MULTIMODAL
