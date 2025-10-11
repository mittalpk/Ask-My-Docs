import uuid
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Document, User
from app.schemas import UploadResponse
from app.routers.auth_router import get_current_user
try:
    from azure.storage.blob import BlobServiceClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    
from app.config import AZURE_STORAGE_CONNECTION_STRING
from app.services.embeddings_service import embed_and_upsert_from_text
import aiofiles
import tempfile

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

    # store file temporarily and optionally upload to Azure Blob Storage
    blob_url = f"local://uploads/{file.filename}"

    suffix = file.filename.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        tmp_path = tmp.name

    if AZURE_AVAILABLE and AZURE_STORAGE_CONNECTION_STRING:
        blob_service = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_name = "documents"
        try:
            blob_service.create_container(container_name)
        except Exception:
            pass

        unique_name = f"{uuid.uuid4()}_{file.filename}"
        blob_client = blob_service.get_blob_client(container=container_name, blob=unique_name)
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
