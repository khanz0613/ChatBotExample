from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": f"다음에 대해 한국어로만 대답해: {user_input}",
        "stream": True
    }, stream=True)

    full_reply = ""
    for line in response.iter_lines():
        if line:
            try:
                chunk = json.loads(line.decode("utf-8"))
                full_reply += chunk.get("response", "")
            except json.JSONDecodeError:
                continue

    return {"reply": full_reply}
