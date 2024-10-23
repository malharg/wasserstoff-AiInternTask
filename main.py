
import json
import pymongo
from pdf_processing import process_pdfs
from summarizer import summarize_textrank, clean_text
from keyword_extractor import extract_keywords
import time
import psutil  # For memory usage

print("Starting the PDF processing pipeline...")

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pdf_database"]  # Replace with your actual database name
collection = db["pdf_data_2"]  # Replace with your actual collection name

# Load JSON data
with open('Dataset.json') as f:
    json_data = json.load(f)

print(f"Loaded {len(json_data)} PDFs from Dataset.json.")
print(json_data)

def log_error_to_mongodb(pdf_name, pdf_url, error_message):
    
    error_document = {
        "pdf_name": pdf_name,
        "url": pdf_url,
        "status": "error",
        "error_message": error_message
    }
    collection.update_one(
        {"pdf_name": pdf_name},
        {"$set": error_document},
        upsert=True  # Create new document if it doesn't exist
    )
    print(f"Logged error for {pdf_name} in MongoDB.")

# Function to process each PDF
def process_pdf(pdf_name, pdf_url):
    try:
        # Extract text from PDF
        text = process_pdfs(pdf_url)
        

        # Proceed only if text extraction is successful
        if text:
            # Generate summary and extract keywords
            c_text = clean_text(text)
            summary = summarize_textrank(c_text)
            keywords = extract_keywords(text)

            #  MongoDB document
            document = {
                "pdf_name": pdf_name,
                "url": pdf_url,
                "summary": summary,
                "keywords": keywords,
                "status": "processed"  
            }
            collection.update_one(
                {"pdf_name": pdf_name},
                {"$set": document},
                upsert=True  # Create new document if it doesn't exist
            )
            print(f"Processed and saved {pdf_name} successfully.")
        else:
            raise ValueError(f"Unable to extract text from {pdf_url}")

    except Exception as e:
        print(f"Error processing {pdf_name}: {str(e)}")
        log_error_to_mongodb(pdf_name, pdf_url, str(e))

# Track the start time for performance measurement
start_time = time.time()
print("Starting PDF processing...")

# Process PDFs one by one
for pdf_name, pdf_url in json_data.items():
    process_pdf(pdf_name, pdf_url)

print("All PDFs have been processed.")

# Measure and print total processing time and memory usage
end_time = time.time()
total_time = end_time - start_time
memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert bytes to MB
print(f"Total processing time: {total_time:.2f} seconds")
print(f"Memory usage: {memory_usage:.2f} MB")




