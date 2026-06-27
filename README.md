# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using **Python**, **Machine Learning**, and **Streamlit**. The application recommends movies similar to the one selected by the user and displays their official movie posters using the TMDB API.

---

## 📌 Features

- 🎥 Content-Based Movie Recommendation
- 🤖 Machine Learning using Cosine Similarity
- 🎞️ Displays Official Movie Posters
- 🔍 Search and Recommend Similar Movies
- ⚡ Fast and Interactive Streamlit Web App
- 🌐 TMDB API Integration
- 📊 Preprocessed Movie Metadata

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Machine Learning
- Scikit-learn
- CountVectorizer
- Cosine Similarity

### Libraries Used
- Pandas
- NumPy
- Requests
- Pickle
- Streamlit

### API
- TMDB (The Movie Database)

---

# 📂 Project Structure

```
movie_predictor/
│
├── app.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
├── README.md
│
├── dataset/
│   ├── movies.csv
│   └── credits.csv
│
└── images/
    └── demo.png
```

---

# 📊 Dataset

The project uses the TMDB Movie Dataset containing movie metadata such as:

- Movie Title
- Genres
- Keywords
- Cast
- Crew
- Overview

These features are combined into a single text column called **tags** for recommendation.

---

# ⚙️ How It Works

### Step 1

Load Movie Dataset

↓

### Step 2

Clean and preprocess the data

↓

### Step 3

Merge important movie features

↓

### Step 4

Create Tags

↓

### Step 5

Convert text into vectors using CountVectorizer

↓

### Step 6

Calculate Cosine Similarity Matrix

↓

### Step 7

Store processed data using Pickle

↓

### Step 8

Streamlit loads the model

↓

### Step 9

User selects a movie

↓

### Step 10

Top similar movies are recommended with posters

---

# 🧠 Machine Learning Pipeline

```
Movie Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Tags Generation
      │
      ▼
CountVectorizer
      │
      ▼
Feature Vectors
      │
      ▼
Cosine Similarity
      │
      ▼
Recommendation Engine
```

---



# 📚 Learning Outcomes

This project demonstrates:

- Data Cleaning
- Feature Engineering
- Natural Language Processing
- Vectorization
- Cosine Similarity
- Machine Learning
- API Integration
- Streamlit Development
- Python Programming
- Recommendation Systems

---

# 🎯 Project Highlights

✔ Content-Based Recommendation System

✔ Machine Learning Powered

✔ Interactive Streamlit Interface

✔ TMDB API Integration

✔ Real-Time Poster Fetching

✔ Fast Recommendation Engine

✔ Beginner-Friendly Architecture

---

# 👨‍💻 Author

**Harsh Shaw**

Master's in Computational Science and Applications

Python Developer | Machine Learning Enthusiast | AI Engineer

GitHub:
https://github.com/Theguywithspideysense

LinkedIn:
(Add your LinkedIn profile)

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.

---

## 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and contribute.
