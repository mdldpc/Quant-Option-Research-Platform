from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RebuildResult:
    job_name: str
    status: str
    output_path: Optional[Path] = None
    rows: int = 0
    message: str = ""


class RebuildJob:
    job_name = "unknown_rebuild_job"

    def validate_inputs(self) -> None:
        raise NotImplementedError

    def run(self) -> RebuildResult:
        raise NotImplementedError

    def print_result(self, result: RebuildResult) -> None:
        print("=" * 72)
        print(f"Rebuild Job: {result.job_name}")
        print("=" * 72)
        print(f"Status : {result.status}")
        print(f"Rows   : {result.rows}")

        if result.output_path is not None:
            print(f"Output : {result.output_path}")

        if result.message:
            print(f"Message: {result.message}")