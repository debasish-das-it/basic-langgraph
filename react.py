from dotenv import load_dotenv
import os   
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

load_dotenv()

@tool
def triple(num:float) -> float:
    """Triples the input number."""
    return num * 3

tools = [triple, TavilySearch(max_results=1)]

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0).bind_tools(tools)