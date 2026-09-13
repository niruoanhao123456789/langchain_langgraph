from typing import TypedDict

from langgraph.constants import START
from langgraph.graph import StateGraph


# 公共状态
class State(TypedDict):
    result: str

class NodeOneOutputState(TypedDict):
    # 隐私数据
    sensitive_data: str

class NodeTwoInputState(TypedDict):
    # 隐私数据
    sensitive_data: str

def node_1(state:State)->NodeOneOutputState:
    """第一步：获取隐私数据"""
    print("node1：获取隐私数据")
    return {
        "sensitive_data":"This is sensitive_data"
    }

def node_2(state:NodeTwoInputState)->State:
    """第二步：拿到隐私数据，去处理（生成非隐私数据）"""
    print("node2：拿到隐私数据，去处理")
    return {
        "result": "This is result after handler"
    }

def node_3(state: State):
    """第三步：构造返回结果"""
    print("node3：构造返回结果")
    return {
        "result": state["result"] + " - finish"
    }

builder = StateGraph(State)
# 添加了3个节点，并规定好了执行顺序
builder.add_sequence([node_1, node_2, node_3])
builder.add_edge(START,"node_1")
# node_3 不指向 END
graph = builder.compile()
print(graph.invoke({
    "result": ""
}))