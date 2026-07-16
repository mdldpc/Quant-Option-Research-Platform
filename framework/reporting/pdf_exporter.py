from pathlib import Path
import subprocess


class PDFExporter:
    """
    Convert DOCX reports into PDF.

    Uses LibreOffice conversion engine.
    """


    def convert(
        self,
        docx_path,
        output_dir=None,
    ) -> Path:

        docx_path = Path(docx_path)


        if output_dir is None:
            output_dir = docx_path.parent


        output_dir = Path(output_dir)


        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_dir),
                str(docx_path),
            ],
            check=True,
        )


        return (
            output_dir
            /
            f"{docx_path.stem}.pdf"
        )