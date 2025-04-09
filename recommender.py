import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from scraper import SHLScraper

class SHLRecommender:
    def __init__(self):
        self.scraper = SHLScraper()
        self.df = self.scraper.get_assessments()
        
        # Convert duration to minutes
        self.df['duration_mins'] = self.df['duration'].apply(
            lambda x: int(re.search(r'\d+', str(x)).group()) if pd.notnull(x) else 0
        )
        
        # Configure vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Prepare search text
        self.texts = self.df['name'] + ' ' + self.df['test_type']
        self.vectors = self.vectorizer.fit_transform(self.texts)

    def recommend(self, query, top_k=3):
        try:
            query = query.lower()
            
            # 1. Handle special cases first
            if 'javascript' in query:
                filtered = self.df[self.df['name'].str.contains('JavaScript', case=False)]
            elif 'java' in query and 'script' not in query:
                filtered = self.df[self.df['name'].str.contains('Java', case=False) & 
                          ~self.df['name'].str.contains('JavaScript', case=False)]
            elif 'cognitive' in query or 'personality' in query:
                filtered = self.df[self.df['test_type'] == 'Psychometric']
            elif 'python' in query or 'sql' in query:
                filtered = self.df[self.df['test_type'] == 'Technical']
            elif 'screen' in query or 'jd' in query:
                filtered = self.df[self.df['name'].str.contains('Quick|Screen', case=False)]
            else:
                filtered = self.df.copy()
            
            # 2. Filter by duration
            duration_match = re.search(r'(\d+)\s*min', query)
            if duration_match:
                max_duration = int(duration_match.group(1))
                filtered = filtered[filtered['duration_mins'] <= max_duration]
            
            # 3. If no special case matched, use similarity
            if len(filtered) == len(self.df):
                query_vec = self.vectorizer.transform([query])
                vectors = self.vectorizer.transform(filtered['name'] + ' ' + filtered['test_type'])
                similarities = cosine_similarity(query_vec, vectors).flatten()
                filtered['similarity'] = similarities
                filtered = filtered[filtered['similarity'] > 0.2]
                filtered = filtered.sort_values('similarity', ascending=False)
            
            # 4. Fallback to fastest tests if empty
            if len(filtered) == 0:
                if duration_match:
                    return self.df[self.df['duration_mins'] <= max_duration].sort_values('duration_mins').head(top_k).to_dict('records')
                return self.df.sort_values('duration_mins').head(top_k).to_dict('records')
            
            return filtered.head(top_k).to_dict('records')
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return self.df.sort_values('duration_mins').head(top_k).to_dict('records')