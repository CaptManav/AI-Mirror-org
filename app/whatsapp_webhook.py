from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.generate import generate_reply
from app.whatsapp_sender import send_whatsapp_message
from app.draft_store import create_draft
from app.risk import compute_risk
from app.categorizer import detect_category
import app.config as config

app = FastAPI()

VERIFY_TOKEN = "mirror_verify_123"


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(params.get("hub.challenge"))

    return PlainTextResponse("Verification failed", status_code=403)


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        text = msg["text"]["body"]
        sender = msg["from"]

        print("USER:", sender, "MSG:", text)

        # 🔹 Generate AI reply
        from app.generate import generate_reply
        reply = generate_reply(text)

        # 🔹 Save to dashboard
        from app.draft_store import create_draft
        create_draft(
            channel="whatsapp",
            sender=sender,
            incoming=text,
            draft=reply,
            risk="LOW"
        )

        # 🔥 SEND BACK TO WHATSAPP
        from app.whatsapp_sender import send_whatsapp_message
        send_whatsapp_message(sender, reply)

        print("✅ WhatsApp reply sent")

    except Exception as e:
        print("❌ ERROR:", e)

    return {"status": "ok"}