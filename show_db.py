import chromadb

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(name="email_data")


# Fetch all records
results = collection.get(include=['metadatas', 'documents', 'embeddings'])

# Display the data
for i in range(len(results["ids"])):
    metadata = results['metadatas'][i]
    
    print(f"\n📨 Email ID: {results['ids'][i]}")
    print(f"👤 Sender: {metadata.get('sender')}")
    print(f"📬 Subject: {metadata.get('subject')}")
    print(f"📝 Summary: {metadata.get('summary')}")
    print(f"⚡ Urgency: {metadata.get('urgency')}")
    print(f"🎯 Intent: {metadata.get('intent')}")
    print(f"🏷️ Topic: {metadata.get('topic')}")
    print(f"🤖 Auto Reply: {metadata.get('auto_reply')}")
    print(f"💬 AI Reply: {metadata.get('ai_reply')}")
    print(f"📈 Sentiment: {metadata.get('sentiment')}")
    print(f"📄 Document (body): {results['documents'][i][:150]}...") 
    print(f"🔍 Embedding: {results['embeddings'][i][:10]}...") 
