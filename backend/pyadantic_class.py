from pydantic import BaseModel,Field
class AgentState(BaseModel): 
    query: str = Field(description="Query to be sent to the chatbot", default=" ")
    model: str = Field(description="Model to be used for generating the reply", default="gemini")
    response: str = Field(description="Response from the llm in savage and harvy tone", default=" ")
