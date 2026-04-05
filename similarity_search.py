import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

def retrieve_similar_reply(query_body, top_k=1):
    from generate_embeddings import create_embedding 
    query_embedding = create_embedding(query_body)

    client = chromadb.PersistentClient(path="./chroma_store")
    collection = client.get_or_create_collection(name="email_data")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['metadatas', 'documents']
    )

    if results and results['metadatas'][0]:
        similar_metadata = results['metadatas'][0][0]
        similar_document = results['documents'][0][0]
        context_reply = similar_metadata.get("ai_reply", "")
        return context_reply, similar_document

    return "", ""  # No match found
