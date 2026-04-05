from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from extract_emails import get_full_email_content
from call_gemini import summarize_email_text, classify_email, generate_ai_reply_from_body, get_sentiment_from_email
from generate_embeddings import create_embedding
from ingest_db import ingest_data
from replying_auto_reply import send_email_reply
from similarity_search import retrieve_similar_reply
from chromadb import PersistentClient

from guardrail import check_profanity_in_email

app = FastAPI()



class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str
    email_id: str
    thread_id: Optional[str] = None
    message_id: Optional[str] = None

class EmailIDRequest(BaseModel):
    email_id: str



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/process_emails")
def process_emails():
    top_5_emails = get_full_email_content()
    responses = []

    for email in top_5_emails:
        sender = email['from']
        subject = email['subject']
        body = email['body']
        email_id = email['email_id']
        thread_id = email['thread_id']
        message_id = email['message_id']

        flag, profane_word = check_profanity_in_email(body)
        sentiment = get_sentiment_from_email(body)
        embedding = create_embedding(body)
        summary = summarize_email_text(body)
        classification = classify_email(summary)

        urgency = classification['urgency']
        intent = classification['intent']
        topic = classification['topic']
        auto_reply = (urgency != 'urgent') and (intent != 'FYI')

        context_reply, _ = retrieve_similar_reply(body)
        ai_reply = generate_ai_reply_from_body(body, sender, context_reply)

        ingest_data(
            sender=sender,
            subject=subject,
            summary=summary,
            urgency=urgency,
            intent=intent,
            topic=topic,
            auto_reply=str(auto_reply).lower(),
            ai_reply=ai_reply,
            sentiment=sentiment,
            flag=flag,
            profane_word=profane_word,
            email_id=email_id,
            embedding=embedding,
            body=body
        )
        print(f"Processed email from {sender} with email ID {email_id}")

        responses.append({
            "email_id": email_id,
            "sender": sender,
            "subject": subject,
            "summary": summary,
            "urgency": urgency,
            "intent": intent,
            "topic": topic,
            "sentiment": sentiment,
            "flag": flag,
            "profane_word": profane_word,
            "rag_context": context_reply,
            "ai_reply": ai_reply,
            "auto_reply": auto_reply
        })

    return {"processed_emails": responses}


@app.post("/send_email")
def send_ai_reply_by_id(request: EmailIDRequest):
    email_id = request.email_id

    client = PersistentClient(path="./chroma_store")
    collection = client.get_collection(name="email_data")

    # Retrieve stored data
    result = collection.get(ids=[email_id], include=["metadatas", "documents"])
    if not result["ids"]:
        raise HTTPException(status_code=404, detail="Email not found")

    metadata = result["metadatas"][0]
    body = result["documents"][0]

    sender = metadata["sender"]
    subject = metadata["subject"]
    thread_id = metadata.get("thread_id")
    message_id = metadata.get("message_id")

    # Generate reply
    ai_reply = generate_ai_reply_from_body(body, sender)

    # Send reply
    send_email_reply(
        receiver_email=sender,
        subject=subject,
        reply_body=ai_reply,
        thread_id=thread_id,
        message_id=message_id
    )

    return {
        "message": f"Reply sent to {sender}",
        "reply": ai_reply
    }



@app.get("/get_email_by_id")
def get_email_by_id(email_id: str):
    client = PersistentClient(path="./chroma_store")
    collection = client.get_collection(name="email_data")
    result = collection.get(ids=[email_id], include=["metadatas", "documents"])
    if result["ids"]:
        metadata = result["metadatas"][0]
        return {
            "email_id": email_id,
            "sender": metadata.get("sender"),
            "subject": metadata.get("subject"),
            "summary": metadata.get("summary"),
            "urgency": metadata.get("urgency"),
            "intent": metadata.get("intent"),
            "topic": metadata.get("topic"),
            "sentiment": metadata.get("sentiment"),
            "contains_profanity": metadata.get("contains_profanity"),
            "profane_word": metadata.get("profane_word"),
            "ai_reply": metadata.get("ai_reply"),
            "auto_reply": metadata.get("auto_reply"),
            "document": result["documents"][0]
        }
    raise HTTPException(status_code=404, detail="Email not found")
