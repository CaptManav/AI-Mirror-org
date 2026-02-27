# import os
# from dotenv import load_dotenv
# from google import genai
# import chromadb
# from sentence_transformers import SentenceTransformer
# from app.risk import compute_risk


# # --- load keys ---
# load_dotenv()

# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# # --- models ---
# embed_model = SentenceTransformer("all-MiniLM-L6-v2")
# chroma = chromadb.PersistentClient(path="data/chroma_db")
# collection = chroma.get_collection("style_memory")


# def generate_reply(message):

#     # ✅ risk check MUST be inside function
#     risk, level = compute_risk(message)
#     print(f"Risk score: {risk} | Level: {level}")

#     if level == "HIGH":
#         return "[BLOCKED — high-risk message. Human approval required]"

#     print("Embedding query...")
#     emb = embed_model.encode(message).tolist()

#     print("Retrieving style examples...")
#     results = collection.query(
#         query_embeddings=[emb],
#         n_results=3
#     )

#     examples = results["documents"][0]
#     style_block = "\n---\n".join(examples)

#     prompt = f"""
# Write a reply in this user's writing style.

# Style examples:
# {style_block}

# Reply to this message:
# {message}
# """

#     print("Calling Gemini...")
#     resp = client.models.generate_content(
#         model="models/gemini-2.5-flash",
#         contents=prompt
#     )

#     return resp.text


# # --- test runner ---
# if __name__ == "__main__":
#     msg = "Client says the delivery is delayed. Reply politely."
#     reply = generate_reply(msg)

#     print("\nAI MIRROR REPLY:\n")
#     print(reply)
import os
from dotenv import load_dotenv
from groq import Groq
import chromadb
from sentence_transformers import SentenceTransformer
from app.risk import compute_risk
import app.config as config

# --- load keys ---
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- models ---
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma.get_collection("style_memory")


def generate_reply(message):

    # ✅ Risk check
    risk, level = compute_risk(message)
    print(f"Risk score: {risk} | Level: {level}")

    if level == "HIGH":
        return "[BLOCKED — high-risk message. Human approval required]"

    print("Embedding query...")
    emb = embed_model.encode(message).tolist()

    print("Retrieving style examples...")
    results = collection.query(
        query_embeddings=[emb],
        n_results=3
    )

    examples = results["documents"][0]
    style_block = "\n---\n".join(examples)

    # ✅ Get tone safely from config
    current_tone = config.CURRENT_TONE

    # ✅ Improved prompt with tone injection
    user_prompt = f"""
Write a reply in this user's writing style.

Tone: {current_tone}

Match tone strictly. If tone is:
- Professional → Polished, respectful, structured
- Friendly → Warm, conversational, slightly casual
- Direct → Short, concise, minimal fluff
- Formal → Highly structured, respectful, corporate tone

Style examples:
{style_block}

Reply to this message:
{message}
"""

    print("Calling Groq (LLaMA 3.1 8B Instant)...")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert email assistant. Always write in a {current_tone} tone."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content


# --- test runner ---
if __name__ == "__main__":
    msg = "Client says the delivery is delayed. Reply politely."
    reply = generate_reply(msg)

    print("\nAI MIRROR REPLY:\n")
    print(reply)