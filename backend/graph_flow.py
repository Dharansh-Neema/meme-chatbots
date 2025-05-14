from langgraph.graph import StateGraph
from logger import setup_logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

logger = setup_logger(name="graph_flow",log_file="logs/graph_flow.log",level=logging.INFO)

def get_groq_llm():
    """
    It will initialize the groq llm
    and return it. 
    """
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.8,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise
