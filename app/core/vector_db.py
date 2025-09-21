# File: app/core/vector_db.py
import os
from pinecone import Pinecone, ServerlessSpec

# It's best practice to use environment variables for keys
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "YOUR_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "YOUR_ENVIRONMENT")
INDEX_NAME = "resume-matcher"

pinecone = Pinecone(api_key=PINECONE_API_KEY)

def get_pinecone_index():
    if INDEX_NAME not in pinecone.list_indexes().names():
        # Create a new index if it doesn't exist.
        # The vector dimension for 'all-MiniLM-L6-v2' is 384.
        pinecone.create_index(
            name=INDEX_NAME,
            dimension=384, 
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-west-2')
        )
    return pinecone.Index(INDEX_NAME)

index = get_pinecone_index()