from datetime import datetime

from fastapi import HTTPException, APIRouter, Depends
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_core.tracers import langchain
from sqlalchemy.orm import Session

from app import database
from app.config import vector_db_path, embeddings, llm
from app.faiss_index import load_faiss_index
from app.models import QueryModel, ChatMessage, ChatSession

router = APIRouter(tags=['Ask Question'])


@router.post("/ask-question/")
def ask_question(query_model: QueryModel, db: Session = Depends(database.get_db)):
    query = query_model.query
    if not query:
        raise HTTPException(status_code=400, detail="Query is empty")

    # Fetch the chat session
    chat_session = db.query(ChatSession).filter(
        ChatSession.chat_id == query_model.chat_id,
        ChatSession.user_id == query_model.user_id
    ).first()
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    # Update last_updated field
    chat_session.last_updated = datetime.utcnow()
    db.commit()

    # Store the query in the database
    db_message = ChatMessage(
        user_id=query_model.user_id,
        chat_id=query_model.chat_id,
        message_type="human",
        chat_order=query_model.chat_order + 1,
        message=query_model.query
    )
    db.add(db_message)
    db.commit()
    vector_store = load_faiss_index(embeddings, vector_db_path)
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_store.as_retriever())
    langchain.debug = True
    result = chain({'question': query}, return_only_outputs=True)

    answer = result.get("answer", "No answer found")
    sources = result.get("sources", "")

    db_message = ChatMessage(
        user_id=query_model.user_id,
        chat_id=query_model.chat_id,
        message_type="ai",
        chat_order=query_model.chat_order + 2,  # Increment to keep order
        message=answer
    )
    db.add(db_message)
    db.commit()
    return {
        "answer": answer,
        "sources": sources.split("\n") if sources else [],
        "user_id": query_model.user_id,
        "chat_id": query_model.chat_id,
        "chat_order": query_model.chat_order + 2
    }
