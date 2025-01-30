from qdrant_client import QdrantClient
from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter

# Qdrant configuration
url = "https://a4433f8f-e80e-4067-b02e-c127e263cc55.us-east4-0.gcp.cloud.qdrant.io:6333"  
api_key = "N8IrtraPhAviG2id7OjVjwyd1UzQccNiT3o_xYW_QqOAQW5ry8hbGQ"

# Initialize Qdrant client
client = QdrantClient(url=url, api_key=api_key)

# Set models
client.set_model("sentence-transformers/all-MiniLM-L6-v2")
client.set_sparse_model("Qdrant/bm25")


def upload_pdf(file_path, collection_name):
    """
    Upload and process a PDF document to Qdrant collection
    
    Args:
        file_path: Path to the document file
        collection_name: Name of the Qdrant collection
    """
    # Initialize document converter with supported formats
    doc_converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PPTX,
            InputFormat.PDF,
            InputFormat.DOCX,
            InputFormat.XLSX
        ]
    )

    # Convert document
    result = doc_converter.convert(file_path)

    # Process document chunks
    documents, metadatas = [], []
    for chunk in HybridChunker().chunk(result.document):
        documents.append(chunk.text)
        metadatas.append(chunk.meta.export_json_dict())

    # Upload to Qdrant
    qdrant = client.add(
        collection_name=collection_name,
        documents=documents,
        metadata=metadatas,
        batch_size=64
    )

    print("Upload successful")



