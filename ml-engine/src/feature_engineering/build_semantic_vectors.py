import pandas as pd
import ast
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data/processed/recipes_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/recipe_semantic_vectors.npy"

print("Loading recipes...")

df = pd.read_csv(DATA_PATH)
df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

# -----------------------------
# Load AI model
# -----------------------------
print("Loading semantic model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Create recipe texts
# -----------------------------
print("Preparing recipe text...")

recipe_texts = []

for _, row in df.iterrows():
    text = row["Name"] + " " + " ".join(row["cleaned_ingredients"])
    recipe_texts.append(text)

# -----------------------------
# Generate embeddings
# -----------------------------
print("Generating embeddings (may take few minutes)...")

embeddings = model.encode(
    recipe_texts,
    batch_size=64,
    show_progress_bar=True
)

# -----------------------------
# Save
# -----------------------------
np.save(OUTPUT_PATH, embeddings)

print("✅ Semantic vectors saved!")
print("Shape:", embeddings.shape)