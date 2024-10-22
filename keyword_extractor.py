
import re
from collections import defaultdict

# Custom keyword extraction logic
def extract_keywords(text):
    # Check if the input text is empty or too short
    if not text or len(text.split()) < 15:  # Assuming 15 words is a reasonable minimum for keyword extraction
        return []

    # Define a regex pattern to match dates in formats like DD/MM/YYYY, YYYY-MM-DD, or just YYYY
    date_pattern = r'\b(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{1,2}-\d{1,2}|\d{4})\b'

    # Find all dates and store them
    dates = re.findall(date_pattern, text)

    # Remove punctuation from the text (but retain spaces and words)
    text_without_punct = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text_without_numbers = re.sub(r'\b\d+\b', '', text_without_punct)  # Remove standalone numbers

    # Convert the cleaned text to lowercase and split into words
    words = re.findall(r'\b\w+\b', text_without_numbers.lower())

    # Define a list of common stopwords to exclude (you can expand this list)
    stopwords = set([
        # General stopwords (English)
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
        "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
        "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
        "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
        "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by",
        "for", "with", "about", "against", "between", "into", "through", "during", "before",
        "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when", "where", "why",
        "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
        "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
        "will", "just", "don", "should", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "number","cl","ii","v","assessee","one","rs","wef","j",
        # Legal/Regulatory stopwords
        "court", "judgment", "bench", "petitioner", "respondent", "appeal", "case", "law", "section",
        "article", "clause", "provision", "act", "code", "rule", "rules", "regulation", "order",
        "decree", "justice", "tribunal", "act", "bench", "filed", "hearing", "proceedings", "affidavit", 
        "suit", "authority", "department", "ministry", "commissioner", "board", "enforcement", 
        "notification", "compliance", "circular", "official", "gazette", "directive", "fraud", 
        "violation", "rbi", "sebi", "high court", "supreme court", "india", "constitution", 
        "prevention", "money-laundering", "records", "state", "union", "territory", 
        "filed", "hearing", "passed", "dated", "issued", "annexure", "document", "certified", 
        "submitted", "report", "forwarded", "referred", "regarding", "therein", "mentioned"
    ])

    # Create a dictionary to count word frequencies
    word_freq = defaultdict(int)

    # Count frequencies of non-stopwords and reinsert dates
    for word in words:
        if word not in stopwords and not word.isdigit():
            word_freq[word] += 1

    # Add dates back into the frequency count, treating each date as a word
    for date in dates:
        word_freq[date] += 1

    # Sort words by frequency and pick the top 10 most common words as keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Extract the words only (excluding the counts) for the top 10
    keywords = [word for word, count in sorted_words[:10]]

    # If no keywords were found, return an empty list
    if not keywords:
        return []

    return keywords





