import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "gmail_credentials.json",
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    return service


def get_latest_email(service):
    results = service.users().messages().list(
        userId="me",
        maxResults=1,
        q="in:inbox"
    ).execute()

    msgs = results.get("messages", [])
    if not msgs:
        return None

    msg_id = msgs[0]["id"]

    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    payload = msg["payload"]

    parts = payload.get("parts", [])
    for p in parts:
        if p["mimeType"] == "text/plain":
            data = p["body"]["data"]
            return base64.urlsafe_b64decode(data).decode()

    return None
