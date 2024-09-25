# config.py
import os
import urllib

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()
# Define the path to save the file
temp_file_path = "uploaded_files/uploaded_file.pdf"

# Path to the FAISS index file
vector_db_path = "faiss_index_constitution"
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Database details
encoded_password = urllib.parse.quote(os.getenv('DB_PASSWORD'))
host = os.getenv('DB_HOST')
name = os.getenv('DB_NAME')
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{encoded_password}@{host}/{name}"
