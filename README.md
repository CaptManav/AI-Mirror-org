# 🪞 AI Mirror

AI Mirror is an intelligent email assistant that learns your writing style and automatically generates context-aware replies.

It integrates with Gmail, retrieves past writing patterns using vector search (ChromaDB), evaluates message risk, and generates human-like drafts powered by LLaMA 3 via Groq — all accessible through a clean FastAPI dashboard.

---

## 🚀 Features

- 📬 Gmail integration (read + threaded replies)
- 🧠 Writing style memory using ChromaDB (vector embeddings)
- 🤖 AI-generated drafts via Groq (LLaMA 3)
- ⚠ Risk detection before sending replies
- 🎨 Clean FastAPI dashboard with:
  - Draft preview
  - Edit before send
  - Tone selector (Professional / Friendly / Direct / Formal)
  - Status tracking (Pending / Sent / Discarded)
  - Auto-refresh
- 🔄 Background email worker
- 🖱 One-click launcher (Windows .bat)

---

## 🏗 System Architecture

Gmail Inbox
↓
Email Worker (background loop)
↓
Risk Analysis
↓
Style Retrieval (ChromaDB embeddings)
↓
Groq LLaMA 3 Generation
↓
Draft Saved (JSON)
↓
FastAPI Dashboard
↓
Edit → Approve → Send → Gmail Thread Reply


---

## 📂 Project Structure

AI-Mirror-org/
│
├── app/
│ ├── main.py # FastAPI dashboard
│ ├── generate.py # LLM + embedding logic
│ ├── email_worker.py # Background Gmail processor
│ ├── draft_store.py # Draft persistence
│ ├── email_reader.py # Gmail API integration
│ ├── risk.py # Risk scoring logic
│ └── config.py # Global configuration (tone)
│
├── data/ # Runtime data (ignored in Git)
├── start_ai_mirror.bat # One-click launcher (Windows)
├── requirements.txt
├── .gitignore
└── README.md


---

## ⚙ Installation

### 1️⃣ Clone Repository
git clone https://github.com/CaptManav/AI-Mirror-org.git
cd AI-Mirror-org

---

### 2️⃣ Create Virtual Environment
python -m venv venv

Activate:

**Windows**
venv\Scripts\activate

---

### 3️⃣ Install Dependencies
pip install -r requirements.txt

---

## 🔑 Environment Setup

### Set Groq API Key (Permanent – Windows)
setx GROQ_API_KEY "your_api_key_here"

Restart terminal after running this command.

---

## 📬 Gmail API Setup

1. Go to Google Cloud Console  
2. Create a new project  
3. Enable **Gmail API**  
4. Create OAuth 2.0 credentials  
5. Download `credentials.json`  
6. Place `credentials.json` in the project root  

On first run, authentication will generate `token.json`.

⚠ Do NOT upload `credentials.json` or `token.json` to GitHub.

---

## ▶ Running the Application

### Option 1 – Manual (Recommended for Development)

Terminal 1: uvicorn app.main:app --reload

Terminal 2: python -m app.email_worker

Open in browser: http://127.0.0.1:8000

---

### Option 2 – One Click (Windows)

Double-click: start_ai_mirror.bat

This will:
- Activate virtual environment
- Start FastAPI server
- Start email worker
- Open browser automatically

---

## 🎨 Dashboard Capabilities

- View incoming messages
- See AI-generated drafts
- Select reply tone
- Edit drafts before sending
- Send threaded Gmail replies
- Track status (Pending / Sent / Discarded)

---

## 🔒 Security Notes

Do NOT commit:

- `credentials.json`
- `token.json`
- `data/chroma_db/`
- `data/drafts.json`
- Any API keys

These files should remain ignored via `.gitignore`.

---

## 🧠 Tech Stack

- FastAPI
- Groq (LLaMA 3)
- ChromaDB
- Sentence Transformers
- Gmail API
- Python 3.10+

---

## 🚀 Future Improvements

- Multi-user authentication
- Docker containerization
- Cloud deployment (Render / AWS / GCP)
- React frontend
- Background task queue (Celery)
- Real-time updates via WebSockets

---

## 👤 Author

Built as an experimental AI automation system to simulate a digital communication substitute capable of learning and responding in the user's writing style.

---

## 📜 License

This project is for educational and experimental purposes.
