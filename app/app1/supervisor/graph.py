from langchain_core.messages import BaseMessage, HumanMessage

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import END, StateGraph, START
from app.agents.agentstate import AgentState
from app.agents.app_detect import appdetect_node
from app.app1.supervisor.supervisor import supervisor_chain
from langgraph.checkpoint.sqlite import SqliteSaver


members = ["App_Detect"] 

def graph_build() :
    workflow = StateGraph(AgentState)
    workflow.add_node("supervisor", supervisor_chain)
    workflow.add_node("App_Detect",appdetect_node)

    for member in members:
        # We want our workers to ALWAYS "report back" to the supervisor when done
        workflow.add_edge(member, "supervisor")
    
    # The supervisor populates the "next" field in the graph state
    # which routes to a node or finishes
    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
    # Finally, add entrypoint
    workflow.add_edge(START, "supervisor")

    memory = SqliteSaver.from_conn_string(":memory:")
    #graph = workflow.compile()
    graph = workflow.compile(checkpointer=memory)
    return graph




