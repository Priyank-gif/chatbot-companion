from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models, database

router = APIRouter(tags=['Chat'])


@router.get("/retrieve-chat/")
async def retrieve_chat(user_id: int, chat_id: int, db: Session = Depends(database.get_db)):
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.user_id == user_id,
        models.ChatMessage.chat_id == chat_id
    ).order_by(models.ChatMessage.chat_order).all()

    if not messages:
        raise HTTPException(status_code=404, detail="Chat not found")

    response_messages_list = []
    for message in messages:
        message_dict = {'chat_order':message.chat_order,
                        'message_type': message.message_type,
                        'message': message.message
                        }
        response_messages_list.append(message_dict)

    response = {'user_id': user_id,
                'chat_id': chat_id,
                'messages': response_messages_list}
    return response


@router.post("/start-chat/")
async def start_chat(user_id: int, db: Session = Depends(database.get_db)):
    # Create a new chat session in the database
    db_chat_session = models.ChatSession(user_id=user_id)
    db.add(db_chat_session)
    db.commit()
    db.refresh(db_chat_session)

    # AI's initial greeting message
    ai_message = "Hello there, I am your AI assistant. How may I help you?"

    # Create and store the AI message in the database
    db_message = models.ChatMessage(
        user_id=user_id,
        chat_id=db_chat_session.chat_id,
        message_type="ai",
        chat_order=1,  # First message of the chat
        message=ai_message
    )
    db.add(db_message)
    db.commit()
    response_messages_list=[]
    message_dict = {'chat_order': db_message.chat_order,
                    'message_type': db_message.message_type,
                    'message': db_message.message
                    }
    response_messages_list.append(message_dict)
    response = {'user_id': db_message.user_id,
                'chat_id': db_message.chat_id,
                'messages': response_messages_list}
    return response


@router.delete("/delete-chat/")
async def delete_chat(user_id: int, chat_id: int, db: Session = Depends(database.get_db)):
    # Query to find the chat session
    chat_session = db.query(models.ChatSession).filter(
        models.ChatSession.chat_id == chat_id,
        models.ChatSession.user_id == user_id
    ).first()

    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    # Delete all messages associated with the chat session
    db.query(models.ChatMessage).filter(
        models.ChatMessage.chat_id == chat_id
    ).delete()

    # Delete the chat session itself
    db.delete(chat_session)
    db.commit()

    return {"detail": "Chat deleted successfully"}


@router.get("/get-user-chats/", response_model=List[models.ChatSessionResponse])
async def get_user_chats(user_id: int, db: Session = Depends(database.get_db)):
    # Query to find all chat sessions for the user
    chat_sessions = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user_id
    ).order_by(desc(models.ChatSession.last_updated)).all()

    if not chat_sessions:
        raise HTTPException(status_code=404, detail="No chat sessions found for the user")

    return chat_sessions
