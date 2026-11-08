"""Build a local ChromaDB store from the fictional sample emails.

Lets you try the store, `show_db.py`, `view_in_pandas.ipynb` and the similarity
search without connecting a real Gmail account or calling Gemini.
The labels below are placeholders set by hand, not model output.

Run:  python seed_sample_db.py
"""

import json
from pathlib import Path

from generate_embeddings import create_embedding
from guardrail import check_profanity_in_email
from ingest_db import collection, ingest_data

SAMPLES = Path(__file__).with_name("sample_data") / "sample_emails.json"


def main() -> None:
    emails = json.loads(SAMPLES.read_text(encoding="utf-8"))["emails"]
    existing = set(collection.get()["ids"])
    added = 0
    for e in emails:
        if e["email_id"] in existing:
            continue
        flag, profane_word = check_profanity_in_email(e["body"])
        ingest_data(
            sender=e["sender"],
            subject=e["subject"],
            summary="(sample: not summarised)",
            urgency="normal",
            intent="FYI",
            topic="sample",
            auto_reply="false",
            ai_reply="",
            sentiment="(sample)",
            flag=flag,
            profane_word=profane_word or "",
            email_id=e["email_id"],
            embedding=[create_embedding(e["body"])],
            body=e["body"],
        )
        added += 1
    print(f"Added {added} sample emails to ./chroma_store ({len(emails)} in the file).")


if __name__ == "__main__":
    main()
