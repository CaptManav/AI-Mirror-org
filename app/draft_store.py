import json
import uuid
from datetime import datetime
from pathlib import Path

DRAFT_FILE = Path("data/drafts.json")
DRAFT_FILE.parent.mkdir(exist_ok=True)

def load_drafts():
    if not DRAFT_FILE.exists():
        return []
    return json.loads(DRAFT_FILE.read_text())

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
        "created_at": datetime.utcnow().isoformat()
    }

    drafts.append(item)
    save_drafts(drafts)
    return item
