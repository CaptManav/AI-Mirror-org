from app.email_reader import get_service, get_latest_email
from app.email_draft import create_draft
from app.generate import generate_reply

print("Connecting to Gmail...")
service = get_service()

print("Fetching latest email...")
email_text = get_latest_email(service)

if not email_text:
    print("❌ No readable email body found.")
    exit()

print("\nLATEST EMAIL:\n", email_text)

reply = generate_reply(email_text)

print("\nMIRROR REPLY:\n", reply)

create_draft(service, reply)
