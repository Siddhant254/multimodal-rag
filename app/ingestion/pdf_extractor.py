from pathlib import Path
import json
import fitz


PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def extract_pdf(file_path: str, document_id: str):
    document = fitz.open(file_path)

    document_dir = PROCESSED_DIR / document_id
    images_dir = document_dir / "images"

    images_dir.mkdir(parents=True, exist_ok=True)

    pages = []

    for page_number, page in enumerate(document, start=1):

        # -------------------------
        # 1. Extract page text
        # -------------------------
        text = page.get_text("text")

        # -------------------------
        # 2. Extract page images
        # -------------------------
        images = []

        for image_index, image_info in enumerate(
            page.get_images(full=True),
            start=1,
        ):
            xref = image_info[0]

            image_data = document.extract_image(xref)

            image_bytes = image_data["image"]
            image_extension = image_data["ext"]

            image_filename = (
                f"page_{page_number}_image_{image_index}.{image_extension}"
            )

            image_path = images_dir / image_filename

            with image_path.open("wb") as image_file:
                image_file.write(image_bytes)

            images.append(
                {
                    "image_id": f"page_{page_number}_image_{image_index}",
                    "filename": image_filename,
                    "path": str(image_path),
                    "extension": image_extension,
                    "width": image_data["width"],
                    "height": image_data["height"],
                }
            )

        # -------------------------
        # 3. Store page information
        # -------------------------
        pages.append(
            {
                "page_number": page_number,
                "text": text,
                "images": images,
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