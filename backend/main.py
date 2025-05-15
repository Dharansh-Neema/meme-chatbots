import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyadantic_class import AgentState
from dotenv import load_dotenv
from graph_flow import chatbot_resposne
import uvicorn


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Meme Chatbot API",
    description="API for generating memes using AI",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class MemeRequest(BaseModel):
    query: str



# Define routes
@app.get("/")
async def root():
    return {"message": "Welcome to Meme Chatbot API"}

@app.post("/generate-response")
async def create_meme(request: AgentState):
    try:
        response = chatbot_resposne(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
