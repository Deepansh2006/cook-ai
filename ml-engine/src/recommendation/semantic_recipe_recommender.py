import numpy as np
import pandas as pd
import ast
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data/processed/recipes_clean.csv"
SEMANTIC_VECTOR_PATH = PROJECT_ROOT / "data/processed/recipe_semantic_vectors.npy"

# -----------------------------
# Load Data
# -----------------------------
print("Loading recipes...")

df = pd.read_csv(DATA_PATH)
df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

recipe_vectors = np.load(SEMANTIC_VECTOR_PATH)

print("Recipes loaded:", len(df))
print("Vector shape:", recipe_vectors.shape)

# -----------------------------
# Load AI Model
# -----------------------------
print("\nLoading Semantic AI model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("✅ Model Ready")

# -----------------------------
# Convert User Query → Vector
# -----------------------------
def encode_query(query):

    embedding = model.encode([query])

    return embedding


# -----------------------------
# Recommend Recipes
# -----------------------------
def recommend_recipes(user_query, top_k=5):

    query_vector = encode_query(user_query)

    similarities = cosine_similarity(query_vector, recipe_vectors)

    top_indices = similarities[0].argsort()[-top_k:][::-1]

    results = df.iloc[top_indices][["Name", "cleaned_ingredients"]]

    return results


# -----------------------------
# Interactive Assistant
# -----------------------------
if __name__ == "__main__":

    while True:

        user_query = input("\nWhat do you want to cook? (type 'exit' to quit)\n")

        if user_query.lower() == "exit":
            break

        recommendations = recommend_recipes(user_query)

        print("\n🔥 Recommended Recipes:\n")

        for _, row in recommendations.iterrows():
            print("Recipe:", row["Name"])
            print("Ingredients:", row["cleaned_ingredients"])
            print("----------------------------")