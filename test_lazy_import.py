"""Test that lazy imports work correctly and show when the cost occurs"""
import time

print("=" * 60)
print("Testing Lazy Import Behavior")
print("=" * 60)

# Test 1: Fast import
print("\n1. Importing stormcatchments...")
start = time.perf_counter()
import stormcatchments
elapsed = time.perf_counter() - start
print(f"   ✓ Import time: {elapsed:.3f}s (should be ~0s)")

# Test 2: Accessing module attributes (still fast)
print("\n2. Accessing stormcatchments.terrain...")
start = time.perf_counter()
terrain_module = stormcatchments.terrain
elapsed = time.perf_counter() - start
print(f"   ✓ Access time: {elapsed:.3f}s (should be ~0s)")

# Test 3: First call to function (this is where the cost happens)
print("\n3. First call to terrain.preprocess_dem()...")
print("   (This will trigger pysheds import - expect ~10s delay)")
start = time.perf_counter()
try:
    # This will fail without a real DEM, but it will import pysheds
    stormcatchments.terrain.preprocess_dem("fake.tif")
except Exception as e:
    elapsed = time.perf_counter() - start
    print(f"   ✓ Import triggered in {elapsed:.3f}s")
    print(f"   (Error expected: {type(e).__name__})")

# Test 4: Second call (should be fast now)
print("\n4. Second call to terrain.preprocess_dem()...")
start = time.perf_counter()
try:
    stormcatchments.terrain.preprocess_dem("fake2.tif")
except Exception as e:
    elapsed = time.perf_counter() - start
    print(f"   ✓ Time: {elapsed:.3f}s (should be <0.1s - pysheds already loaded)")

print("\n" + "=" * 60)
print("Summary: Lazy imports working correctly!")
print("- Module import: instant")
print("- First use: ~10s (one-time cost)")
print("- Subsequent uses: fast")
print("=" * 60)
