from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langgraph.graph import END, StateGraph, MessagesState
from langchain_core.agents import AgentAction, AgentFinish


from app.agents.agentstate import AgentState
from app.tools.appdef import appdef
from app.agents.prompt import SUMMARY_PROMPT
from app.config.config import config





# This is actually not used.
# Supervisor is summarizing
def summary_node(state: AgentState):
    
    if (config.LOG_STATE_DATA):
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
