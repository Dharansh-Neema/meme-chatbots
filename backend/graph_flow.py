from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.checkpoint.memory import MemorySaver
from pyadantic_class import AgentState
from logger import setup_logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage
from prompts import chatbot_prompt
from dotenv import load_dotenv
import os 
load_dotenv()

# logger = setup_logger(name="graph_flow",log_file="logs/graph_flow.log")
memory = MemorySaver()
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
        print(f"Failed to initialize LLM: {str(e)}")
        raise

def get_gemini_llm():
    """
    It will initialize the gemini llm
    and return it. 
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.8,
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        return llm
    except Exception as e:
        print(f"Failed to initialize LLM: {str(e)}")
        raise

def generate_response(state:MessagesState):
    """
    It will generate the response for the given state or the query.
    """
    try:
        llm = get_groq_llm()
        prompt = chatbot_prompt.format(query=state["messages"])
        system_prompt = (prompt)
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = llm.invoke(messages)
        return {"messages":response}


    except Exception as e:
        print(f"Failed to generate response: {str(e)}")
        raise
def chatbot_resposne(state:AgentState):
    try:
        llm = get_gemini_llm()
        prompt = chatbot_prompt.format(query=state.query)
        response = llm.invoke(prompt)
        state.response = response.content.upper()
        return state
    except Exception as e:
        print(f"Failed to generate response: {str(e)}")
        raise
    

# graph = StateGraph(AgentState)
# graph=graph.add_node("generate_response", generate_response)   
# graph=graph.add_edge(START, "generate_response")
# graph=graph.add_edge("generate_response", END) 
# app = graph.compile(checkpointer=memory)          
        
if __name__ == "__main__":
    print(chatbot_resposne(AgentState(query="I have a date tonight but I am sacred to ask.")))