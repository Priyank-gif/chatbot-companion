# config.py
import json
import os
import urllib

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from app.aws_secret_manager import get_secret

# Load environment variables
load_dotenv()

# Define the path to save the file
temp_file_path = "uploaded_files/uploaded_file.pdf"

# Path to the FAISS index file
vector_db_path = "faiss_index_constitution"

try:
    secrets = json.loads(get_secret())
    api_key = secrets['GOOGLE_API_KEY']
    encoded_password = secrets['DB_PASSWORD']
    host = secrets['DB_HOST']
    name = secrets['DB_NAME']
except:
    api_key=os.getenv('GOOGLE_API_KEY')
    encoded_password = urllib.parse.quote(os.getenv('DB_PASSWORD'))
    host = os.getenv('DB_HOST')
    name = os.getenv('DB_NAME')

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# Database details

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{encoded_password}@{host}/{name}"
