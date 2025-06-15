from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from config import Config
import json

class VectorService:
    def __init__(self):
        # Updated Pinecone v5+ initialization
        self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        
        # Create index if doesn't exist
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        if Config.INDEX_NAME not in existing_indexes:
            self.pc.create_index(
                name=Config.INDEX_NAME,
                dimension=384,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='gcp-starter')
            )
        
        self.index = self.pc.Index(Config.INDEX_NAME)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize with career paths
        self._initialize_career_paths()
    
    def _initialize_career_paths(self):
        from career_paths import CAREER_PATHS
        
        for path_id, path_data in CAREER_PATHS.items():
            text = f"{path_data['title']} {path_data['description']} {' '.join(path_data['keywords'])}"
            embedding = self.encoder.encode(text).tolist()
            
            self.index.upsert([(
                f"career_{path_id}",
                embedding,
                {"type": "career_path", "path": path_id, "data": json.dumps(path_data)}
            )])
    
    def find_matching_career(self, user_interests):
        embedding = self.encoder.encode(user_interests).tolist()
        results = self.index.query(embedding, top_k=3, include_metadata=True)
        
        matches = []
        for match in results['matches']:
            if match['metadata']['type'] == 'career_path':
                matches.append({
                    'path': match['metadata']['path'],
                    'score': match['score'],
                    'data': json.loads(match['metadata']['data'])
                })
        
        return matches
