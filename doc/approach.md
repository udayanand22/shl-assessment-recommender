# SHL Assessment Recommender – Solution Summary

## 🧩 Problem Statement
Build a SHL Assessment Recommendation Engine using SHL's product catalogue.

## 🔍 Approach
- Scraped SHL assessment data and cleaned it.
- Used `all-MiniLM-L6-v2` from Sentence Transformers to generate embeddings.
- Calculated cosine similarity between user input and assessment vectors.
- Returned the top-k most similar assessments.

## ⚙️ Tech Stack
- Python
- SentenceTransformers
- FastAPI
- Pandas & Scikit-learn

## 🌐 API Endpoint
POST `/recommend`  
Accepts: `{"text": "<query>", "top_k": <int>}`  
Returns: Top-k JSON recommendations.

## 📦 Repo
[GitHub – SHL Recommender](https://github.com/udayanand22/shl-assessment-recommender)

## 🚀 Hosted on
[Hugging Face Space](https://huggingface.co/spaces/udayanand/shlrecommendation)
