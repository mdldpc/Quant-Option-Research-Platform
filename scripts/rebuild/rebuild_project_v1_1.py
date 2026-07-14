from scripts.rebuild.rebuild_common import iter_cleaned_sessions

from scripts.rebuild.rebuild_daily_pipeline_v1_1 import process_one_file
from scripts.rebuild.combine_daily_greeks_v1_1 import main as combine_greeks

from scripts.rebuild.rebuild_research_datasets import main as build_research

from scripts.rebuild.rebuild_strangle_dataset_v1_1 import main as build_strangle_dataset
from scripts.rebuild.rebuild_butterfly_dataset_v1_1 import main as build_butterfly_dataset
from scripts.rebuild.rebuild_calendar_dataset_v1_1 import main as build_calendar_dataset

from scripts.rebuild.rebuild_strangle_snapshot_v1_1 import main as build_strangle_snapshot
from scripts.rebuild.rebuild_butterfly_snapshot_v1_1 import main as build_butterfly_snapshot
from scripts.rebuild.rebuild_calendar_snapshot_v1_1 import main as build_calendar_snapshot


def run_daily_pipeline():

    print("=" * 80)
    print("STEP 1: DAILY PIPELINE")
    print("=" * 80)

    files = list(iter_cleaned_sessions())

    print(f"Total sessions: {len(files)}")

    for file_path in files:

        print("-" * 60)
        print("Processing:", file_path.name)

        try:
            process_one_file(file_path)

        except Exception as e:

            print("FAILED:", file_path)
            print("ERROR:", repr(e))
            continue


def run_combine():

    print("=" * 80)
    print("STEP 2: COMBINE GREEKS")
    print("=" * 80)

    combine_greeks()


def run_research():

    print("=" * 80)
    print("STEP 3: RESEARCH DATASETS")
    print("=" * 80)

    build_research()


def run_strategy_datasets():

    print("=" * 80)
    print("STEP 4: STRATEGY DATASETS")
    print("=" * 80)

    build_strangle_dataset()
    build_butterfly_dataset()
    build_calendar_dataset()


def run_snapshots():

    print("=" * 80)
    print("STEP 5: SNAPSHOTS")
    print("=" * 80)

    build_strangle_snapshot()
    build_butterfly_snapshot()
    build_calendar_snapshot()


def main():

    print("#" * 80)
    print("FULL REBUILD PIPELINE v1.1")
    print("#" * 80)

    run_daily_pipeline()
    run_combine()
    run_research()
    run_strategy_datasets()
    run_snapshots()

    print("#" * 80)
    print("REBUILD COMPLETE")
    print("#" * 80)


if __name__ == "__main__":
    main()