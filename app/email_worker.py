import time
import traceback

from app.email_reader import get_service, get_unread_emails, mark_as_processed
from app.generate import generate_reply
from app.draft_store import create_draft


POLL_SECONDS = 60  # 1 minute


def run():
    print("📬 Email worker started. Checking Gmail every 60 seconds...")
    service = get_service()

    while True:
        try:
            emails = get_unread_emails(service, limit=2)

            if not emails:
                print("No new emails.")
            else:
                print(f"Found {len(emails)} new email(s).")

            for mail in emails:
                sender = mail.get("from", "unknown")
                subject = mail.get("subject", "")
                body = mail.get("body", "")
                msg_id = mail.get("id")

                incoming_text = f"Subject: {subject}\n\n{body}"

                print("Processing email from:", sender)

                reply = generate_reply(incoming_text)

                create_draft(
                    channel="gmail",
                    sender=sender,
                    incoming=incoming_text,
                    draft=reply,
                    risk="LOW",
                )

                # Mark email so we don't process it again
                mark_as_processed(service, msg_id)

                print("✅ Draft saved for:", sender)

        except Exception as e:
            print("❌ Worker error:", e)
            traceback.print_exc()

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    run()