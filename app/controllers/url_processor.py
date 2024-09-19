
from fastapi import HTTPException, APIRouter
from app.models import UrlsModel
from app.config import vector_db_path, embeddings
from app.faiss_index import create_vector_store, fetch_documents_from_url, split_documents

router = APIRouter(tags=['URL Process'])
@router.post("/process-urls/")
def process_urls(urls_model: UrlsModel):
    urls = urls_model.urls
    if not urls:
        raise HTTPException(status_code=400, detail="URL list is empty")

    documents = fetch_documents_from_url(urls)
    docs = split_documents(documents)
    create_vector_store(docs, vector_db_path, embeddings)
    return {"message": "URLs processed and vector store created"}