# PDF Processing Pipeline

This project implements a pipeline to process multiple PDFs, extract text, summarize the content, and extract relevant keywords. It stores the results and metadata in MongoDB. The pipeline is designed to handle concurrency, error logging, and performance monitoring.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Overview](#project-overview)
- [File Descriptions](#file-descriptions)
- [Performance Metrics](#performance-metrics)

## System Requirements

- **Python 3.8+**
- **MongoDB** (Ensure MongoDB is installed and running)
- **pip** (Python package manager)
- Internet connection for downloading PDF files

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install MongoDB** (if not already installed):
    - You can follow the instructions from the official [MongoDB installation guide](https://docs.mongodb.com/manual/installation/).

5. **Download NLTK datasets** for the summarizer:
    ```python
    python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
    ```

## Usage

1. **Edit Dataset.json**:
    - Add the URLs of the PDFs to be processed in the `Dataset.json` file in the following format:
    ```json
    {
      "pdf1": "https://example.com/pdf1.pdf",
      "pdf2": "https://example.com/pdf2.pdf",
      ...
    }
    ```

2. **Run the main script**:
    ```bash
    python main.py
    ```

3. **Check MongoDB for results**:
    - Open your MongoDB instance and check the `pdf_data` (your collection name here) collection to see the processed PDFs, summaries, keywords, and errors (if any).

## Project Overview

The pipeline performs the following tasks for each PDF in the dataset:
1. Downloads and extracts text from PDFs.
2. Cleans the extracted text and removes unnecessary punctuation, numbers, and stopwords.
3. Generates a summary of the text using a TextRank algorithm.
4. Extracts relevant keywords, including dates, from the content.
5. Logs metadata, summary, and keywords into MongoDB.
6. Handles errors during the processing and logs them for review.

## File Descriptions

- **`main.py`**:
    - The main entry point that orchestrates the PDF processing. It manages MongoDB connections, processes PDFs, and logs errors.
  
- **`pdf_processing.py`**:
    - Contains functions to download and extract text from PDFs using PyPDF2.
  
- **`summarizer.py`**:
    - Implements the TextRank summarization algorithm and functions to clean text and split it into sentences.

- **`keyword_extractor.py`**:
    - Extracts keywords based on word frequency, excluding common stopwords and domain-specific terms (legal, regulatory, etc.).

- **`Dataset.json`**:
    - Stores PDF names and URLs for processing.

## Performance Metrics

The script tracks and prints:
- **Total processing time** for all PDFs.
- **Memory usage** during processing (in MB).
  
These metrics are displayed at the end of the run for performance monitoring.

## Example Output in MongoDB

For each processed PDF, the MongoDB collection `pdf_data_2` will store a document like the following:
```json
{
  "pdf_name": "pdf1",
  "url": "https://example.com/pdf1.pdf",
  "summary": "The extracted summary text...",
  "keywords": ["keyword1", "keyword2", ...],
  "status": "processed"
}


