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

SUPERVISOR_PROMPT = """You are a supervisor tasked with getting the application health. \
    You have the following workers:  {members}. Given the user request, \
    find the application name that user is asking about. \
    Use the worker/member that can do it. \
    Once you have got the application name, \
    find out the health of that application from the metrics point of view. \
    Use the worker/member that can do it. \
    Just respond with the worker/member name who should act next - nothing else. \
    Each worker will perform a \
    task and respond with their results and status. \
    Hint - the order in which the members are organized is the order in which they can be called. \
    Concretely - call Appdetect first. After its done, call Appmetric etc. \
    When finished, respond with FINISH."""

members = ["App_Detect"] 


def supervisor_chain(state: AgentState):
    
    
    if isinstance(state['messages'][-1], str):
        msg = state['messages'][-1]
    else:
        msg = state['messages'][-1].content

    messages = [
        SystemMessage(content=SUPERVISOR_PROMPT.format(members=members)), 
        HumanMessage(content=msg)
        
   ]
    
    if (log_state_data):
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
    
