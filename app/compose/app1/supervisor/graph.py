from langchain_core.messages import BaseMessage, HumanMessage

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import END, StateGraph, START
from app.compose.app1.supervisor.agentstate import AgentState
from app.agents.appdetect import appdetect_node

from app.agents.appchangedetect import appchangedetect_node
from app.agents.clusterhealth import cluster_health_node
from app.agents.appmetric import appmetric_node
from app.agents.applog import applog_node
from app.agents.appalert import appalert_node
from app.agents.appslo import appslo_node

from app.compose.app1.supervisor.supervisor import supervisor_chain
from langgraph.checkpoint.sqlite import SqliteSaver

from IPython.display import Image, display
#from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeColors
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod


members = ["App_Detect","App_Change_Detect","Cluster_Health","App_Health_from_metric",
           "App_Health_from_log","App_Health_from_alert","App_Health_from_slo"] 

def graph_build() :
    workflow = StateGraph(AgentState)
    workflow.add_node("supervisor", supervisor_chain)
    workflow.add_node("App_Detect",appdetect_node)

    workflow.add_node("App_Change_Detect",appchangedetect_node)
    workflow.add_node("Cluster_Health",cluster_health_node)
    workflow.add_node("App_Health_from_metric",appmetric_node)
    workflow.add_node("App_Health_from_log",applog_node)
    workflow.add_node("App_Health_from_alert",appalert_node)
    workflow.add_node("App_Health_from_slo",appslo_node)

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


    """ 
    display(
        Image(
            graph.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )
        )
    ) """

    return graph




