
from fastapi import HTTPException, APIRouter
from app.models import QueryModel
from app.config import vector_db_path, embeddings, llm
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_core.tracers import langchain
from app.faiss_index import load_faiss_index


router = APIRouter(tags=['Ask Question'])

@router.post("/ask-question/")
def ask_question(query_model: QueryModel):
    query = query_model.query
    if not query:
        raise HTTPException(status_code=400, detail="Query is empty")

    vector_store = load_faiss_index(embeddings, vector_db_path)
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_store.as_retriever())
    langchain.debug = True
    result = chain({'question': query}, return_only_outputs=True)

    answer = result.get("answer", "No answer found")
    sources = result.get("sources", "")

    return {
        "answer": answer,
        "sources": sources.split("\n") if sources else []
    }