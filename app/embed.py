import json
from sentence_transformers import SentenceTransformer
import chromadb

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Opening Chroma DB...")
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection("style_memory")

print("Loading samples...")
with open("data/clean_samples.json", "r", encoding="utf-8") as f:
    samples = json.load(f)

print("Embedding and storing...")

for i, item in enumerate(samples):
    emb = model.encode(item["text"]).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[emb],
        documents=[item["text"]],
        metadatas=[{"source": item["source"]}]
    )

    print("Stored:", i)

print("DONE — style memory built.")
