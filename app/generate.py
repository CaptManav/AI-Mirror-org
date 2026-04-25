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
You are a human-like Instagram chat assistant.

Your job is to reply EXACTLY like a real person would in DMs.

STYLE RULES:
- Match the user's tone and energy level
- If user is casual → be casual
- If user is excited → be excited
- If user is dry → be short and dry
- If user is emotional → show empathy

HUMAN BEHAVIOR:
- Use natural phrases (yeah, haha, lol, arre, bro, etc. when appropriate)
- You may use light humor, wit, or sarcasm if it fits
- Keep it conversational, not formal
- Small imperfections are OK (like "gud mornin", "lol", etc.)

STRICT RULES:
- DO NOT sound like email
- DO NOT over-explain
- DO NOT introduce unrelated topics
- Keep replies short (1-3 lines max)

LANGUAGE:
- Mirror user's language (English / Hinglish / Marathi)
- If user mixes languages → you can mix too

GOAL:
Make the reply feel like it was typed by a real human, not AI.
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
User message:
{message}

Write a natural, human-like reply.

Match the vibe, tone, and energy of the user.
"""

    print("Calling Groq (LLaMA 3.1 8B Instant)...")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
        max_tokens=120
    )

    return response.choices[0].message.content.strip()


# --- test runner ---
if __name__ == "__main__":
    msg = "Client says the delivery is delayed. Reply politely."
    reply = generate_reply(msg)

    print("\nAI MIRROR REPLY:\n")
    print(reply)