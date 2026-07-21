import json

from pathlib import Path
from datetime import datetime, timezone



class MetadataBuilder:
    """
    Generate research artifact metadata.
    """


    def build(
        self,
        output_dir,
        strategy_name,
        display_name,
        version="v1.2",
        category="",
    ):

        output_dir = Path(output_dir)


        metadata = {

            "strategy":
                strategy_name,


            "display_name":
                display_name,


            "version":
                version,


            "category":
                category,


            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "generated_by":
                "Quant Option Research Platform",


            "artifacts":
                [

                    "report.docx",

                    "report.pdf",

                    "summary.md",

                    "trades.csv",

                    "charts/",

                ],

        }


        path = (
            output_dir
            /
            "metadata.json"
        )


        path.write_text(
            json.dumps(
                metadata,
                indent=4,
            ),
            encoding="utf-8",
        )


        return path