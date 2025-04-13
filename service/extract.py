import re
import json
import logging
import os
from datetime import datetime
from typing import List, Dict

def setup_logger() -> logging.Logger:
    """
    Uses (or creates) the 'log' directory and appends log entries
    to today’s date-named file.
    """
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(log_dir, f"{today}.log")

    logger = logging.getLogger("vuln_extractor")
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

def extract_vulnerabilities(input_path: str) -> List[Dict[str, str]]:
    """
    Extracts vulnerability blocks from the given text file, writes them
    to a fixed 'vulnerabilities.json' file, and logs steps to 'log/YYYY-MM-DD.log'.

    Args:
        input_path (str): Path to the source text file.

    Returns:
        List[Dict[str, str]]: List of extracted vulnerabilities.
    """
    output_path = "vulnerabilities.json"
    logger = setup_logger()
    logger.info(f"Starting extraction: input={input_path}, output={output_path}")

    # Read input file
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info("Input file read successfully.")
    except Exception as e:
        logger.error(f"Failed to read input file: {e}")
        raise

    # Find blocks via regex
    pattern = (
        r'(\d{5}) - (.+?)\n'
        r'Synopsis\n(.*?)\n'
        r'See Also\n(.*?)\n'
        r'(.*?)Plugin Information'
    )
    blocks = re.findall(pattern, content, re.DOTALL)
    logger.info(f"Found {len(blocks)} vulnerability blocks.")

    vulns = []
    for idx, (vuln_id, title, description, see_also, rest) in enumerate(blocks, 1):
        vulns.append({
            "id": vuln_id,
            "title": title.strip(),
            "description": description.strip().replace("\n", " "),
            "see_also": see_also.strip(),
        })
        logger.debug(f"Block #{idx}: id={vuln_id}, title={title.strip()}")

    # Write to JSON
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(vulns, f, indent=4, ensure_ascii=False)
        logger.info(f"JSON file written: {output_path}")
    except Exception as e:
        logger.error(f"Failed to write JSON file: {e}")
        raise

    logger.info("Extraction completed.")
    return vulns