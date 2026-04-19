# import numpy as np
# import json
# import pandas as pd
# import ast
# from pathlib import Path
# from sklearn.metrics.pairwise import cosine_similarity

# # -----------------------------
# # Project Paths
# # -----------------------------
# PROJECT_ROOT = Path(__file__).resolve().parents[2]

# DATA_PATH = PROJECT_ROOT / "data/processed/recipes_clean.csv"
# VOCAB_PATH = PROJECT_ROOT / "data/processed/ingredient_vocab.json"
# VECTOR_PATH = PROJECT_ROOT / "data/processed/recipe_vectors.npy"

# # -----------------------------
# # Load Files
# # -----------------------------
# print("Loading data...")

# df = pd.read_csv(DATA_PATH)
# df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

# with open(VOCAB_PATH) as f:
#     vocab = json.load(f)

# recipe_vectors = np.load(VECTOR_PATH)

# VOCAB_SIZE = len(vocab)

# print("Recipes loaded:", len(df))
# print("Vocabulary size:", VOCAB_SIZE)


# # -----------------------------
# # Convert User Ingredients → Vector
# # -----------------------------
# def ingredients_to_vector(ingredients):

#     vector = np.zeros(VOCAB_SIZE)

#     for ing in ingredients:
#         if ing in vocab:
#             vector[vocab[ing]] = 1

#     return vector.reshape(1, -1)


# # -----------------------------
# # Recommend Recipes
# # -----------------------------
# def recommend_recipes(user_ingredients, top_k=5):

#     user_vector = ingredients_to_vector(user_ingredients)

#     similarities = cosine_similarity(user_vector, recipe_vectors)

#     top_indices = similarities[0].argsort()[-top_k:][::-1]

#     results = df.iloc[top_indices][["Name", "cleaned_ingredients"]]

#     return results


# # -----------------------------
# # Test Example
# # -----------------------------
# if __name__ == "__main__":

#     user_input = ["bread", "capsicum", "paneer"]

#     recommendations = recommend_recipes(user_input)

#     print("\nRecommended Recipes:\n")
#     print("\nRecommended Recipes:\n")

# for i, row in recommendations.iterrows():
#     print("Recipe:", row["Name"])
#     print("Ingredients:", row["cleaned_ingredients"])
#     print("----------------------------")






import numpy as np
import json
import pandas as pd
import ast
import re
import pickle
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz

# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data/processed/recipes_clean.csv"
VOCAB_PATH = PROJECT_ROOT / "data/processed/ingredient_vocab.json"
VECTOR_PATH = PROJECT_ROOT / "data/processed/recipe_vectors.npy"
TFIDF_PATH = PROJECT_ROOT / "data/processed/tfidf_vectorizer.pkl"

# -----------------------------
# Load Files
# -----------------------------
print("Loading data...")

df = pd.read_csv(DATA_PATH)
df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

with open(VOCAB_PATH) as f:
    vocab = json.load(f)

recipe_vectors = np.load(VECTOR_PATH)

with open(TFIDF_PATH, "rb") as f:
    vectorizer = pickle.load(f)

VOCAB_LIST = list(vocab.keys())
VOCAB_SET = set(VOCAB_LIST)

print("Recipes loaded:", len(df))
print("Vector size:", recipe_vectors.shape[1])

# -----------------------------
# Extract Ingredients from Sentence
# -----------------------------
def extract_ingredients(user_input, threshold=80):

    user_input = user_input.lower()

    # remove punctuation
    user_input = re.sub(r"[^a-zA-Z\s]", " ", user_input)

    tokens = user_input.split()

    detected = set()

    for token in tokens:

        match, score, _ = process.extractOne(
            token,
            VOCAB_LIST,
            scorer=fuzz.partial_ratio
        )

        if score >= threshold:
            detected.add(match)

    return list(detected)

# -----------------------------
# Convert Ingredients → TFIDF Vector
# -----------------------------
def ingredients_to_vector(ingredients):

    text = " ".join(ingredients)

    vector = vectorizer.transform([text]).toarray()

    return vector

# -----------------------------
# Recommend Recipes
# -----------------------------
def recommend_recipes(user_ingredients, top_k=5):

    user_vector = ingredients_to_vector(user_ingredients)

    similarities = cosine_similarity(user_vector, recipe_vectors)

    top_indices = similarities[0].argsort()[-top_k:][::-1]

    results = df.iloc[top_indices][["Name", "cleaned_ingredients"]]

    return results

# -----------------------------
# Interactive Assistant
# -----------------------------
if __name__ == "__main__":

    sentence = input("\nWhat ingredients do you have?\n")

    user_ingredients = extract_ingredients(sentence)

    if len(user_ingredients) == 0:
        print("\nNo ingredients detected. Try mentioning food items.")
        exit()

    print("\nDetected ingredients:", user_ingredients)

    recommendations = recommend_recipes(user_ingredients)

    print("\nRecommended Recipes:\n")

    for i, row in recommendations.iterrows():

        print("Recipe:", row["Name"])
        print("Ingredients:", row["cleaned_ingredients"])
        print("----------------------------")