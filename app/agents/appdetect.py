from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langgraph.graph import END, StateGraph, MessagesState
from langchain_core.agents import AgentAction, AgentFinish

from app.compose.app1.supervisor.agentstate import AgentState
from app.tools.appdef import appdef
from app.agents.prompt import APPDETECT_PROMPT
from app.config.config import config


def appdetect_node(state: AgentState):

    
    if (config.LOG_STATE_DATA):
        print("*************inside appdetect_node********************")
        for key in state:
            print(key," : ",state[key])
        print("*********************************")
    
    messages = [
        SystemMessage(content=APPDETECT_PROMPT), 
        HumanMessage(content=state['task'])
    ]
   

    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = model.invoke(messages)
    
    # notice how we call the tool directly
    # This business of detecting the application topology is 
    # a very complex one. What is shown here now is deployment topology
    # What is not shown is application internal dependencies between pods etc.
    # Those are very valuable when available. They can be surfaced from different sources
    # NetworkObservability, Traces, KnowledgeGraphs etc
    value = appdef.run({"query": response.content})  

    return {"messages": [response.content],"appname":response.content,"composition": value }