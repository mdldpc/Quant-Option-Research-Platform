from pathlib import Path
import subprocess
import sys
import time
import importlib


LINE_WIDTH = 72


def banner(title: str):
    print()
    print("=" * LINE_WIDTH)
    print(title)
    print("=" * LINE_WIDTH)


def run_script(
    project_root: Path,
    target: str,
    *,
    as_module: bool = False,
):
    banner(f"Running: {target}")

    start = time.perf_counter()

    if as_module:
        command = [
            sys.executable,
            "-m",
            target,
        ]
    else:
        command = [
            sys.executable,
            str(project_root / target),
        ]

    subprocess.run(
        command,
        cwd=project_root,
        check=True,
    )

    elapsed = time.perf_counter() - start

    print(f"Finished in {elapsed:.2f} sec")

    return elapsed


def verify_files(project_root: Path, expected_files):

    banner("Verifying Outputs")

    missing = []

    for file in expected_files:

        p = project_root / file

        if p.exists():

            print(f"[ OK ] {file}")

        else:

            print(f"[FAIL] {file}")

            missing.append(file)

    return missing


def check_python_packages(packages):

    banner("Checking Python Environment")

    missing = []

    for pkg in packages:

        try:

            importlib.import_module(pkg)

            print(f"[ OK ] {pkg}")

        except ImportError:

            print(f"[FAIL] {pkg}")

            missing.append(pkg)

    if missing:

        raise RuntimeError(
            "Missing Python packages:\n"
            + "\n".join(missing)
        )


def print_summary(
    title: str,
    scripts_executed: int,
    elapsed: float,
    missing_files,
):

    banner(title)

    print()

    status = "SUCCESS" if not missing_files else "FAILED"

    print(f"Status            : {status}")

    print(f"Scripts Executed  : {scripts_executed}")

    print(f"Missing Outputs   : {len(missing_files)}")

    print(f"Elapsed Time      : {elapsed:.2f} sec")

    if missing_files:

        print()

        print("Missing Files:")

        for file in missing_files:

            print("  -", file)

    print()


class Timer:

    def __enter__(self):

        self.start = time.perf_counter()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.elapsed = time.perf_counter() - self.start