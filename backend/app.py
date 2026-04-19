from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import ast
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# -----------------------------
# Load model and data once
# -----------------------------

print("Loading ML model...")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "ml-engine/data/processed/recipes_clean.csv"
VECTOR_PATH = PROJECT_ROOT / "ml-engine/data/processed/recipe_semantic_vectors.npy"

df = pd.read_csv(DATA_PATH)
df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

recipe_vectors = np.load(VECTOR_PATH)

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully")

# -----------------------------
# Recommendation function
# -----------------------------

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


# -----------------------------
# API Endpoint
# -----------------------------

@app.route("/recommend", methods=["POST"])
def recommend_api():

    data = request.json

    query = data.get("query")

    recommendations = recommend(query)

    return jsonify({
        "query": query,
        "recommendations": recommendations
    })


# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)