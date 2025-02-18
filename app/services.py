import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def get_ai_response(user_message: str) -> str:
    """Отправляет запрос к OpenAI API и получает ответ от модели 'gpt-4o-mini'"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Be a friend to the user"}, # Системный запрос, можно вписать что угодно,
                {"role": "user", "content": user_message} # Наше сообщение
            ]
        )
        ai_response = response['choices'][0]['message']['content'].strip()
        print("AI response:", ai_response)
        return ai_response
    except Exception as e:
        print(f"Ошибка AI: {str(e)}")
        return f"Ошибка AI: {str(e)}"
