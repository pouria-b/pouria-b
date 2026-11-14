# Review and corrections

- Missing algos/pso.py and algos/ga.py prevented running the uploaded comparison; no replacements or performance data were fabricated.
- Restored package layout and module entry point; lazy optimizer imports allow catalog validation without missing files.
- Corrected Quartic+Noise's generator reset; added reproducible, independent per-run noise streams.
- Replaced removable assert-only bounds checks with explicit validation; added dimensions, finite bounds and ordering checks.
- Required Rosenbrock dimension >= 2; fixed the Ellipsoid denominator convention.
- Removed silent Hartmann clipping so objective evaluation does not disguise invalid optimizer bounds behavior.
- Moved Quintic and Three-Hump Camel to the multimodal group.
- Added configuration-aware resume, CSV validation, evaluation budget enforcement, accurate-count checks, and singleton statistics handling.
- Added eight tests and installation/run documentation. Original sources retained unchanged.
