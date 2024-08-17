import functools
import operator
from typing import Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import END, StateGraph, START
from typing import Annotated


# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # This is storing the initial question from the user
    task: str
    # This will store the appname    
    appname: str
    # This stores the composition of the application
    # This should probably be a python dict at some point
    composition: str    
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str
    # The 'summary' field contains the final summary
    summary: str 