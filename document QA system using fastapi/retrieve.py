from qdrant_client import QdrantClient  # qdrant client
from docling.chunking import HybridChunker  # chunking
from docling.datamodel.base_models import InputFormat  # doc converter
from docling.document_converter import DocumentConverter  # doc converter
from llm import *  # llm


# set url and api key
url = ""  
api_key = ""


def retrieve(COLLECTION_NAME, question, limit):
    # qdrant client
    client = QdrantClient(url=url, api_key=api_key)

    # set model
    client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    client.set_sparse_model("Qdrant/bm25")

    # query
    points = client.query(
        collection_name=COLLECTION_NAME,
        query_text=question,
        limit=limit,
    )

    # final response
    final_response = " "

    # loop through points
    for i, point in enumerate(points):
        final_response += point.document

    # prompt
    prompt = f"""
      context: {final_response}

       Question: {question}

        you are a document expert and you can answer the question based on the document only give the answer based on given context
      """

    
    return chat_completion(prompt, "meta-llama/llama-3.2-90b-vision-instruct:free")



