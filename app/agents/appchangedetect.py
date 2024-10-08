from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langgraph.graph import END, StateGraph, MessagesState
from langchain_core.agents import AgentAction, AgentFinish

from app.compose.app1.supervisor.agentstate import AgentState
from app.tools.appdef import appdef
from app.agents.prompt import APPCHANGE_PROMPT
from app.config.config import config

def appchangedetect_node(state: AgentState):
    
    if (config.LOG_STATE_DATA):
        print("*************inside appchangedetect_node********************")
        for key in state:
            print(key," : ",state[key])
        print("*********************************")
    
    composition = state['composition']
    
    messages = [
        SystemMessage(content=APPCHANGE_PROMPT.format(composition = composition)) ,
   ]

    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = model.invoke(messages)

    return {"messages": [response.content]}