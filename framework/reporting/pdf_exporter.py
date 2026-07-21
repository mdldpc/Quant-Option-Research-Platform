from shutil import which
from pathlib import Path
import subprocess



class PDFExporter:


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


        libreoffice = (
            which("libreoffice")
            or
            which("soffice")
        )


        if libreoffice is None:

            raise RuntimeError(
                "LibreOffice is required "
                "for PDF conversion. "
                "Please install LibreOffice "
                "or add it to PATH."
            )


        subprocess.run(
            [
                libreoffice,
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