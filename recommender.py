import json
import cohere
import os
from scraper import SHLScraper
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load API key
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

class SHLRecommender:
    def __init__(self):
        self.scraper = SHLScraper()
        self.assessments = []
        self.embeddings = None
        self.cohere = cohere.Client(COHERE_API_KEY)

    def load_or_scrape(self, filename='shl_assessments.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.assessments = json.load(f)
            print(f"✅ Loaded {len(self.assessments)} assessments from file.")
        except FileNotFoundError:
            print("🔄 File not found. Scraping data...")
            self.assessments = self.scraper.scrape_all()
            self.scraper.save_to_json(self.assessments, filename)

        if len(self.assessments) == 0:
            print("⚠️ No assessments were loaded or scraped.")
            return
        
        print(f"Loaded assessments (first 3): {self.assessments[:3]}")  # Show first 3 for debugging

    def embed_assessments(self):
        if not self.assessments:
            print("⚠️ No assessments available to embed.")
            return

        texts = [a['name'] + " " + a.get('description', '') for a in self.assessments]
        print("🔢 Generating embeddings for assessments...")
        response = self.cohere.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        self.embeddings = np.array(response.embeddings)
        print(f"✅ Embeddings generated. Number of embeddings: {len(self.embeddings)}")

    def recommend(self, user_query, top_k=5):
        print(f"\n🔍 Searching for assessments similar to: {user_query}")

        if not self.assessments:
            print("⚠️ No assessments loaded.")
            return []

        query_embedding = self.cohere.embed(
            texts=[user_query],
            model="embed-english-v3.0",
            input_type="search_query"
        ).embeddings[0]
        query_embedding = np.array(query_embedding).reshape(1, -1)

        similarities = cosine_similarity(query_embedding, self.embeddings)[0]

        # Debug: Print all similarity scores
        print("\n📊 Similarity Scores:")
        for i, score in enumerate(similarities):
            if i < len(self.assessments):  # Ensure index is within bounds
                print(f"{self.assessments[i]['name'][:40]:40} → Score: {round(score, 4)}")

        top_indices = similarities.argsort()[-top_k:][::-1]

        recommendations = []
        for idx in top_indices:
            score = similarities[idx]
            if score < 0.2:  # Optional threshold filter
                continue
            item = self.assessments[idx]
            recommendations.append({
                "name": item['name'],
                "description": item.get('description', 'N/A'),
                "url": item['url'],
                "score": round(score, 3)
            })

        if not recommendations:
            print("⚠️ No strong matches found for the query.")

        return recommendations


# Singleton instance (for API reuse)
_recommender_instance = SHLRecommender()
_recommender_instance.load_or_scrape()
_recommender_instance.embed_assessments()

def recommend_assessments(query: str, top_k: int = 5):
    return _recommender_instance.recommend(query, top_k=top_k)

# Optional: interactive CLI
if __name__ == '__main__':
    while True:
        query = input("\n🧠 Enter a job role or skill you're hiring for (or 'exit'): ").strip()
        if query.lower() == 'exit':
            break
        results = recommend_assessments(query)
        for i, r in enumerate(results, 1):
            print(f"\n🔹 Recommendation #{i}")
            print(f"Name       : {r['name']}")
            print(f"Score      : {r['score']}")
            print(f"Description: {r['description']}")
            print(f"Link       : {r['url']}")
