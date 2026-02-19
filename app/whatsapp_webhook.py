from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.generate import generate_reply
from app.whatsapp_sender import send_whatsapp_message

app = FastAPI()

VERIFY_TOKEN = "mirror_verify_123"


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        text = msg["text"]["body"]
        sender = msg["from"]

        print("USER:", sender, "MSG:", text)

        reply = generate_reply(text)
        from app.draft_store import create_draft

    except Exception as e:
        print("IGNORED EVENT:", e)

    return {"status": "ok"}
