from app.instagram_handler import login, fetch_instagram_messages, send_instagram_reply
from app.generate import generate_reply

login()

msgs = fetch_instagram_messages()

for msg in msgs:
    print("Incoming:", msg["message"])

    reply = generate_reply(msg["message"], platform="instagram")

    print("Reply:", reply)

    send_instagram_reply(msg["thread_id"], reply)