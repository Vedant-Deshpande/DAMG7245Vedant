from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

class UserInput(BaseModel):
        service: str
        apikey: str
        content: list

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

app = FastAPI(title="DAMG7245 - Labs")


@app.get("/api/v1/health")
async def check() -> dict:
    return {"message": "OK"}

@app.post("/api/v1/tokenize")
async def tokenize(userinput: UserInput) -> dict:
    # user input validations

    # service validation
    if userinput.service not in ["huggingface", "openai", "cohere"]:
        raise HTTPException(status_code=404, detail=r"Service not among 'huggingface', 'openai', 'cohere'")

    # content validation
    print(len(userinput.content))
    if len(userinput.content) < 1:
        raise HTTPException(status_code=404, detail=r"Content should be a list of one or more than items")
    
    response = {}
    response["userinput"] = userinput.content
    # tokenization
    if userinput.service == "huggingface":
        embeddings = model.encode(userinput.content)
        response["embeddings"] = embeddings.tolist()
        return JSONResponse(content=response)
    elif userinput.service == "openai":
        # Call OpenAI API
        return JSONResponse(content="OK")
    elif userinput.service == "cohere":
        # Call Cohere API
        return JSONResponse(content="OK")

# Testing
# uvicorn main:app --reload --port 8000

# Production
# gunicorn -k uvicorn.workers.UvicornWorker main:app