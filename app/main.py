from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.draft_store import load_drafts, save_drafts
from app.email_reader import get_service, send_gmail_reply

app = FastAPI()

CURRENT_TONE = "Professional"


# ===============================
# DASHBOARD
# ===============================
@app.get("/", response_class=HTMLResponse)
def dashboard():

    drafts = load_drafts()

    pending_count = sum(1 for d in drafts if d["status"] == "PENDING")
    sent_count = sum(1 for d in drafts if d["status"] == "SENT")
    discarded_count = sum(1 for d in drafts if d["status"] == "DISCARDED")
    total_count = len(drafts)

    html = f"""
<html>
<head>
    <title>AI Mirror Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta http-equiv="refresh" content="10">
</head>
<body class="bg-gray-100">

    <div class="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white shadow-lg">
        <h1 class="text-3xl font-bold">AI Mirror</h1>
        <p class="text-sm opacity-90">Your Digital Substitute</p>
    </div>

    <div class="p-10">

        <!-- STATUS CARDS -->
        <div class="grid grid-cols-4 gap-6 mb-10">

            <div class="bg-white p-6 rounded-2xl shadow text-center">
                <p class="text-gray-500 text-sm">Total Drafts</p>
                <p class="text-2xl font-bold">{total_count}</p>
            </div>

            <div class="bg-yellow-50 p-6 rounded-2xl shadow text-center">
                <p class="text-yellow-700 text-sm">Pending</p>
                <p class="text-2xl font-bold text-yellow-800">{pending_count}</p>
            </div>

            <div class="bg-green-50 p-6 rounded-2xl shadow text-center">
                <p class="text-green-700 text-sm">Sent</p>
                <p class="text-2xl font-bold text-green-800">{sent_count}</p>
            </div>

            <div class="bg-red-50 p-6 rounded-2xl shadow text-center">
                <p class="text-red-700 text-sm">Discarded</p>
                <p class="text-2xl font-bold text-red-800">{discarded_count}</p>
            </div>

        </div>

        <!-- TONE SELECTOR -->
        <div class="mb-8 flex items-center gap-4">
            <span class="text-gray-600 font-medium">Tone:</span>

            <form method="post" action="/set-tone">
                <select name="tone"
                        onchange="this.form.submit()"
                        class="p-2 rounded-lg border bg-white shadow-sm">

                    <option value="Professional" {"selected" if CURRENT_TONE=="Professional" else ""}>
                        Professional
                    </option>

                    <option value="Friendly" {"selected" if CURRENT_TONE=="Friendly" else ""}>
                        Friendly
                    </option>

                    <option value="Direct" {"selected" if CURRENT_TONE=="Direct" else ""}>
                        Direct
                    </option>

                    <option value="Formal" {"selected" if CURRENT_TONE=="Formal" else ""}>
                        Formal
                    </option>

                </select>
            </form>
        </div>

        <h2 class="text-xl font-semibold mb-6">Pending Drafts</h2>
    """

    # ===============================
    # DRAFT CARDS
    # ===============================
    for draft in reversed(drafts):

        if draft["status"] == "PENDING":

            html += f"""
            <div class="bg-white p-6 rounded-2xl shadow-lg mb-6 border border-gray-200">

                <div class="flex justify-between items-center mb-2">
                    <div class="text-sm text-gray-600">
                        {draft["from"]}
                    </div>

                    <span class="bg-yellow-100 text-yellow-800 text-xs px-3 py-1 rounded-full">
                        PENDING
                    </span>
                </div>

                <div class="text-xs text-gray-400 mb-4">
                    {draft.get("created_at", "")}
                </div>

                <div class="mb-3">
                    <p class="text-gray-500 text-sm mb-1">Incoming Message</p>
                    <div class="bg-gray-50 p-3 rounded-lg text-sm whitespace-pre-wrap">
                        {draft["incoming"]}
                    </div>
                </div>

                <div class="mb-4">
                    <p class="text-gray-500 text-sm mb-1">AI Suggested Reply</p>
                    <div class="bg-indigo-50 p-3 rounded-lg text-sm whitespace-pre-wrap">
                        {draft["draft"]}
                    </div>
                </div>

                <div class="flex gap-3 mt-4">
                    <a href="/edit/{draft['id']}"
                       class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg">
                       Edit
                    </a>

                    <a href="/send/{draft['id']}"
                       class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg">
                       Send
                    </a>

                    <a href="/discard/{draft['id']}"
                       class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg">
                       Discard
                    </a>
                </div>

            </div>
            """

    html += """
    </div>
</body>
</html>
    """

    return html


# ===============================
# DISCARD
# ===============================
@app.get("/discard/{draft_id}")
def discard_draft(draft_id: str):

    drafts = load_drafts()

    for d in drafts:
        if d["id"] == draft_id:
            d["status"] = "DISCARDED"

    save_drafts(drafts)
    return RedirectResponse("/", status_code=302)


# ===============================
# SEND EMAIL
# ===============================
@app.get("/send/{draft_id}")
def send_draft(draft_id: str):

    drafts = load_drafts()

    for d in drafts:

        if d["id"] == draft_id and d["status"] == "PENDING":

            if d["channel"] == "gmail":

                service = get_service()

                send_gmail_reply(
                    service,
                    original_msg_id=d.get("message_id"),
                    thread_id=d.get("thread_id"),
                    to_email=d["from"],
                    subject=d.get("subject", ""),
                    body_text=d["draft"]
                )

            d["status"] = "SENT"

    save_drafts(drafts)
    return RedirectResponse("/", status_code=302)


# ===============================
# EDIT PAGE
# ===============================
@app.get("/edit/{draft_id}", response_class=HTMLResponse)
def edit_draft_page(draft_id: str):

    drafts = load_drafts()

    for d in drafts:
        if d["id"] == draft_id:

            return f"""
            <html>
            <head>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100 p-10">

                <h1 class="text-2xl font-bold mb-6">Edit Draft</h1>

                <form method="post" action="/update/{draft_id}">

                    <textarea name="updated_text"
                              class="w-full h-64 p-4 border rounded-lg mb-4">
{d["draft"]}
                    </textarea>

                    <button type="submit"
                            class="bg-green-500 text-white px-4 py-2 rounded-lg">
                        Save Changes
                    </button>

                    <a href="/" class="ml-4 text-gray-600">
                        Cancel
                    </a>

                </form>

            </body>
            </html>
            """

    return RedirectResponse("/", status_code=302)


# ===============================
# UPDATE DRAFT
# ===============================
@app.post("/update/{draft_id}")
def update_draft(draft_id: str, updated_text: str = Form(...)):

    drafts = load_drafts()

    for d in drafts:
        if d["id"] == draft_id:
            d["draft"] = updated_text

    save_drafts(drafts)
    return RedirectResponse("/", status_code=302)


# ===============================
# SET TONE
# ===============================
@app.post("/set-tone")
def set_tone(tone: str = Form(...)):
    global CURRENT_TONE
    CURRENT_TONE = tone
    return RedirectResponse("/", status_code=302)