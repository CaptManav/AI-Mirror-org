# import json
# import os
# import time
# import random
# PROCESSED_FILE = "processed_ids.json"
# from instagrapi import Client

# cl = Client()

# USERNAME = "atharv_more45"
# PASSWORD = "Atharv@42"

# # Store processed message IDs (prevents duplicate replies)
# PROCESSED_IDS = set()

# def load_processed_ids():
#     if os.path.exists(PROCESSED_FILE):
#         with open(PROCESSED_FILE, "r") as f:
#             return set(json.load(f))
#     return set()

# def save_processed_ids(ids):
#     with open(PROCESSED_FILE, "w") as f:
#         json.dump(list(ids), f)

# def login():
#     cl.delay_range = [1, 3]  # avoid Instagram blocking

#     try:
#         cl.load_settings("session.json")
#         cl.login(USERNAME, PASSWORD)
#     except:
#         cl.login(USERNAME, PASSWORD)
#         cl.dump_settings("session.json")


# def fetch_instagram_messages():
#     messages = []
#     threads = cl.direct_threads(amount=20)

#     processed_ids = load_processed_ids()

#     for thread in threads:
#      for msg in thread.messages:

#         # ❗ Ignore your own messages
#         if msg.is_sent_by_viewer:
#             continue

#         if msg.text and msg.id not in processed_ids:
#             processed_ids.add(msg.id)

#             messages.append({
#                 "id": msg.id,
#                 "platform": "instagram",
#                 "message": msg.text,
#                 "thread_id": thread.id
#             })

#     save_processed_ids(processed_ids)

#     return messages


# def send_instagram_reply(thread_id, text):

#     # 👀 Seen effect
#     print("👀 Seen")
#     time.sleep(random.uniform(0.5, 1.2))

#     # ⌨️ Typing effect
#     print("⌨️ Typing...")
#     simulate_typing_delay(text)

#     # 🚀 Send message
#     cl.direct_send(text, thread_ids=[thread_id])
import json
import os
import time
import random
from instagrapi import Client

# =========================
# CONFIG
# =========================
PROCESSED_FILE = "processed_ids.json"

USERNAME = "atharv_more45"
PASSWORD = "Atharv@42"

cl = Client()


# =========================
# LOAD / SAVE IDS
# =========================
def load_processed_ids():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_processed_ids(ids):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(ids), f)


# =========================
# LOGIN
# =========================
def login():
    cl.delay_range = [1, 3]  # Instagram safety delay

    try:
        cl.load_settings("session.json")
        cl.login(USERNAME, PASSWORD)
    except:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings("session.json")


# =========================
# FETCH MESSAGES
# =========================
def fetch_instagram_messages():
    messages = []
    threads = cl.direct_threads(amount=20)

    processed_ids = load_processed_ids()

    for thread in threads:
        for msg in thread.messages:

            # ❗ Ignore your own messages
            if msg.is_sent_by_viewer:
                continue

            if msg.text and msg.id not in processed_ids:
                processed_ids.add(msg.id)

                messages.append({
                    "id": msg.id,
                    "platform": "instagram",
                    "message": msg.text,
                    "thread_id": thread.id
                })

    save_processed_ids(processed_ids)
    return messages


# =========================
# HUMAN-LIKE DELAY
# =========================
def simulate_typing_delay(message):
    words = len(message.split())

    # ⚡ much faster scaling
    delay = 0.5 + (words * 0.12)

    # small randomness
    delay += random.uniform(0.2, 0.6)

    # cap max delay (IMPORTANT)
    delay = min(delay, 2.5)

    print(f"⏳ Typing delay: {round(delay,2)}s")
    time.sleep(delay)
  

# =========================
# SEND REPLY (HUMANIZED)
# =========================
def send_instagram_reply(thread_id, text):

    try:
        # 👀 Seen simulation
        print("👀 Seen")
        time.sleep(random.uniform(0.5, 1.2))

        # ⌨️ Typing simulation
        print("⌨️ Typing...")
        simulate_typing_delay(text)

        # 🧠 Slight human imperfection (optional)
        if random.random() < 0.1:
            text = text.replace("you", "u")

        # 🚀 Send message
        cl.direct_send(text, thread_ids=[thread_id])

        print("✅ Instagram reply sent")

    except Exception as e:
        print("❌ Instagram send error:", e)