import pandas as pd
import ast
import json
from pathlib import Path

# ==============================
# PROJECT PATH SETUP
# ==============================

# go from:
# feature_engineering → src → ml-engine
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data/processed/recipes_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/ingredient_vocab.json"

# ==============================
# LOAD DATASET
# ==============================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

# convert string list → python list
df["cleaned_ingredients"] = df["cleaned_ingredients"].apply(ast.literal_eval)

# ==============================
# BUILD VOCABULARY
# ==============================

print("Building vocabulary...")

all_ingredients = set()

for ingredients in df["cleaned_ingredients"]:
    all_ingredients.update(ingredients)

# IMPORTANT:
# create INDEX mapping (ingredient → index)
ingredient_vocab = {
    ing: idx for idx, ing in enumerate(sorted(all_ingredients))
}

# ==============================
# SAVE VOCAB
# ==============================

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_PATH, "w") as f:
    json.dump(ingredient_vocab, f, indent=2)

print("✅ Vocabulary saved at:", OUTPUT_PATH)
print("Total ingredients:", len(ingredient_vocab))