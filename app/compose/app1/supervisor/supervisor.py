from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langgraph.graph import END, StateGraph, MessagesState
from langchain_core.agents import AgentAction, AgentFinish

from app.agents.agentstate import AgentState
#from app.tools.appdef import appdef
from app.agents.prompt import SUMMARY_PROMPT
from app.agents.prompt import SUPERVISOR_PROMPT
from app.config.config import config


# This needs to composed by hand.
# Because we will never know which of the agents 
# are used by an application
members = ["App_Detect","App_Change_Detect","Cluster_Health","App_Health_from_metric",
           "App_Health_from_log","App_Health_from_alert","App_Health_from_slo"] 


def supervisor_chain(state: AgentState):
    
    
    if isinstance(state['messages'][-1], str):
        msg = state['messages'][-1]
    else:
        msg = state['messages'][-1].content

    messages = [
        SystemMessage(content=SUPERVISOR_PROMPT.format(members=members)), 
        HumanMessage(content=msg)
        
   ]
    
    if (config.LOG_STATE_DATA):
        print("*************inside supervisor_chain********************")
        for key in state:
            print(key," : ",state[key])
        print("*********************************")
    
    
    #model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    #modelt = model.bind_tools(tools)
    #response = model.invoke(messages)
    
    # As you will see, this supervisor does not even call the LLM
    # This is a point in time statement. Ofcourse we will use LLM
    # This is also exploring art of possible
    
    if not state['appname']:
        value = 'App_Detect'
        return {"next": value,"task":state['messages'][0].content }
    elif state['next'] == 'App_Detect':
        value = 'App_Change_Detect'
        return {"next": value,"task":state['messages'][0].content }
    elif state['next'] == 'App_Change_Detect':
        value = 'Cluster_Health'
        return {"next": value,"task":state['messages'][0].content }
    elif state['next'] == 'Cluster_Health':
        value =  'App_Health_from_metric' 
        return {"next": value,"task":state['messages'][0].content }
    elif state['next'] == 'App_Health_from_metric':
        value = 'App_Health_from_log'  
        return {"next": value,"task":state['messages'][0].content }
    elif state['next'] == 'App_Health_from_log':
        value = 'App_Health_from_alert'  
        return {"next": value,"task":state['messages'][0].content }
    elif state['next'] == 'App_Health_from_alert':
        value = 'App_Health_from_slo'  
        return {"next": value,"task":state['messages'][0].content }
    elif state['next'] == 'App_Health_from_slo':
        value = 'Summary'
        #return {"next": value,"task":state['messages'][0].content }
        content = state['messages'] 
        messages = [
        SystemMessage(content=SUMMARY_PROMPT.format(content=content)),
        ]
    
        model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        response = model.invoke(messages)
        return {"next": 'FINISH', "summary": response.content}
    
    else:
        value = 'FINISH'
        return {"next": value,"task":state['messages'][0].content }
    
