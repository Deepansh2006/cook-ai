# 🍳 Cook-AI — Intelligent Recipe Recommendation System

An AI-powered recipe recommendation system that suggests recipes based on user-provided ingredients using **Natural Language Processing (NLP)** and **semantic similarity**.

---

## 🚀 Overview

Cook-AI allows users to input ingredients in natural language (e.g., *"I have paneer, bread, and capsicum"*) and returns the most relevant recipes.

This project demonstrates a **complete Machine Learning pipeline**, from data preprocessing to deployment via a Flask API.

---

## 🧠 What I Learned

Through this project, I gained hands-on experience in:

* Data preprocessing & cleaning
* NLP techniques for text normalization
* Feature engineering (TF-IDF & embeddings)
* Semantic search using vector similarity
* Building end-to-end ML pipelines
* Backend integration using Flask

---

## ⚙️ Tech Stack

* **Python**
* **Pandas, NumPy**
* **Scikit-learn**
* **Sentence Transformers (BERT-based embeddings)**
* **RapidFuzz (fuzzy matching)**
* **Flask (API backend)**

---

## 🏗️ ML Pipeline (Step-by-Step)

### 1️⃣ Data Preprocessing

* Loaded dataset using `pandas`
* Cleaned ingredient lists using:

  * `ast.literal_eval` (convert string → list)
* Normalized text:

  * Lowercasing
  * Removing special characters
  * Tokenization

---

### 2️⃣ Ingredient Normalization

* Built a **vocabulary of ingredients**
* Applied fuzzy matching using:

  * `RapidFuzz (partial_ratio)`
* Handled:

  * typos (e.g., *capsicm → capsicum*)
  * variations (e.g., *paneer vs cottage cheese*)

---

### 3️⃣ Feature Engineering

#### 🔹 TF-IDF Vectorization

* Used `TfidfVectorizer`
* Converted ingredient text → numerical vectors
* Captures importance of ingredients

#### 🔹 Semantic Embeddings (Advanced)

* Used:

  ```python
  SentenceTransformer("all-MiniLM-L6-v2")
  ```
* Converts recipes into **dense semantic vectors**
* Captures meaning, not just keywords

---

### 4️⃣ Vector Storage

* Stored vectors using:

  * `.npy` files (NumPy arrays)
* Enables fast similarity computation

---

### 5️⃣ Similarity Search

* Used:

  ```python
  cosine_similarity
  ```
* Compared user query vector with recipe vectors
* Retrieved **Top-K most similar recipes**

---

### 6️⃣ Query Understanding

* User can input **free-text queries**

  ```
  "I have paneer and bread, what can I cook?"
  ```
* System extracts relevant ingredients using:

  * regex tokenization
  * fuzzy matching

---

### 7️⃣ Recommendation Engine

* Steps:

  1. Convert query → vector
  2. Compute similarity scores
  3. Rank recipes
  4. Return top matches

---

## 🧪 Example

**Input:**

```
i have paneer and bread
```

**Output:**

```
Recommended Recipes:
- Cheese Sandwich
- Bread Butter Pudding
- Paneer Toast
```
---

## 📁 Project Structure

```
cook-ai/
│
├── ml-engine/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── recommendation/
│
├── backend/
│   └── app.py
│
├── data/
│   └── processed/
│
└── README.md
```

---

## ⚡ Key Features

✔ Semantic recipe search (not keyword-based)
✔ Handles natural language input
✔ Fuzzy matching for real-world inputs
✔ Fast vector-based retrieval
✔ Flask API integration

---

## 🎯 Conclusion

This project goes beyond basic ML models and demonstrates:

* Real-world problem solving
* End-to-end system design
* Integration of ML with backend

It reflects the ability to build **production-ready AI systems**, not just notebooks.

---

## 👨‍💻 Author

**Deepansh Khandelwal**

---

⭐ If you like this project, feel free to star the repo!
