from framework.research.atm_builder import ATMBuilder
from framework.research.smile_builder import SmileNearBuilder
from framework.research.surface_builder import SurfaceNearBuilder
from framework.research.term_structure_builder import TermStructureBuilder

from framework.research.registry import enabled_research_datasets


BUILDERS = {
    "atm_iv": ATMBuilder,
    "smile_near": SmileNearBuilder,
    "surface_near": SurfaceNearBuilder,
    "term_structure": TermStructureBuilder,
}


def main():

    print("=" * 72)
    print("Research Dataset Rebuild")
    print("=" * 72)
    print()

    enabled = enabled_research_datasets()

    print("Enabled datasets:")

    for name in enabled:
        print("  -", name)

    print()

    results = []

    for name in enabled:

        print("-" * 72)
        print("Building:", name)
        print("-" * 72)

        builder_cls = BUILDERS[name]
        builder = builder_cls()

        result = builder.build()

        results.append(result)

        print()
        print(result)
        print()

    print("=" * 72)
    print("Summary")
    print("=" * 72)

    total_rows = 0

    for r in results:

        total_rows += r.rows

        print(
            f"{r.dataset_name:<20}"
            f"{r.status:<12}"
            f"{r.rows:>12,}"
        )

    print()

    print("Datasets :", len(results))
    print("Rows     :", f"{total_rows:,}")

    print()
    print("Research rebuild completed.")


if __name__ == "__main__":
    main()