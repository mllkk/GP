import PyPDF2
import os
import logging
from datetime import datetime


def setup_logger() -> logging.Logger:
    """
    Uses (or creates) the 'log' directory and appends log entries
    to today’s date-named file.
    """
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(log_dir, f"{today}.log")

    logger = logging.getLogger("pdf_converter")
    logger.setLevel(logging.INFO)

    # Only add the handler once per session
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == log_path 
               for h in logger.handlers):
        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def pdf_to_text(pdf_path: str) -> str:
    """
    Extracts text from the given PDF and writes it to temp/<basename>.txt,
    logging each step to 'log/YYYY-MM-DD.log'.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Path to the generated text file.
    """
    logger = setup_logger()
    logger.info(f"Starting PDF-to-text conversion: {pdf_path}")

    # Ensure output folder exists
    output_folder = "temp"
    os.makedirs(output_folder, exist_ok=True)

    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_txt = os.path.join(output_folder, base_filename + ".txt")

    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            logger.info(f"Opened PDF, {len(pdf_reader.pages)} pages found.")

            text = ''
            for i, page in enumerate(pdf_reader.pages, start=1):
                page_text = page.extract_text() or ''
                text += page_text
                logger.debug(f"Extracted text from page {i} ({len(page_text)} characters).")

        with open(output_txt, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        logger.info(f"Text written to: {output_txt}")

    except Exception as e:
        logger.error(f"PDF conversion failed: {e}")
        raise

    logger.info("PDF-to-text conversion completed successfully.")
    return output_txt
