import time
import traceback

from app.categorizer import detect_category
from app.email_reader import get_service, get_unread_emails, mark_as_processed, send_gmail_reply
from app.generate import generate_reply
from app.draft_store import create_draft
from app.risk import compute_risk
import app.config as config

from app.instagram_handler import (
    login as insta_login,
    fetch_instagram_messages,
    send_instagram_reply
)

POLL_SECONDS = 60  # 1 minute


def run():
    print("📬 Worker started. Checking Gmail + Instagram...")

    # Initialize services
    service = get_service()
    insta_login()

    while True:
        try:
            # =========================
            # 📧 GMAIL PROCESSING
            # =========================
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

                # 🔹 Trim long emails (fix token issue)
                MAX_LEN = 1500
                trimmed_body = body[:MAX_LEN]

                incoming_text = f"Subject: {subject}\n\n{trimmed_body}"

                print("📧 Processing email from:", sender)

                # 🔹 Category + Risk
                category = detect_category(incoming_text)
                risk, level = compute_risk(incoming_text)

                # 🔹 Generate reply
                reply = generate_reply(incoming_text, platform="gmail")

                # 🔥 Decide status
                if config.AUTO_SEND and level == "LOW":
                    print("⚡ Auto-sending email...")

                    send_gmail_reply(
                        service,
                        original_msg_id=msg_id,
                        thread_id=mail.get("thread_id"),
                        to_email=sender,
                        subject=subject,
                        body_text=reply
                    )

                    status = "SENT"
                else:
                    status = "PENDING"

                # 🔹 Save draft (ONLY ONCE)
                create_draft(
                    channel="gmail",
                    sender=sender,
                    incoming=incoming_text,
                    draft=reply,
                    risk=level,
                    status=status,
                    category=category
                )

                # ✅ Mark processed
                mark_as_processed(service, msg_id)

                print("✅ Gmail processed:", sender)

            # =========================
            # 📸 INSTAGRAM PROCESSING
            # =========================
            print("\n📸 Checking Instagram...")

            insta_msgs = fetch_instagram_messages()

            if not insta_msgs:
                print("No new Instagram messages.")
            else:
                print(f"Found {len(insta_msgs)} new Instagram message(s).")

            for msg in insta_msgs:
                text = msg["message"]
                thread_id = msg["thread_id"]

                print("📸 Incoming:", text)

                reply = generate_reply(text, platform="instagram")

                # 🔹 Category
                category = detect_category(text)

                # 🔹 Save to dashboard
                create_draft(
                    channel="instagram",
                    sender="instagram_user",
                    incoming=text,
                    draft=reply,
                    risk="LOW",
                    status="SENT",
                    category=category
                )

                # 🔥 SEND MESSAGE (you forgot this earlier)
                send_instagram_reply(thread_id, reply)

                print("✅ Instagram reply sent")

        except Exception as e:
            print("❌ Worker error:", e)
            traceback.print_exc()

        print(f"\n⏳ Sleeping for {POLL_SECONDS} seconds...\n")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    run()