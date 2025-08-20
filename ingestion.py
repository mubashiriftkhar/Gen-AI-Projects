from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
import cohere
from dotenv import load_dotenv
import os
import glob
import uuid

load_dotenv()

co = cohere.AsyncClientV2(api_key=os.getenv("cohereKey"))

pc = Pinecone(api_key=os.getenv("pineconeKey"))




    
def generate_pdf_chunks(pdf, chunk_size=500, chunk_overlap=50):
        all_docs = []
        # Load PDF
        loader = PyPDFLoader(pdf)
        pages = loader.load()  # returns list of Documents

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for page in pages:
            chunks = text_splitter.split_text(page.page_content)
            for chunk in chunks:
                doc ={
                    "_id":str(uuid.uuid4()),
                    "text":chunk,
                }
                all_docs.append(doc)

        print(f"[DONE] Generated {len(all_docs)} chunks of PDF '{pdf}'")
        return all_docs

dense_index_name = "legal-tech-dense-for-hybrid-search"
sparse_index_name = "legal-tech-sparse-for-hybrid-search"

if not pc.has_index(dense_index_name):
    pc.create_index_for_model(
        name=dense_index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )

if not pc.has_index(sparse_index_name):
    pc.create_index_for_model(
        name=sparse_index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"pinecone-sparse-english-v0",
            "field_map":{"text": "chunk_text"}
        }
    )

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i+chunk_size]

def ingestRecords(pdfFiles):
    dense_index = pc.Index(host="https://legal-tech-dense-for-hybrid-search-crs8ha4.svc.aped-4627-b74a.pinecone.io")
    sparse_index = pc.Index(host="https://legal-tech-sparse-for-hybrid-search-crs8ha4.svc.aped-4627-b74a.pinecone.io")
    for pdf in pdfFiles:
        records = generate_pdf_chunks(pdf)

        # Batch the records to avoid exceeding Pinecone’s limit
        for batch in chunk_list(records, 96):
            dense_index.upsert_records("all-over-world", batch)
            sparse_index.upsert_records("all-over-world", batch)

if __name__ == "__main__":
    pdf_dir = "DataSets"
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    ingestRecords(pdfFiles=pdf_files)
