
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Leer Core.md al iniciar
with open("Core.md", "r", encoding="utf-8") as f:
    core_prompt = f.read()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    user_message = data.get("text", "")

    if not user_message:
        return JSONResponse(content={"text": "Mensaje vacío"}, status_code=400)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": core_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
        )

        reply = response.choices[0].message.content.strip()
        return {"text": reply}

    except Exception as e:
        return JSONResponse(content={"text": f"Error: {str(e)}"}, status_code=500)
