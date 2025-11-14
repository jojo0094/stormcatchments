"""Profile import times to find bottlenecks"""
import time

def time_import(module_name):
    """Time how long it takes to import a module"""
    start = time.perf_counter()
    exec(f"import {module_name}")
    elapsed = time.perf_counter() - start
    print(f"{module_name:30s} : {elapsed:.3f}s")
    return elapsed

print("=" * 60)
print("Profiling import times")
print("=" * 60)

# Test individual dependencies
print("\n--- Individual Dependencies ---")
time_import("numpy")
time_import("pandas")
time_import("geopandas")
time_import("shapely")
time_import("networkx")
time_import("rasterio")
time_import("pysheds")

# Test stormcatchments submodules
print("\n--- Stormcatchments Submodules ---")
total_start = time.perf_counter()
time_import("stormcatchments.constants")
time_import("stormcatchments.network")
time_import("stormcatchments.terrain")
time_import("stormcatchments.delineate")
time_import("stormcatchments.topology")
total_elapsed = time.perf_counter() - total_start

print("\n--- Full Import ---")
full_start = time.perf_counter()
time_import("stormcatchments")
full_elapsed = time.perf_counter() - full_start

print("=" * 60)
print(f"Total stormcatchments submodules: {total_elapsed:.3f}s")
print(f"Full stormcatchments import:      {full_elapsed:.3f}s")
print("=" * 60)
