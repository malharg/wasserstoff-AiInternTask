import re
import numpy as np
from collections import defaultdict
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
nltk.download('stopwords')
nltk.download('wordnet')

# Refined stopwords for summarization
STOPWORDS = set(nltk_stopwords.words('english'))

lemmatizer = WordNetLemmatizer()

# Helper function to clean and split text into sentences
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [sentence.strip() for sentence in sentences if sentence]

# Function to clean text and remove unwanted characters like '\n'
def clean_text(text):
    # Regex pattern to preserve dates (e.g., 12/05/2023, 2023-05-12, YYYY)
    date_pattern = r'\b(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{1,2}-\d{1,2}|\d{4})\b'

    # Extract dates
    dates = re.findall(date_pattern, text)

    # Remove newline characters 
    text = text.replace('\n', ' ')

    # Remove any lingering '\n' attached to words
    text = re.sub(r'\\n', '', text)

    # Remove punctuation except periods (for sentence splitting)
    text_without_punct = re.sub(r'[^\w\s.]', '', text)

    # Remove standalone numbers but keep dates
    text_without_numbers = re.sub(r'\b\d+\b', '', text_without_punct)

    # Reinsert dates into the cleaned text
    for date in dates:
        text_without_numbers = text_without_numbers.replace(" ", f" {date} ", 1)

    # Remove stopwords and lemmatize words
    words = text_without_numbers.lower().split()
    cleaned_words = [lemmatizer.lemmatize(word) for word in words if word not in STOPWORDS]

    # Join cleaned words into a final string
    return " ".join(cleaned_words)

# WordNet Synonyms Lookup (for synonym-based similarity enhancement)
def get_synonyms(word):
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Function to calculate sentence similarity using TF-IDF and cosine similarity
def sentence_similarity_tfidf(sentences):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    return cosine_similarity(tfidf_matrix)

# TextRank Algorithm for Summarization (using sentence similarity matrix)
def text_rank(sentences, d=0.85, threshold=0.0001, max_iter=100):
    n = len(sentences)

    # Compute similarity matrix using TF-IDF
    similarity_matrix = sentence_similarity_tfidf(sentences)

    # Normalize the matrix
    row_sums = similarity_matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # Handle zero-sum rows
    similarity_matrix = similarity_matrix / row_sums

    # Initialize page rank scores
    scores = np.ones(n) / n

    # PageRank loop
    for _ in range(max_iter):
        new_scores = (1 - d) + d * similarity_matrix.dot(scores)
        if np.sum(np.abs(new_scores - scores)) < threshold:
            break
        scores = new_scores

    return scores

# Summarization using TextRank
def summarize_textrank(text, summary_size=0.3):
    sentences = split_sentences(text)
    if len(sentences) <= 3:
        return text  # Return original text if it's short

    # Clean sentences
    cleaned_sentences = [clean_text(sentence) for sentence in sentences]

    # Get TextRank scores
    scores = text_rank(cleaned_sentences)

    # Rank sentences by scores and select the top 'summary_size' percentage
    ranked_sentences = sorted(((score, sentence) for score, sentence in zip(scores, sentences)), reverse=True)
    summary_length = max(1, int(len(sentences) * summary_size))
    summary_sentences = [sentence for _, sentence in ranked_sentences[:summary_length]]

    # Return the summary as a string
    return " ".join(summary_sentences)

