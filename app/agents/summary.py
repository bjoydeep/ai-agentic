from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langgraph.graph import END, StateGraph, MessagesState
from langchain_core.agents import AgentAction, AgentFinish

from app.agents.agentstate import AgentState
from app.tools.appdef import appdef

log_state_data = False

SUMMARY_PROMPT = """You are an expert at summarizing the state of affairs. \
List all the checks that has been done. \
Create a concluding statement - call it in conclusion - a summarize your findings in a binary manner - good or bad. 
------

{content}"""

# This is actually not used.
# Supervisor is summarizing
def summary_node(state: AgentState):
    
    if (log_state_data):
        print("*************inside summary_node********************")
        for key in state:
            print(key," : ",state[key])
        print("*********************************")
    
    content = state['messages'] 
    
    messages = [
        SystemMessage(content=SUMMARY_PROMPT.format(content=content)),
    ]
    
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = model.invoke(messages)
    
    return {"summary": response.content}
