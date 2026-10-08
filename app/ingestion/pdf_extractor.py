from pathlib import Path
import json

import fitz


PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def extract_pdf(file_path: str):
    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text")

        images = page.get_images(full=True)

        pages.append(
            {
                "page_number": page_number,
                "text": text,
                "image_count": len(images),
            }
        )

    document.close()

    return pages


def save_extraction(document_id: str, pages: list):

    output_dir = PROCESSED_DIR / document_id
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "extraction.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "document_id": document_id,
                "pages": pages,
            },
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_file