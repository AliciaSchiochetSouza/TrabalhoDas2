import json
from pathlib import Path
from benchmark_config import RESULTS_DIR


def load_results():
    if not RESULTS_DIR.exists():
        raise FileNotFoundError(f"Results folder not found: {RESULTS_DIR}")

    summaries = []
    for path in sorted(RESULTS_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as input_file:
            data = json.load(input_file)
        summaries.append((path.stem, data))
    return summaries


def print_report(summaries):
    print("\n=== Benchmark Summary Report ===")
    for library_name, data in summaries:
        print(f"\n{library_name}")
        print(f"  rounds: {data['rounds']}")
        print(f"  rows_returned: {data['rows_returned']}")
        print(f"  average_seconds: {data['average_seconds']:.6f}")
        print(f"  min_seconds: {data['min_seconds']:.6f}")
        print(f"  max_seconds: {data['max_seconds']:.6f}")
        print(f"  times: {data['times_seconds']}")


def save_markdown_report(summaries):
    output_path = RESULTS_DIR / "benchmark_summary.md"
    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write("# Benchmark Summary Report\n\n")
        for library_name, data in summaries:
            output_file.write(f"## {library_name}\n")
            output_file.write(f"- rounds: {data['rounds']}\n")
            output_file.write(f"- rows_returned: {data['rows_returned']}\n")
            output_file.write(f"- average_seconds: {data['average_seconds']:.6f}\n")
            output_file.write(f"- min_seconds: {data['min_seconds']:.6f}\n")
            output_file.write(f"- max_seconds: {data['max_seconds']:.6f}\n")
            output_file.write(f"- times: {data['times_seconds']}\n\n")
    print(f"Saved markdown report to {output_path}")


def main():
    summaries = load_results()
    print_report(summaries)
    save_markdown_report(summaries)


if __name__ == "__main__":
    main()
