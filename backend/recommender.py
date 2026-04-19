from pathlib import Path
import os
import numpy as np
import pandas as pd
import ast
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# Setup paths
# =========================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "recipes_clean.csv"
VECTOR_PATH = DATA_DIR / "recipe_semantic_vectors.npy"

# =========================
# Google Drive Direct Links
# =========================
CSV_URL = "https://drive.google.com/uc?export=download&id=1iABSCjilIiRiAru9SuhJeYvkdNPpI0Yh"
VECTOR_URL = "https://drive.google.com/uc?export=download&id=13XVO-W3M_W_DJZUznReqlJO3nkhREvSY"

# =========================
# Download helper
# =========================
def download_file(url, path):
    if not path.exists():
        print(f"Downloading {path.name}...")
        response = requests.get(url)
        with open(path, "wb") as f:
            f.write(response.content)

# =========================
# Download data if missing
# =========================
download_file(CSV_URL, CSV_PATH)
download_file(VECTOR_URL, VECTOR_PATH)

# =========================
# Load data + model
# =========================
print("Loading ML model...")

df = pd.read_csv(CSV_PATH)
df['cleaned_ingredients'] = df['cleaned_ingredients'].apply(ast.literal_eval)

recipe_vectors = np.load(VECTOR_PATH)

# Load model ONCE (global)
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Model loaded successfully")

# =========================
# Recommendation function
# =========================
def recommend(query, top_k=5):
    query_vec = model.encode([query])
    similarities = cosine_similarity(query_vec, recipe_vectors)

    top_indices = similarities[0].argsort()[-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "recipe": df.iloc[idx]["Name"],
            "ingredients": df.iloc[idx]["cleaned_ingredients"]
        })

    return results