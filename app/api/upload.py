from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.pdf_extractor import (
    extract_pdf,
    save_extraction,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required",
        )

    document_id = str(uuid4())

    file_path = UPLOAD_DIR / f"{document_id}_{file.filename}"

    with file_path.open("wb") as buffer:

        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    pages = extract_pdf(str(file_path))

    extraction_file = save_extraction(
        document_id=document_id,
        pages=pages,
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "page_count": len(pages),
        "extraction_file": str(extraction_file),
    }