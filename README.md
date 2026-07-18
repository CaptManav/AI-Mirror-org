# 🪞 AI Mirror

> An AI-powered communication assistant that learns your writing style and generates personalized Gmail reply drafts.

AI Mirror combines LLMs, semantic memory, and Gmail integration to automate email replies while preserving a user's unique tone. Instead of producing generic responses, it retrieves writing patterns from previous emails and generates context-aware drafts that users can review before sending.

---

## ✨ Why I Built It

Most AI email tools generate replies that sound like AI.

I wanted to build something that writes **like the user**, not **for the user**.

The goal was to create a system that learns communication patterns over time, retrieves relevant writing examples using vector search, and produces personalized drafts while keeping the human in control.

---

## 🚀 Key Features

- 📧 Gmail integration with threaded replies
- 🧠 Long-term writing style memory using ChromaDB
- 🤖 Personalized draft generation with LLaMA 3 (Groq)
- ⚠️ Reply confidence & risk analysis
- ✍️ Edit-before-send workflow
- 🎭 Multiple response tones
- 🔄 Background email processing
- 📊 FastAPI dashboard

---

## 🏗️ How It Works

```text
Incoming Email
      │
      ▼
Background Worker
      │
      ▼
Risk Analysis
      │
      ▼
Retrieve Similar Writing Style
   (ChromaDB)
      │
      ▼
LLaMA 3 (Groq)
      │
      ▼
Draft Generated
      │
      ▼
Review → Edit → Send
```

---

## 🖼️ Screenshots

## 🖼️ Product Preview

### Dashboard

Unified inbox for Gmail, WhatsApp, and Instagram with AI-generated drafts.

![](screenshots/Screenshot%20(487).png)

---

### Draft Generation

Users can review and edit AI-generated replies before sending.

![](screenshots/Screenshot%20(486).png)

---

### Memory Retrieval

Vector memory retrieves previous writing patterns to generate replies consistent with the user's style.

![](screenshots/Screenshot%20(485).png)
---

## 🛠️ Tech Stack

**Backend**
- FastAPI
- Python

**AI**
- Groq (LLaMA 3)
- Sentence Transformers
- ChromaDB

**Integrations**
- Gmail API

---

## ⚡ Quick Start

```bash
git clone https://github.com/CaptManav/AI-Mirror-org.git
cd AI-Mirror-org

python -m venv venv
pip install -r requirements.txt
```

Configure:

- Gmail API credentials
- GROQ_API_KEY

Run:

```bash
uvicorn app.main:app --reload
python -m app.email_worker
```

---

## 📂 Repository Structure

```text
app/
├── main.py
├── generate.py
├── email_reader.py
├── email_worker.py
├── draft_store.py
├── risk.py
└── config.py
```

---

## 🚀 Future Improvements

- Multi-user support
- Docker
- React frontend
- WebSockets
- Celery task queue

---

## 👤 Author

Built independently as a product experiment exploring personalized AI communication and autonomous workflow automation.
