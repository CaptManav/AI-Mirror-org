import json
import uuid
from datetime import datetime
from pathlib import Path
from datetime import datetime

DRAFT_FILE = Path("data/drafts.json")
DRAFT_FILE.parent.mkdir(exist_ok=True)

def load_drafts():
    if not DRAFT_FILE.exists():
        return []
    with open(DRAFT_FILE, "r") as f:
        return json.load(f)

def save_drafts(drafts):
    DRAFT_FILE.write_text(json.dumps(drafts, indent=2))

def create_draft(channel, sender, incoming, draft, risk):
    drafts = load_drafts()
    

    item = {
        "id": str(uuid.uuid4()),
        "channel": channel,
        "from": sender,
        "incoming": incoming,
        "draft": draft,
        "risk": risk,
        "status": "PENDING",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    drafts.append(item)
    save_drafts(drafts)
    return item
