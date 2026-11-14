# Changes

- Restored algorithms/ and tests/ package structure from flattened uploads.
- Added main.py, retaining original/min.py.
- Fixed Prim: skip already visited vertices when removing heap entries; stale candidates previously added extra edges.
- Removed an unused timer read/import from utils.py. No timing feature is claimed.
- Added documentation and correctness checks.
- Preserved all uploaded Python source unchanged in original/. Excluded bytecode caches.
