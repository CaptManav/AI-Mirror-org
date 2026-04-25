from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.responses import PlainTextResponse
from app.draft_store import load_drafts, save_drafts
from app.email_reader import get_service, send_gmail_reply
import app.config as config
import re
def extract_email(raw):
    match = re.search(r"<(.+?)>", raw)
    return match.group(1) if match else raw
app = FastAPI()
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == "mirror_verify_123"
    ):
        return PlainTextResponse(params.get("hub.challenge"))

    return PlainTextResponse("Verification failed", status_code=403)


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("📩 WhatsApp Event:", data)
    return {"status": "ok"}

config.CURRENT_TONE = "Professional"
config.AUTO_SEND = False


# ===============================
# 🏠 HOME PAGE
# ===============================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>AI Mirror</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>

    <body class="bg-gray-100 flex items-center justify-center h-screen">

        <div class="text-center">

            <h1 class="text-4xl font-bold mb-10">AI Mirror</h1>

            <div class="flex gap-10 justify-center">

                <a href="/gmail" class="bg-blue-500 hover:bg-blue-600 text-white p-10 rounded-2xl shadow-lg w-60 text-center">
                    <div class="text-5xl mb-4">📧</div>
                    <div class="text-xl font-semibold">Gmail</div>
                </a>

                <a href="/instagram" class="bg-purple-500 hover:bg-purple-600 text-white p-10 rounded-2xl shadow-lg w-60 text-center">
                    <div class="text-5xl mb-4">📸</div>
                    <div class="text-xl font-semibold">Instagram</div>
                </a>

                <a href="/whatsapp" class="bg-green-500 hover:bg-green-600 text-white p-10 rounded-2xl shadow-lg w-60 text-center">
    <div class="text-5xl mb-4">💬</div>
    <div class="text-xl font-semibold">WhatsApp</div>
