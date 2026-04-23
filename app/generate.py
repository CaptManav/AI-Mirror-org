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
collection = chroma.get_or_create_collection("style_memory")


def generate_reply(message, platform="gmail"):

    # ✅ Risk check
    risk, level = compute_risk(message)
    print(f"Risk score: {risk} | Level: {level}")

    if level == "HIGH":
        return "[BLOCKED — high-risk message. Human approval required]"

    # --- embeddings ---
    print("Embedding query...")
    emb = embed_model.encode(message).tolist()

    print("Retrieving style examples...")
    results = collection.query(
        query_embeddings=[emb],
        n_results=1
    )

    examples = results["documents"][0] if results["documents"] else []
    style_block = "\n---\n".join(examples) [:1000] if examples else ""


    # --- tone config ---
    current_tone = config.CURRENT_TONE

    # ✅ PLATFORM-AWARE BEHAVIOR (FIXED)
    if platform == "instagram":
        system_prompt = f"""
You are a friendly Instagram DM assistant.

- Reply casually and naturally
- Keep it short
- Sound human, not corporate
- Use Hinglish/Marathi if message uses it
- DO NOT use email format
- DO NOT say "Dear" or "Best regards"
"""
    else:
        system_prompt = f"""
You are an expert email assistant.

- Write in a {current_tone} tone
- Use proper email structure
- Be clear and professional
"""

    # --- user prompt ---
    user_prompt = f"""
Write a reply in this user's writing style.

Tone: {current_tone}

Style examples:
{style_block}

Reply to this message:
{message}
"""

    print("Calling Groq (LLaMA 3.1 8B Instant)...")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()


# --- test runner ---
if __name__ == "__main__":
    msg = "Client says the delivery is delayed. Reply politely."
    reply = generate_reply(msg)

    print("\nAI MIRROR REPLY:\n")
    print(reply)