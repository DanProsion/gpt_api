from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.api import get_db
from app import schemas, services
from ..database import models

from sqlalchemy.future import select

router = APIRouter()


@router.post("/chat/", response_model=schemas.MessageResponse)
async def chat_with_ai(request: schemas.MessageCreate, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(models.User).where(models.User.id == request.conversation_id))
    user = user.scalars().first()

    if not user:
        new_user = models.User(username=f"user_{request.conversation_id}")
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        user_id = new_user.id
    else:
        user_id = user.id

    # Проверяем, существует ли conversation
    conversation = await db.execute(select(models.Conversation).where(models.Conversation.id == request.conversation_id))
    conversation = conversation.scalars().first()

    if not conversation:
        # Создаем новый диалог
        new_conversation = models.Conversation(user_id=user_id)
        db.add(new_conversation)
        await db.commit()
        await db.refresh(new_conversation)
        request.conversation_id = new_conversation.id

    ai_response = await services.get_ai_response(request.text)

    # Сохраняем сообщение пользователя
    user_message = models.Message(
        conversation_id=request.conversation_id,
        sender="user",
        text=request.text
    )
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)

    # Сохраняем ответ бота
    bot_message = models.Message(
        conversation_id=request.conversation_id,
        sender="bot",
        text=ai_response
    )
    db.add(bot_message)
    await db.commit()
    await db.refresh(bot_message)

    return schemas.MessageResponse(
        id=bot_message.id,
        sender="bot",
        text=bot_message.text,
        timestamp=bot_message.timestamp
    )

