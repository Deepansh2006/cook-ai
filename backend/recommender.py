from pathlib import Path
import numpy as np
import pandas as pd
import ast
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'ml-engine' / 'data' / 'processed' / 'recipes_clean.csv'
VECTOR_PATH = ROOT / 'ml-engine' / 'data' / 'processed' / 'recipe_semantic_vectors.npy'

print('Loading ML model...')

df = pd.read_csv(DATA_PATH)
df['cleaned_ingredients'] = df['cleaned_ingredients'].apply(ast.literal_eval)
recipe_vectors = np.load(VECTOR_PATH)
model = SentenceTransformer('all-MiniLM-L6-v2')

print('Model loaded successfully')


def recommend(query, top_k=5):
    query_vec = model.encode([query])
    similarities = cosine_similarity(query_vec, recipe_vectors)
    top_indices = similarities[0].argsort()[-top_k:][::-1]
    results = []
    for idx in top_indices:
        results.append({
            'recipe': df.iloc[idx]['Name'],
            'ingredients': df.iloc[idx]['cleaned_ingredients'],
        })
    return results
