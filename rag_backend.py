import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

# Define paths
DATA_DIR = "data/"
CHROMA_PATH = "chroma_db/"

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def get_embedding_function():
    """Returns the local embedding function consistently."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def process_new_pdf(file_name):
    """
    Deletes the old vector database, loads the new PDF,
    chunks it, and builds a fresh vector database.
    """
    # 1. Clear the old vector database directory if it exists
    if os.path.exists(CHROMA_PATH):
        print(f"Clearing old vector database at {CHROMA_PATH}...")
        shutil.rmtree(CHROMA_PATH)

    # 2. Load and chunk the new PDF
    file_path = os.path.join(DATA_DIR, file_name)
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Create the fresh vector database
    embeddings = get_embedding_function()
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Successfully indexed {file_name} ({len(chunks)} chunks).")
    return len(chunks)


def query_rag(query_text):
    """
    Retrieves relevant context chunks from ChromaDB and generates an answer using local Llama.
    """
    embeddings = get_embedding_function()

    # Verify database exists before querying
    if not os.path.exists(CHROMA_PATH):
        return "No documents have been uploaded or indexed yet. Please upload a PDF first.", []

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    if len(results) == 0:
        return "No relevant context found in the document.", []

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    sources = [doc.metadata.get("page", "Unknown") for doc, _score in results]
    formatted_sources = sorted(list(set([int(p) + 1 for p in sources if str(p).isdigit()])))

    PROMPT_TEMPLATE = """
    You are an expert corporate legal and HR assistant. Answer the question based strictly on the following context. 
    If the context does not contain the answer, state clearly that the information is not available in the document.
    Do not make up facts.

    Context:
    {context}

    ---

    Question: {question}
    """

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOllama(model="llama3.2", temperature=0)
    response = model.invoke(prompt)

    # Extract text content from response object safely
    return response.content, formatted_sources