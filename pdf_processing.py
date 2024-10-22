import requests
from PyPDF2 import PdfReader
from io import BytesIO

# Function to download the PDF
def download_pdf(url):
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        # Return the PDF content as a BytesIO object
        return BytesIO(response.content)
    else:
        print(f"Failed to download the PDF from {url}. Status code: {response.status_code}")
        return None

# Function to process the PDF, extract text
def process_pdfs(pdf_url):
    pdf_content = download_pdf(pdf_url)
    if not pdf_content:
        return None

    # Save the PDF temporarily by extracting the byte data
    with open("temp.pdf", "wb") as f:
        f.write(pdf_content.getvalue())  # Use getvalue() to extract byte data from BytesIO

    # Extract text from the PDF
    text = ""
    try:
        with open("temp.pdf", "rb") as f:
            reader = PdfReader(f, strict=False)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:  # Avoiding adding NoneType to the text
                    text += page_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

    if text.strip():
        return text
    else:
        raise ValueError("No text extracted from the PDF.")



    
