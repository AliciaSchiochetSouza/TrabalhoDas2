import json
import time
from benchmark_config import RESULTS_DIR


def ensure_results_dir():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def benchmark_query(run_query, rounds=5):
    timings = []
    row_count = 0

    for _ in range(rounds):
        start = time.perf_counter()
        rows = run_query()
        elapsed = time.perf_counter() - start
        timings.append(elapsed)
        row_count = len(rows)

    return {
        "rounds": rounds,
        "times_seconds": timings,
        "average_seconds": sum(timings) / len(timings),
        "min_seconds": min(timings),
        "max_seconds": max(timings),
        "rows_returned": row_count,
    }


def save_result(library_name, result):
    ensure_results_dir()
    result_path = RESULTS_DIR / f"{library_name}.json"
    with result_path.open("w", encoding="utf-8") as result_file:
        json.dump(result, result_file, indent=2)
    print(f"Saved result to {result_path}")


def print_result(library_name, result):
    print(f"\n=== Benchmark: {library_name} ===")
    print(f"rounds: {result['rounds']}")
    print(f"rows_returned: {result['rows_returned']}")
    print(f"average_seconds: {result['average_seconds']:.6f}")
    print(f"min_seconds: {result['min_seconds']:.6f}")
    print(f"max_seconds: {result['max_seconds']:.6f}")
