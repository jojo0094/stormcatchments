"""Detailed profiling of stormcatchments imports with import chain tracking"""
import sys
import time

class ImportProfiler:
    def __init__(self):
        self.import_times = {}
        self.import_stack = []
        
    def start_import(self, name):
        self.import_stack.append((name, time.perf_counter()))
        
    def end_import(self, name):
        if self.import_stack and self.import_stack[-1][0] == name:
            _, start_time = self.import_stack.pop()
            elapsed = time.perf_counter() - start_time
            indent = "  " * len(self.import_stack)
            print(f"{indent}{name:40s} : {elapsed:.3f}s")
            self.import_times[name] = elapsed

profiler = ImportProfiler()

# Hook into import system
original_import = __builtins__.__import__

def profiled_import(name, *args, **kwargs):
    if name.startswith('stormcatchments'):
        profiler.start_import(name)
    result = original_import(name, *args, **kwargs)
    if name.startswith('stormcatchments'):
        profiler.end_import(name)
    return result

__builtins__.__import__ = profiled_import

print("=" * 80)
print("Detailed Import Profiling - stormcatchments")
print("=" * 80)

start = time.perf_counter()
import stormcatchments
total = time.perf_counter() - start

print("=" * 80)
print(f"Total import time: {total:.3f}s")
print("=" * 80)

# Restore original import
__builtins__.__import__ = original_import
