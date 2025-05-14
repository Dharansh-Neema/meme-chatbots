from pydantic import BaseModel,Field
class chatbot(BaseModel):
    query : str = Field(...,description="Query to be sent to the chatbot")
    model : str = Field(...,description="Model to be used for generating the reply")
    response : str = Field(...,description="Response from the chatbot")