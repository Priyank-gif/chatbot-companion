# config.py
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
