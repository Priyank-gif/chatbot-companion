from fastapi import HTTPException, APIRouter

from app.config import vector_db_path, embeddings
from app.faiss_index import add_to_vector_store, get_text_chunks_langchain
from app.models import TextModel

router = APIRouter(tags=['Extend Vector DB'])


@router.post("/process-text/")
async def process_text(text_model: TextModel):
    if text_model.text == '' or text_model.text == None:
        raise HTTPException(status_code=400, detail="Empty text not allowed")
    try:
        docs = get_text_chunks_langchain(text_model.text)
        add_to_vector_store(docs, vector_db_path, embeddings)
        return {"message": "text processed and vector store extended"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