</a>

            </div>

        </div>

    </body>
    </html>
    """


# ===============================
# 🔧 SHARED DASHBOARD
# ===============================
def build_dashboard(drafts, title, request: Request):

    pending_count = sum(1 for d in drafts if d["status"] == "PENDING")
    sent_count = sum(1 for d in drafts if d["status"] == "SENT")
    discarded_count = sum(1 for d in drafts if d["status"] == "DISCARDED")
    total_count = len(drafts)

    html = f"""
    <html>
    <head>
        <title>{title}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <meta http-equiv="refresh" content="10">
    </head>

    <body class="bg-gray-100">

        <!-- HEADER -->
        <div class="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white shadow-lg">
            <h1 class="text-3xl font-bold">{title}</h1>
            <a href="/" class="text-sm underline">← Back</a>
        </div>

        <div class="p-10">

            <!-- STATUS -->
            <div class="grid grid-cols-4 gap-6 mb-10">

                <div class="bg-white p-6 rounded-2xl shadow text-center">
                    <p class="text-gray-500 text-sm">Total</p>
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

            <!-- CONTROLS -->
            <div class="mb-8 flex items-center gap-6">

                <!-- Tone -->
                <form method="post" action="/set-tone">
                    <select name="tone" onchange="this.form.submit()" class="p-2 rounded-lg border">
                        <option value="Professional" {"selected" if config.CURRENT_TONE=="Professional" else ""}>Professional</option>
                        <option value="Friendly" {"selected" if config.CURRENT_TONE=="Friendly" else ""}>Friendly</option>
                        <option value="Direct" {"selected" if config.CURRENT_TONE=="Direct" else ""}>Direct</option>
                        <option value="Formal" {"selected" if config.CURRENT_TONE=="Formal" else ""}>Formal</option>
                    </select>
                </form>

                <!-- AUTO SEND -->
                <form method="post" action="/toggle-auto-send">
                    <input type="hidden" name="redirect_url" value="{request.url.path}">
                    <button class="px-4 py-2 rounded-lg text-white
                        {"bg-green-500" if config.AUTO_SEND else "bg-gray-500"}">
                        {"⚡ Auto Send ON" if config.AUTO_SEND else "Auto Send OFF"}
                    </button>
                </form>

            </div>

            <h2 class="text-xl font-semibold mb-6">Pending Drafts</h2>
    """

    if not any(d["status"] == "PENDING" for d in drafts):
        html += """
        <div class="text-center text-gray-400 mt-20">
            <p class="text-lg">📭 No pending messages</p>
        </div>
        """

    for draft in reversed(drafts):

        if draft["status"] == "PENDING":

            # ✅ FIXED CHANNEL LOGIC
            channel = draft.get("channel", "gmail")

            if channel == "gmail":
                channel_label = "📧 Gmail"
                channel_color = "bg-blue-100 text-blue-700"
            elif channel == "instagram":
                channel_label = "📸 Instagram"
                channel_color = "bg-purple-100 text-purple-700"
            else:
                channel_label = "💬 WhatsApp"
                channel_color = "bg-green-100 text-green-700"

            html += f"""
            <div class="bg-white p-6 rounded-2xl shadow mb-6">

                <div class="flex justify-between items-center mb-2">

                    <div class="flex items-center gap-3">

                        <span class="text-xs px-2 py-1 rounded-full {channel_color}">
                            {channel_label}
                        </span>

                        <span class="text-sm text-gray-500">
                            {draft.get("sender", "unknown")}
                        </span>

                        <!-- 🧠 LEARNING -->
                        <span class="text-xs text-purple-600">
                            🧠 Learning Enabled
                        </span>

                        <!-- 🏷 CATEGORY -->
                        <span class="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded-full">
                            {draft.get("category", "General")}
                        </span>

                    </div>

                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                        PENDING
                    </span>

                </div>

                <div class="mb-3 bg-gray-50 p-3 rounded">
                    {draft["incoming"]}
                </div>

                <div class="mb-4 bg-indigo-50 p-3 rounded">
                    {draft["draft"]}
                </div>

                <div class="flex gap-3">
                    <a href="/edit/{draft['id']}" class="bg-blue-500 text-white px-4 py-2 rounded">Edit</a>
                    <a href="/send/{draft['id']}" class="bg-green-500 text-white px-4 py-2 rounded">Send</a>
                    <a href="/discard/{draft['id']}" class="bg-red-500 text-white px-4 py-2 rounded">Discard</a>
                </div>

            </div>
            """

    html += "</div></body></html>"
    return html


# ===============================
# 📧 GMAIL
# ===============================
@app.get("/gmail", response_class=HTMLResponse)
def gmail_dashboard(request: Request):
    drafts = [d for d in load_drafts() if d["channel"] == "gmail"]
    return build_dashboard(drafts, "📧 Gmail Dashboard", request)


# ===============================
# 📸 INSTAGRAM
# ===============================
@app.get("/instagram", response_class=HTMLResponse)
def instagram_dashboard(request: Request):
    drafts = [d for d in load_drafts() if d["channel"] == "instagram"]
    return build_dashboard(drafts, "📸 Instagram Dashboard", request)

@app.get("/whatsapp", response_class=HTMLResponse)
def whatsapp_dashboard(request: Request):
    drafts = [d for d in load_drafts() if d["channel"] == "whatsapp"]
    return build_dashboard(drafts, "💬 WhatsApp Dashboard", request)
# ===============================
# TOGGLE AUTO SEND
# ===============================
@app.post("/toggle-auto-send")
def toggle_auto_send(redirect_url: str = Form("/")):
    config.AUTO_SEND = not config.AUTO_SEND
    return RedirectResponse(redirect_url, status_code=302)


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
# SEND
# ===============================
@app.get("/send/{draft_id}")
def send_draft(draft_id: str):

    drafts = load_drafts()

    for d in drafts:
        if d["id"] == draft_id and d["status"] == "PENDING":

            sender = d.get("sender") or d.get("from")

            if not sender:
                print("❌ Missing sender, skipping:", d)
                continue

            channel = d.get("channel", "gmail")

            # 📧 GMAIL
            if channel == "gmail":
                service = get_service()
                send_gmail_reply(
                    service,
                    original_msg_id=d.get("message_id"),
                    thread_id=d.get("thread_id"),
                    to_email=sender,
                    subject=d.get("subject", ""),
                    body_text=d["draft"]
                )

            # 💬 WHATSAPP
            elif channel == "whatsapp":
                from app.whatsapp_sender import send_whatsapp_message
                send_whatsapp_message(sender, d["draft"])

            # 📸 INSTAGRAM
            elif channel == "instagram":
                from app.instagram_handler import send_instagram_reply
                thread_id = d.get("thread_id")

                if not thread_id:
                    print("❌ Missing thread_id for Instagram:", d)
                    continue

                send_instagram_reply(thread_id, d["draft"])

            # ✅ mark as sent
            d["status"] = "SENT"

    save_drafts(drafts)
    return RedirectResponse("/", status_code=302)

# ===============================
# EDIT
# ===============================
@app.get("/edit/{draft_id}", response_class=HTMLResponse)
def edit_draft_page(draft_id: str):

    drafts = load_drafts()

    for d in drafts:
        if d["id"] == draft_id:
            return f"""
            <html><body class="p-10">
            <form method="post" action="/update/{draft_id}">
                <textarea name="updated_text" class="w-full h-64">{d["draft"]}</textarea>
                <button type="submit">Save</button>
            </form>
            </body></html>
            """

    return RedirectResponse("/", status_code=302)


# ===============================
# UPDATE + LEARNING
# ===============================
from app.generate import collection

@app.post("/update/{draft_id}")
def update_draft(draft_id: str, updated_text: str = Form(...)):

    drafts = load_drafts()

    for d in drafts:
        if d["id"] == draft_id:
            d["draft"] = updated_text

            try:
                collection.add(
                    documents=[updated_text],
                    ids=[f"learn_{draft_id}"]
                )
                print("🧠 Learned new writing style")
            except Exception as e:
                print("Learning error:", e)

    save_drafts(drafts)
    return RedirectResponse("/", status_code=302)


# ===============================
# SET TONE
# ===============================
@app.post("/set-tone")
def set_tone(tone: str = Form(...)):
    config.CURRENT_TONE = tone
    return RedirectResponse("/", status_code=302)