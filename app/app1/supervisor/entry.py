import os
import openai
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import END, StateGraph, START
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage

from app.app1.supervisor.graph import graph_build


def main() :

    _ = load_dotenv(find_dotenv()) 
    openai.api_key  = os.getenv('OPENAI_API_KEY')

    graph = graph_build()

    thread = {"configurable": {"thread_id": "1"}}

    print("Starting Program......")

        
    for s in graph.stream(
        {"messages": [HumanMessage(content="How is the health of my application retailbanking.")]},
        #{"task": "How is the health of my application retail_banking."},
        #{"recursion_limit": 4},
        thread
        ):
        if "__end__" not in s:
            print(s)
            print("----")

if __name__ == "__main__":
    main()