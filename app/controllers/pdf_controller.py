import os

from fastapi import HTTPException, APIRouter, UploadFile, File

from app.config import vector_db_path, embeddings, temp_file_path
from app.faiss_index import create_vector_store, split_documents, get_documents_from_pdf

router = APIRouter(tags=['PDF Process'])


@router.post("/process-pdf/")
async def process_pdf(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    if os.path.exists(vector_db_path):
        raise HTTPException(status_code=400,
                            detail="Vector db already exists, please delete that or use extend vector db endpoint.")
    try:
        # Save the uploaded file
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        with open(temp_file_path, "wb") as out_file:
            content = await file.read()
            out_file.write(content)
    except:
        raise HTTPException(status_code=400, detail="could not save pdf ")

    try:
        documents = get_documents_from_pdf(temp_file_path)
        if not documents:
            raise HTTPException(status_code=400, detail="The PDF is empty")
        # Process the extracted text
        docs = split_documents(documents)  # Assuming split_documents can handle a list of texts
        create_vector_store(docs, vector_db_path, embeddings)
        return {"message": "PDF processed and vector store created"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
