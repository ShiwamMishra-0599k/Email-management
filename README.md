# AI Email Assistant (FastAPI + Gemini + ChromaDB)

An AI email assistant that reads the latest emails from a Gmail inbox and runs four LLM tasks on each one: sentiment, summary, classification (urgency, intent, topic) and a draft reply. It stores every email in a ChromaDB vector store. When drafting a new reply, it retrieves the most similar past email and uses that email's reply as a tone and style example.

> **Privacy:** this repository contains **no real emails**. The local vector store, notebook outputs and report screenshots from development were removed (history rewritten on 2026-11-08). To try it without a Gmail account, use the fictional emails in `sample_data/`.

## How it works

```
Gmail API (5 latest)
  → profanity check (better-profanity)
  → Gemini 2.5 Flash: sentiment → summary → JSON classification (urgency / intent / topic)
  → embedding (all-MiniLM-L6-v2) → ChromaDB
  → top-1 similar past email → its reply used as a tone example
  → Gemini draft reply
  → auto-reply flag: not urgent and not FYI
```

## Endpoints (`main.py`)

| Method | Path | What it does |
|---|---|---|
| GET | `/process_emails` | Fetches the 5 latest emails, analyses them, stores them and returns draft replies |
| POST | `/send_email` | Sends a reply to a stored email through the Gmail API. Note: it generates a new reply at send time |
| GET | `/get_email_by_id` | Returns one stored email with its labels and draft reply |

`/` redirects to the interactive docs at `/docs`.

## Run it

```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt chromadb sentence-transformers better-profanity
copy .env.example .env   # add GEMINI_API_KEY and ASSISTANT_ORG_NAME
```

**Option A: fictional sample data (no Gmail, no Gemini)**
```powershell
python seed_sample_db.py   # builds ./chroma_store from sample_data/sample_emails.json
python show_db.py          # or open view_in_pandas.ipynb
```

**Option B: your own Gmail**
1. Create an OAuth client (Desktop app) in Google Cloud with the Gmail API enabled.
2. Save it as `credentials.json` in this folder. `credentials.json` and `token.json` are git-ignored, so they are never committed.
3. Run `uvicorn main:app --reload` and open http://127.0.0.1:8000/docs.

Your emails end up in `./chroma_store`, which is also git-ignored. Don't commit it.

## Files

| File | Role |
|---|---|
| `gmail_auth.py`, `extract_emails.py` | OAuth and fetching the latest messages |
| `call_gemini.py` | The four Gemini prompts and JSON parsing |
| `guardrail.py` | Profanity check |
| `generate_embeddings.py`, `ingest_db.py`, `similarity_search.py` | Embeddings, storage, top-1 retrieval |
| `replying_auto_reply.py` | Sending a reply through the Gmail API |
| `seed_sample_db.py`, `sample_data/` | Fictional demo data |
| `show_db.py`, `view_in_pandas.ipynb` | Inspecting the store |

## Limitations (honest list)
- Synchronous and single-user. It processes the 5 latest emails per call.
- Sentiment is stored but not used for routing.
- Retrieval is a top-1 tone example. It does not ground facts.
- Thread and message IDs aren't stored, so sent replies don't thread in Gmail.
- No tests or evaluation set yet.

## License
For educational and demo use. Check the terms of the Gmail API and Gemini API before any real use.
