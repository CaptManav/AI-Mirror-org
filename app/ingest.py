import os
import json

DATA_DIR = "data/style_samples"
OUTPUT_FILE = "data/clean_samples.json"

def ingest():
    print("Starting ingestion...")

    samples = []

    for filename in os.listdir(DATA_DIR):
        print("Reading:", filename)

        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()

                if len(text) > 10:
                    samples.append({
                        "text": text,
                        "source": filename
                    })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)

    print("DONE — samples:", len(samples))


if __name__ == "__main__":
    ingest()
