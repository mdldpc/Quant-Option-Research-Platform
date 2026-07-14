from pathlib import Path
import argparse
import subprocess
import sys


OUT_REPORT = Path("research/reports/daily_pipeline_v1_1_report.txt")


STEPS = [
    {
        "name": "Build clean sessions",
        "cmd": [
            sys.executable,
            "-m",
            "scripts.rebuild.build_clean_session_v1_1",
        ],
    },
    {
        "name": "Build portfolio timeseries",
        "cmd": [
            sys.executable,
            "-m",
            "scripts.rebuild.build_portfolio_status_timeseries_v1_1",
        ],
    },
    {
        "name": "Build performance report",
        "cmd": [
            sys.executable,
            "-m",
            "scripts.rebuild.build_performance_report_v1_1",
        ],
    },
]


def run_step(step, dry_run: bool = False):
    name = step["name"]
    cmd = step["cmd"]

    print("=" * 80)
    print(name)
    print("=" * 80)
    print(" ".join(cmd))

    if dry_run:
        return {
            "step": name,
            "status": "dry_run",
            "returncode": 0,
            "stdout": "",
            "stderr": "",
        }

    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    return {
        "step": name,
        "status": "success" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def write_report(results):
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("Daily Pipeline v1.1 Report")
    lines.append("=" * 80)
    lines.append("")

    for r in results:
        lines.append(f"Step       : {r['step']}")
        lines.append(f"Status     : {r['status']}")
        lines.append(f"Returncode : {r['returncode']}")
        lines.append("")
        lines.append("STDOUT")
        lines.append("-" * 80)
        lines.append(r["stdout"] or "")
        lines.append("")
        lines.append("STDERR")
        lines.append("-" * 80)
        lines.append(r["stderr"] or "")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print pipeline steps without running them.",
    )

    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop pipeline when a step fails.",
    )

    args = parser.parse_args()

    results = []

    for step in STEPS:
        result = run_step(
            step,
            dry_run=args.dry_run,
        )

        results.append(result)

        if result["status"] == "failed" and args.stop_on_error:
            break

    write_report(results)

    print("DONE")
    print("Saved:")
    print(OUT_REPORT)


if __name__ == "__main__":
    main()