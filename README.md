# 🧠 AI-Powered Email Assistant with Generative AI

An end-to-end intelligent email assistant built using FastAPI, Google Gemini (Generative AI), ChromaDB, and Gmail API. This system can fetch, analyze, classify, and auto-reply to emails using LLMs with Retrieval-Augmented Generation (RAG), sentiment analysis, and profanity filtering.

---

## 🚀 Features

- 📥 Fetch top 5 emails using Gmail API
- 🧠 Summarize and classify emails (urgency, intent, topic)
- 🔍 Detect sentiment and profanity
- 🧬 Generate embeddings and store in ChromaDB
- 🗃️ Retrieve relevant past emails using vector search (RAG)
- ✍️ Generate smart replies with Gemini and contextual memory
- 📡 FastAPI endpoints for email processing, reply generation, and querying

---

## 🧰 Tech Stack

| Layer              | Tech Used |
|--------------------|-----------|
| **Backend**        | FastAPI, Uvicorn |
| **LLM**            | Google Gemini (`google-generativeai`) |
| **Vector DB**      | ChromaDB (`chromadb.PersistentClient`) |
| **Embeddings**     | SentenceTransformer (`all-MiniLM-L6-v2`) |
| **Email API**      | Gmail API with OAuth |
| **Filtering**      | `better-profanity`, `vaderSentiment` |
| **Data Handling**  | Pandas, DuckDB |
| **Environment**    | Python, dotenv |

---

## 🧠 AI Capabilities

- **Summarization**: Condenses email body while preserving meaning.
- **Classification**:
  - Urgency: `urgent`, `normal`, `low`
  - Intent: `meeting_request`, `action_required`, `notification`, `FYI`
  - Topic: `security`, `events`, `project`, `personal`
- **Sentiment**: Detects tone (`positive`, `neutral`, `negative`)
- **Profanity Check**: Flags offensive content before reply
- **Auto-Reply**: Uses Gemini with RAG to generate context-aware replies

---

## 🗂️ Architecture

[ Gmail API ]
↓
[ Extraction Layer ]
↓
[ NLP Pipeline ]
├─ Summarize
├─ Classify
├─ Sentiment
└─ Profanity Filter
↓
[ Embeddings + Metadata → ChromaDB ]
↓
[ RAG: Similarity Search ]
↓
[ Gemini Response Generator ]
↓
[ FastAPI Endpoints ]


---

## 🧾 FastAPI Endpoints

| Endpoint              | Description |
|-----------------------|-------------|
| `/process_emails`     | Fetch and process latest 5 emails |
| `/send_email`         | Send AI-generated reply |
| `/get_email_by_id`    | Retrieve stored email data |
| `/summarize`          | Summarize a specific email |
| `/classify`           | Classify a specific email |
| `/sentiment`          | Get sentiment of a specific email |

---

## 🔁 Auto-Reply Logic

| Urgency | Intent         | Topic     | Action           |
|---------|----------------|-----------|------------------|
| urgent  | any            | any       | `manual_review`  |
| normal  | meeting_request| any       | `auto_reply`     |
| normal  | notification   | events    | `auto_reply`     |
| normal  | FYI            | any       | `no_reply_needed`|
| low     | notification   | any       | `no_reply_needed`|
| low     | action_required| personal  | `optional_reply` |

---

## 📦 ChromaDB Field Mapping

| Field           | Type      |
|------------------|-----------|
| `body`           | document  |
| `embedding`      | embedding |
| `metadata`       | id, subject, summary, sender, recipient, timestamp, message_thread_id, labels, urgency, intent, topic, auto_reply_flag, manual_review_flag, ai_response, reply_sent, user_feedback |

---

## 📋 Requirements

See `requirements.txt`:

```txt
fastapi==0.110.0
uvicorn[standard]==0.29.0
google-api-python-client==2.126.0
google-auth==2.29.0
google-auth-oauthlib==1.2.0
google-generativeai==0.5.2
psycopg2-binary==2.9.9
pgvector==0.2.4
SQLAlchemy==2.0.30
python-dotenv==1.0.1
vaderSentiment==3.3.2
requests==2.32.3
chromadb
duckdb
pandas
sentence-transformers
better-profanity

🧪 Models Used
✅ Successfully Integrated:

-Google Gemini

-SentenceTransformer (all-MiniLM-L6-v2)

-VADER Sentiment

-better-profanity

❌ Not Used / Dropped:

-DistilBERT (too slow for real-time)

-OpenAI embeddings (avoided API-mixing)

-Rule-based classification

🛡️ Ethics & Safeguards
⚠️ Profanity Filter: Prevents offensive replies

🧠 Manual Review Flags: For urgent or security-related mails

🛑 No Hallucination Rule: Gemini is instructed not to fabricate

🚧 Known Challenges
-Embedding type mismatches

-Windows-specific ChromaDB locks

-Prompt tuning for Gemini hallucinations

-State management between FastAPI endpoints

📈 Future Enhancements
🔐 Add user authentication

📬 Integrate with Outlook (Microsoft Graph API)

🧠 Migrate memory to PostgreSQL + pgvector for scale

🗣️ Add feedback loop for AI replies

📊 Extend classification (e.g., billing, HR, sales)

📌 License
This project is for educational and demo purposes. For enterprise use, consult licensing of third-party APIs (e.g., Google Gemini, Gmail API).

🤝 Contributions
Pull requests and discussions are welcome! Feel free to fork and adapt for enterprise use cases like CRM automation or virtual email assistants.

