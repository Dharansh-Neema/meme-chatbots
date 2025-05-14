import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
import uvicorn

# Import services (to be implemented)
from app.services.agent_service import enhance_prompt
from app.services.image_service import generate_image
from app.core.config import settings

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
    prompt: str
    style: Optional[str] = None
    model: Optional[str] = "default"  # default, flux, dalle, gemini, ideogram

class MemeResponse(BaseModel):
    original_prompt: str
    enhanced_prompt: str
    image_url: str
    model_used: str

# Define routes
@app.get("/")
async def root():
    return {"message": "Welcome to Meme Chatbot API"}

@app.post("/generate-meme", response_model=MemeResponse)
async def create_meme(request: MemeRequest):
    try:
        # Enhance the prompt using LangGraph agent
        enhanced_prompt = await enhance_prompt(request.prompt, request.style)
        
        # Generate image using the selected model
        image_url = await generate_image(enhanced_prompt, request.model)
        
        return MemeResponse(
            original_prompt=request.prompt,
            enhanced_prompt=enhanced_prompt,
            image_url=image_url,
            model_used=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )
