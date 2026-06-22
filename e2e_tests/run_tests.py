import os
import sys
import time
import json
import importlib
import inspect
import unittest

# Ensure the project root is in the path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    print("=" * 60)
    print("VICARIOUS E2E TEST RUNNER (GEN 2)")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Python: {sys.version}")
    print("-" * 60)

    modules_to_load = [
        "e2e_tests.tier1.test_tier1",
        "e2e_tests.tier2.test_tier2",
        "e2e_tests.tier3.test_tier3",
        "e2e_tests.tier4.test_tier4"
    ]

    all_tests = []
    for mod_name in modules_to_load:
        try:
            mod = importlib.import_module(mod_name)
            # Retrieve functions starting with test_
            funcs = []
            for name, func in inspect.getmembers(mod, inspect.isfunction):
                if name.startswith("test_"):
                    funcs.append((name, func))
            # Sort alphabetically within the module to ensure deterministic order
            funcs.sort(key=lambda x: x[0])
            for name, func in funcs:
                all_tests.append((mod_name, name, func))
        except Exception as e:
            print(f"ERROR: Failed to load test module {mod_name}: {e}")
            sys.exit(1)

    total_tests = len(all_tests)
    print(f"Discovered {total_tests} test cases.")
    print("-" * 60)

    passed = 0
    failed = 0
    skipped = 0
    errors = 0

    results_details = []
    start_time_all = time.time()

    for idx, (mod_name, test_name, func) in enumerate(all_tests, 1):
        tier = mod_name.split(".")[-2]
        test_fullname = f"{mod_name}.{test_name}"
        
        # Display progress indicator
        print(f"[{idx}/{total_tests}] Running {test_fullname}... ", end="")
        sys.stdout.flush()

        status = "passed"
        message = ""
        start_time_test = time.time()
        
        try:
            func()
            passed += 1
            print("PASS")
        except unittest.SkipTest as e:
            status = "skipped"
            message = str(e)
            skipped += 1
            print(f"SKIP ({message})")
        except AssertionError as e:
            status = "failed"
            message = str(e)
            failed += 1
            print(f"FAIL: {message}")
        except Exception as e:
            status = "error"
            message = f"Unexpected error: {type(e).__name__}: {str(e)}"
            errors += 1
            print(f"ERROR: {message}")
        
        elapsed_test = time.time() - start_time_test
        results_details.append({
            "test_name": test_name,
            "full_name": test_fullname,
            "tier": tier,
            "status": status,
            "message": message,
            "duration_seconds": round(elapsed_test, 4)
        })

    elapsed_all = time.time() - start_time_all

    # Compile Summary
    summary = {
        "total": total_tests,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": errors,
        "duration_seconds": round(elapsed_all, 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    # Save JSON Report
    report_data = {
        "summary": summary,
        "tests": results_details
    }
    report_path = os.path.join(PROJECT_ROOT, "e2e_tests", "test_report.json")
    try:
        with open(report_path, "w", encoding="utf-8") as rf:
            json.dump(report_data, rf, indent=2)
        print("-" * 60)
        print(f"Saved test report to {report_path}")
    except Exception as e:
        print("-" * 60)
        print(f"WARNING: Could not save test report: {e}")

    print("-" * 60)
    print("TEST SUMMARY")
    print("-" * 60)
    print(f"Total:      {summary['total']}")
    print(f"Passed:     {summary['passed']}")
    print(f"Failed:     {summary['failed']}")
    print(f"Skipped:    {summary['skipped']}")
    print(f"Errors:     {summary['errors']}")
    print(f"Duration:   {summary['duration_seconds']}s")
    print("=" * 60)

    # Exit code decision
    if failed > 0 or errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
