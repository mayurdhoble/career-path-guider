# vector_service.py (converted from Pinecone to Chroma)
from sentence_transformers import SentenceTransformer
from config import Config
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import json
import os

class VectorService:
    def __init__(self):
        # Initialize Chroma client (local persistent DB)
        self.chroma_client = Client(Settings(persist_directory=Config.CHROMA_DB_PATH))

        # Load or create collection
        if Config.COLLECTION_NAME not in [c.name for c in self.chroma_client.list_collections()]:
            self.collection = self.chroma_client.create_collection(
                name=Config.COLLECTION_NAME,
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            )
        else:
            self.collection = self.chroma_client.get_collection(name=Config.COLLECTION_NAME)

        # Used separately for manual encoding (not needed if Chroma handles it)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize with career paths
        self._initialize_career_paths()

    def _initialize_career_paths(self):
        from career_paths import CAREER_PATHS

        ids = []
        documents = []
        metadatas = []

        for path_id, path_data in CAREER_PATHS.items():
            text = f"{path_data['title']} {path_data['description']} {' '.join(path_data['keywords'])}"
            ids.append(f"career_{path_id}")
            documents.append(text)
            metadatas.append({"type": "career_path", "path": path_id, "data": json.dumps(path_data)})

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def find_matching_career(self, user_interests):
        results = self.collection.query(
            query_texts=[user_interests],
            n_results=3
        )

        matches = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            matches.append({
                'path': meta['path'],
                'score': results['distances'][0][i],
                'data': json.loads(meta['data'])
            })

        return matches
