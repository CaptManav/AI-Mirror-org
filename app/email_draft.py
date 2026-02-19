import base64
from email.mime.text import MIMEText


def create_draft(service, reply_text):

    message = MIMEText(reply_text)
    message["to"] = "atharvmore024@gmail.com"
    message["subject"] = "AI Mirror Draft Reply"

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    draft = {
        "message": {
            "raw": raw
        }
    }

    service.users().drafts().create(
        userId="me",
        body=draft
    ).execute()

    print("✅ Draft created in Gmail")
