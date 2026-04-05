import chromadb
client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(name="email_data")



def ingest_data(sender, subject, summary, urgency, intent, topic, auto_reply, ai_reply, sentiment, flag, profane_word, email_id, embedding, body):
    collection.add(
        documents=[body], 
        metadatas=[{
            "sender": sender,
            "subject": subject,
            "summary": summary,
            "urgency": urgency,
            "intent": intent,
            "topic": topic,
            "auto_reply": auto_reply,
            "ai_reply": ai_reply,
            "sentiment": sentiment,
            "flag": flag,
            "profane_word": profane_word
        }],
        ids=[email_id],
        embeddings=embedding
    )

