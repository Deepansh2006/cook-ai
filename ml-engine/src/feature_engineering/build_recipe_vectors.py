# import pandas as pd
# import json
# import numpy as np
# import ast
# from pathlib import Path

# # -------------------------------
# # Project Paths
# # -------------------------------
# PROJECT_ROOT = Path(__file__).resolve().parents[2]

# DATA_PATH = PROJECT_ROOT / "data/processed/recipes_clean.csv"
# VOCAB_PATH = PROJECT_ROOT / "data/processed/ingredient_vocab.json"
# OUTPUT_PATH = PROJECT_ROOT / "data/processed/recipe_vectors.npy"

# print("Loading data...")

# # -------------------------------
# # Load Dataset
# # -------------------------------
# df = pd.read_csv(DATA_PATH)

# # convert string list → python list
# df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

# # -------------------------------
# # Load Vocabulary
# # -------------------------------
# with open(VOCAB_PATH, "r") as f:
#     vocab = json.load(f)

# VOCAB_SIZE = len(vocab)

# print("Vocabulary size:", VOCAB_SIZE)
# print("Creating recipe vectors...")

# # -------------------------------
# # Recipe → Vector Function
# # -------------------------------
# def recipe_to_vector(ingredients):
#     vector = np.zeros(VOCAB_SIZE, dtype=np.int8)

#     for ing in ingredients:
#         if ing in vocab:          # ✅ safety check (IMPORTANT)
#             vector[vocab[ing]] = 1

#     return vector


# # -------------------------------
# # Create All Recipe Vectors
# # -------------------------------
# recipe_vectors = np.array([
#     recipe_to_vector(ings)
#     for ings in df["cleaned_ingredients"]
# ])

# # -------------------------------
# # Save Vectors
# # -------------------------------
# np.save(OUTPUT_PATH, recipe_vectors)

# print("✅ Recipe vectors saved at:", OUTPUT_PATH)
# print("Shape:", recipe_vectors.shape)






import pandas as pd
import numpy as np
import ast
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# -----------------------------
# Project paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data/processed/recipes_clean.csv"
VECTORS_PATH = PROJECT_ROOT / "data/processed/recipe_vectors.npy"
VECTORIZER_PATH = PROJECT_ROOT / "data/processed/tfidf_vectorizer.pkl"

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

# convert string list → python list
df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

print("Preparing ingredient text...")

# convert list → text
df["ingredient_text"] = df["cleaned_ingredients"].apply(lambda x: " ".join(x))

# -----------------------------
# TF-IDF Vectorization
# -----------------------------
print("Creating TF-IDF vectors...")

vectorizer = TfidfVectorizer()

recipe_vectors = vectorizer.fit_transform(df["ingredient_text"])

print("Saving vectors...")

np.save(VECTORS_PATH, recipe_vectors.toarray())

# save vectorizer (VERY IMPORTANT)
with open(VECTORIZER_PATH, "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ TF-IDF vectors saved")
print("Shape:", recipe_vectors.shape)