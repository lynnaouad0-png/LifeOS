import uuid
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from fastembed import TextEmbedding

# --- CONFIGURATION INITIALIZATION ---
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "user_memories"

class MemoryService:
    def __init__(self):
        """Initialize connection to Qdrant vector storage and load multilingual E5 via ONNX."""
        self.qdrant_client = QdrantClient(url=QDRANT_URL)
        
        print("🔄 Loading Multilingual-E5-Large text embedding weights via FastEmbed...")
        self.encoder = TextEmbedding(model_name="intfloat/multilingual-e5-large")
        
        # Self-healing database check: Ensure the collection exists in Qdrant
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Verifies collection exists with E5-Large dimensions (1024), or auto-creates it."""
        try:
            if not self.qdrant_client.collection_exists(collection_name=COLLECTION_NAME):
                self.qdrant_client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
                )
                print(f"✅ Created unified vector collection: '{COLLECTION_NAME}'")
        except Exception as e:
            print(f"⚠️ Vector database collection initialization failure: {e}")

    def create_memory_embedding(self, text: str) -> list:
        """Generates a dense vector embedding using FastEmbed for semantic vector queries."""
        formatted_text = f"passage: {text}"
        embeddings_generator = self.encoder.embed([formatted_text])
        embedding = next(embeddings_generator)
        return embedding.tolist()

    def save_memory(self, user_id: str, content: str, source_category: str, metadata: dict = None) -> str:
        """Saves contextual events into the storage cluster."""
        memory_uuid = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        vector = self.create_memory_embedding(content)
        
        payload = {
            "memory_id": memory_uuid,
            "user_id": user_id,
            "content": content,
            "source_category": source_category,
            "created_at": timestamp,
            **(metadata or {})
        }
        
        self.qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=memory_uuid,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        
        return memory_uuid

    def retrieve_relevant_memories(self, user_id: str, query: str, limit: int = 3) -> list:
        """Performs vector similarity lookup to retrieve context-relevant memory logs."""
        query_vector = self.create_memory_embedding(f"query: {query}")
        
        user_isolation_filter = Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        )
        
        # FIX: Swapped out deprecated .search() for the modern .query_points() API endpoint
        search_results = self.qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=user_isolation_filter,
            limit=limit
        ).points
        
        extracted_memories = []
        for point in search_results:
            extracted_memories.append({
                "content": point.payload.get("content"),
                "category": point.payload.get("source_category"),
                "date": point.payload.get("created_at"),
                "similarity_score": round(point.score, 4)
            })
            
        return extracted_memories

# --- VERIFICATION TEST DRIVE RUNNER ---
if __name__ == "__main__":
    print("🚀 Initializing standalone Memory Service sanity test run...")
    test_user = "b2156f03-4753-484e-abad-ced4371ebfb5"
    memory_engine = MemoryService()
    
    print("\n🧠 Ingesting lifestyle memory patterns...")
    memory_engine.save_memory(
        user_id=test_user,
        content="User prefers code deep-dives late in the morning and playing classical violin pieces (Bach, Sibelius) to wind down in the evening.",
        source_category="reflection"
    )
    
    search_prompt = "What musical instruments or composers do I resonate with?"
    print(f"\n🔍 Searching vector index space for query: '{search_prompt}'")
    
    hits = memory_engine.retrieve_relevant_memories(user_id=test_user, query=search_prompt)
    for index, hit in enumerate(hits, 1):
        print(f"  [{index}] Match Score: {hit['similarity_score']} | Context: {hit['content']}")