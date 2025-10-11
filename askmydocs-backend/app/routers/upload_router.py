import uuid
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import Document, User
from app.schemas import UploadResponse
from azure.storage.blob import BlobServiceClient
from app.config import AZURE_STORAGE_CONNECTION_STRING
from app.services.embeddings_service import embed_and_upsert_from_text
import aiofiles
import tempfile

router = APIRouter(prefix="/upload", tags=["upload"])

# NOTE: For simplicity this example assumes a user id of 1.
# In production extract user from JWT and load from DB.
async def get_current_user_id():
    return 1

@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    user_id = await get_current_user_id()

    # store file temporarily and upload to Azure Blob Storage
    blob_service = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_name = "documents"
    try:
        blob_service.create_container(container_name)
    except Exception:
        pass

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    blob_client = blob_service.get_blob_client(container=container_name, blob=unique_name)

    # write file content to temporary file first (to pass to text extraction)
    suffix = file.filename.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        tmp_path = tmp.name

    # upload to azure
    with open(tmp_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    blob_url = blob_client.url

    # save metadata to DB
    doc = Document(user_id=user_id, filename=file.filename, blob_url=blob_url)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    # extract text from file (basic for txt; for PDF you'd use pdfplumber or PyPDF2)
    text = ""
    if suffix in ("txt", "md"):
        async with aiofiles.open(tmp_path, mode="r", encoding="utf-8", errors="ignore") as f:
            text = await f.read()
    elif suffix in ("pdf",):
        # lightweight example: use PyPDF2 to extract text
        from PyPDF2 import PdfReader
        reader = PdfReader(tmp_path)
        pages = []
        for p in reader.pages:
            pages.append(p.extract_text() or "")
        text = "\n".join(pages)
    else:
        # fallback: treat as binary -> no text
        text = ""

    # send text for embedding (non-blocking: can be made background task)
    if text.strip():
        metadata = {"doc_id": doc.id, "filename": file.filename}
        await embed_and_upsert_from_text(doc.id, text, metadata)

    return UploadResponse(document_id=doc.id, filename=file.filename, blob_url=blob_url)
