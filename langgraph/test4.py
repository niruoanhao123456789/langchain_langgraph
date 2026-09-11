import operator
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Overwrite

# Overwriter

class State(TypedDict):
    messages: Annotated[list[str], operator.add]

# 节点一：追加信息
def add_message(state:State):
    return {"messages":["first message"]}

# 节点二：覆盖消息
def replace_message(state:State):
    return{"messages":Overwrite(["replace message"])}
    # return {"messages": ["replace message"]}

builder = StateGraph(State)
builder.add_node(add_message)
builder.add_node(replace_message)
builder.add_edge(START,"add_message")
builder.add_edge("add_message","replace_message")
builder.add_edge("replace_message",END)
graph = builder.compile()
result = graph.invoke(
    {
        "messages":[""]
    }
)
print(result["messages"])