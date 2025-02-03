from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retrieve import retrieve

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class chatrequest(BaseModel):
    collection_name:str
    question:str
    limit:int
    

@app.get("/")
def read_root():
    return {"message":"welcome to docling fastapi"}


@app.get("/chat")
def chat(input:chatrequest):
    question = input.question 
    collection_name = input.collection_name
    limit = input.limit
    response = retrieve(collection_name, question, limit)
    return response


@app.post("/chat/stream")
async def chat_stream(input:chatrequest):
    question = input.question 
    collection_name = input.collection_name
    limit = input.limit
    response = retrieve(collection_name, question, limit)
    return response
