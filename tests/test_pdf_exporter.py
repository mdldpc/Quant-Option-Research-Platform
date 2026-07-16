from framework.reporting.pdf_exporter import PDFExporter


def test_pdf_exporter_creation():

    exporter = PDFExporter()

    assert exporter is not None