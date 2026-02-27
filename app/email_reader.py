import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


# =============================
# AUTH
# =============================

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "gmail_credentials.json",
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    return service


# =============================
# HELPERS
# =============================

def _get_header(headers, name):
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


# =============================
# FETCH LIMITED UNREAD EMAILS
# =============================

def get_unread_emails(service, limit=2):
    """
    Fetch only latest `limit` unread emails.
    Prevents token explosion.
    """

    results = service.users().messages().list(
        userId="me",
        q="is:unread newer_than:1d",          # only unread
        maxResults=limit        # limit to 2 (or whatever passed)
    ).execute()

    msgs = results.get("messages", [])
    emails = []

    for msg in msgs:
        msg_id = msg["id"]

        email = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        payload = email["payload"]
        headers = payload.get("headers", [])

        sender = _get_header(headers, "From")
        subject = _get_header(headers, "Subject")

        # 🔒 Skip newsletters / noreply automatically
        if "noreply" in sender.lower() or "no-reply" in sender.lower():
            mark_as_processed(service, msg_id)
            continue

        body = ""
        parts = payload.get("parts", [])

        if parts:
            for p in parts:
                if p.get("mimeType") == "text/plain":
                    data = p.get("body", {}).get("data")
                    if data:
                        body = base64.urlsafe_b64decode(
                            data
                        ).decode(errors="ignore")
                        break
        else:
            data = payload.get("body", {}).get("data")
            if data:
                body = base64.urlsafe_b64decode(
                    data
                ).decode(errors="ignore")

        emails.append({
            "id": msg_id,
            "from": sender,
            "subject": subject,
            "body": body
        })

    return emails


# =============================
# MARK AS PROCESSED
# =============================

def mark_as_processed(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()


# =============================
# SEND EMAIL REPLY
# =============================

from email.mime.text import MIMEText
import base64

def send_gmail_reply(service, original_msg_id, thread_id, to_email, subject, body_text):

    message = MIMEText(body_text)

    message["to"] = to_email
    message["subject"] = subject if subject else "Re:"
    message["In-Reply-To"] = original_msg_id
    message["References"] = original_msg_id

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={
            "raw": raw_message,
            "threadId": thread_id
        }
    ).execute()