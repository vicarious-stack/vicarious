import os
import sys
import importlib
import inspect

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def verify():
    print("=" * 60)
    print("E2E TEST SUITE VERIFIER")
    print("=" * 60)
    
    modules = {
        "e2e_tests.tier1.test_tier1": 55,
        "e2e_tests.tier2.test_tier2": 55,
        "e2e_tests.tier3.test_tier3": 11,
        "e2e_tests.tier4.test_tier4": 6
    }
    
    success = True
    total_discovered = 0
    
    for mod_name, expected_count in modules.items():
        print(f"Loading {mod_name}... ", end="")
        try:
            mod = importlib.import_module(mod_name)
            funcs = [name for name, func in inspect.getmembers(mod, inspect.isfunction) if name.startswith("test_")]
            count = len(funcs)
            total_discovered += count
            if count == expected_count:
                print(f"OK (Discovered {count}/{expected_count} tests)")
            else:
                print(f"FAILED (Discovered {count} tests, expected {expected_count})")
                success = False
        except Exception as e:
            print(f"ERROR: {e}")
            success = False
            
    print("-" * 60)
    print(f"Total Discovered: {total_discovered}/127 tests")
    
    if total_discovered == 127 and success:
        print("VERIFICATION SUCCESS: All modules loaded and test counts match exactly!")
        return 0
    else:
        print("VERIFICATION FAILURE: Some modules failed to load or test counts are mismatching.")
        return 1

if __name__ == "__main__":
    sys.exit(verify())
