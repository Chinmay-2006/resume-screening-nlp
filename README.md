# 📄 NLP-Based Resume Screening System

🔗 **Live App:** [https://resume-screening-nlp-c45mfzappqldkgkn5trumbj.streamlit.app](https://resume-screening-nlp-c45mfzappqldkgkn5trumbj.streamlit.app)

A web-based application that automatically screens and ranks resumes against a Job Description using Natural Language Processing techniques.

## 🔍 Overview

This system takes a Job Description and multiple resumes as input, then analyzes and ranks candidates based on:
- **Skill Match** — comparison of technical skills mentioned in the resume vs the JD
- **TF-IDF Similarity** — exact word/content overlap between documents
- **Semantic Similarity** — meaning-based similarity using word embeddings (captures related concepts even with different wording)

It also provides additional resume quality insights: completeness check, readability score, and a visual word cloud per candidate.

## ✨ Features

- Supports PDF, DOCX, and TXT resume formats
- Multi-resume upload and automatic ranking
- Transparent, explainable scoring (see exactly how each score is calculated)
- Skill gap analysis (matched vs missing skills per candidate)
- Resume completeness checker (flags missing sections)
- Readability score (Flesch Reading Ease)
- Word cloud visualization per resume
- Score comparison bar chart
- Downloadable results as CSV

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — web interface
- **NLTK** — tokenization, stopword removal, lemmatization, POS tagging
- **spaCy** — semantic similarity via word embeddings
- **scikit-learn** — TF-IDF vectorization and cosine similarity
- **PyPDF2 / python-docx** — text extraction from resumes
- **WordCloud / Matplotlib** — visualizations
- **textstat** — readability scoring

## ⚙️ How It Works

1. **Text Extraction** — raw text is pulled from uploaded PDF/DOCX/TXT files
2. **Preprocessing** — text is cleaned, tokenized, stopwords removed, and lemmatized
3. **Skill Extraction** — a predefined skill list is matched against both resume and JD (whole-word matching)
4. **Similarity Scoring** — TF-IDF + Cosine Similarity measures exact content overlap; spaCy word embeddings measure semantic/meaning-based similarity
5. **Final Score** — combines Skill Match (60%) and average Content Similarity (40%), with a fallback to pure content similarity if the JD has no explicit technical skills listed
6. **Ranking** — all resumes are ranked by Final Score, with a full breakdown available per candidate

## 🚀 Running Locally

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
streamlit run app.py
```

## 📊 Sample Output

Upload a Job Description and resumes through the web interface, click **Analyze**, and view:
- Ranked results table
- Score comparison chart
- Per-candidate skill breakdown, completeness, readability, and word cloud

## 📁 Project Structure
├── app.py # Streamlit UI
├── extractor.py # PDF/DOCX/TXT text extraction
├── preprocessing.py # Text cleaning, tokenization, lemmatization
├── skills.py # Skill list and matching logic
├── similarity.py # TF-IDF + semantic similarity + final scoring
├── semantic.py # spaCy-based semantic similarity
├── resume_quality.py # Completeness checker + readability scoring
├── requirements.txt
└── sample_data/ # Sample resumes and job description for testing


## 👤 Author

Chinmay Patil
B.E. Computer Engineering, MGM College of Engineering & Technology