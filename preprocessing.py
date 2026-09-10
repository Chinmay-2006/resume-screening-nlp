import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load stopwords once (words like "the", "is", "a" that carry no real meaning)
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """Remove special characters, numbers, and extra whitespace. Lowercase everything."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)   # keep only letters and spaces
    text = re.sub(r'\s+', ' ', text).strip()  # collapse multiple spaces into one
    return text


def tokenize(text):
    """Split cleaned text into individual word tokens."""
    return word_tokenize(text)


def remove_stopwords(tokens):
    """Remove common low-meaning words like 'the', 'is', 'and'."""
    return [word for word in tokens if word not in stop_words]


def lemmatize_tokens(tokens):
    """Reduce words to their base dictionary form (e.g., 'running' -> 'run')."""
    return [lemmatizer.lemmatize(word) for word in tokens]


def preprocess_text(text):
    """
    Full pipeline: clean -> tokenize -> remove stopwords -> lemmatize.
    Returns a list of clean, meaningful base-form words.
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize_tokens(tokens)
    return tokens


if __name__ == "__main__":
    # Quick test — run this file directly to see it work
    sample = "I am experienced in Python programming, Machine Learning, and Data Analysis!"
    result = preprocess_text(sample)
    print("Original:", sample)
    print("Processed:", result)

def clean_for_wordcloud(text):
    """
    Prepares text for word cloud generation:
    - cleans and tokenizes
    - removes stopwords
    - removes single-letter junk tokens (common PDF extraction artifacts)
    - does NOT lemmatize, so words look natural in the visual
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = [word for word in tokens if len(word) > 2]  # drop single/double-letter junk
    return " ".join(tokens)