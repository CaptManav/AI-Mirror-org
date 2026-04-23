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

import uuid
from datetime import datetime
import json

DRAFT_FILE = "data/drafts.json"


def load_drafts():
    try:
        with open(DRAFT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_drafts(drafts):
    with open(DRAFT_FILE, "w") as f:
        json.dump(drafts, f, indent=2)


def create_draft(
    channel,
    sender,
    incoming,
    draft,
    risk,
    status="PENDING",   # ✅ NEW
    category="General"  # ✅ NEW
):
    drafts = load_drafts()

    new_draft = {
        "id": str(uuid.uuid4()),
        "channel": channel,
        "sender": sender,
        "incoming": incoming,
        "draft": draft,
        "risk": risk,
        "status": status,        # ✅ NOW SUPPORTED
        "category": category,    # ✅ NOW SUPPORTED
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    drafts.append(new_draft)
    save_drafts(drafts)
    

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
