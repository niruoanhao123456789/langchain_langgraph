import operator
from typing import TypedDict, Annotated

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

# 准备工作
search = TavilySearch(max_results=4)
tools = [search]
model = init_chat_model("deepseek-flash",temperature=0)
model_with_tools = model.bind_tools(tools)

# 状态定义
class MessageSate(TypedDict):
    # 消息列表
    # 会话记忆
    # 上下文维护
    messages : Annotated[list[AnyMessage],operator.add]
    # 调用LLM的次数
    llm_calls : int

# 节点定义
def llm_call(state:MessageSate):
    """LLM决定是否调用工具"""

    messages = state["messages"]
    result = model_with_tools.invoke(
        [
            SystemMessage(content="你是一个助人为乐的助手，支持调用工具进行搜索")
        ]
        + messages
    )
    return {
        "messages": [result],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

tools_by_name = {tool.name:tool for tool in tools}
def tool_node(state:MessageSate):
    """执行工具调用"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        obs = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=obs,tool_call_id=tool_call["id"]))

    return {
        "messages": result,
    }

# 定义图，添加节点和边
agent_builder = StateGraph(MessageSate)
agent_builder.add_node(llm_call)
agent_builder.add_node(tool_node)

agent_builder.add_edge(START,"llm_call")

def should_continue(state:MessageSate):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"

    return END

agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node",END]
)
agent_builder.add_edge("tool_node", "llm_call")

# 编译图
# 定义一个内存存储库
checkpointer = InMemorySaver()

# 定义了一个postgres存储库
# DB_URI = "postgresql://postgres:bit@192.168.100.233:5432/postgres"
# with PostgresSaver.from_conn_string(DB_URI) as checkpointer:  # checkpointer 是一个链接好存储库

# 第一次使用postgres存储库需要执行一下.setup()
# checkpointer.setup()

agent_search = agent_builder.compile(checkpointer=checkpointer)

# 执行图
# 通过配置的方式将线程id传递给单次执行中
config = {"configurable":{"thread_id":"2222"}}

# 模拟第一次执行
result = agent_search.invoke(
    {"messages": [HumanMessage(content="今天西安的天气如何？")]},
    config=config
)
# # result 是最终的状态结果
result["messages"][-1].pretty_print()

# 第二次执行
# result = agent_search.invoke({
#     "messages": [HumanMessage(content="刚才我们聊了什么？")]
# }, config=config)
# # result 是最终的状态结果
# for r in result["messages"]:
#     r.pretty_print()

# 获取一下最新的状态快照
print(agent_search.get_state(config))

# 历史快照：按照时间顺序，最新的排在前面
print(agent_search.get_state_history(config))

to_replay = None
new_config = None
for snapshot in agent_search.get_state_history(config):
    # print("checkpointer_id: ", snapshot.config["configurable"]["checkpoint_id"])
    # print("下一个节点：", snapshot.next)
    # print("\n")
    # if snapshot.config["configurable"]["checkpoint_id"] == "1f0f75d0-15af-6819-8005-5329d06cd836":
    #     # print("state: ", snapshot.values["messages"][-1])
    #     new_config = agent_search.update_state(
    #         snapshot.config,
    #         {"messages":[HumanMessage(content="我们之前聊过宠物相关的话题吗？")]}
    #     )
    #     print(new_config)
    #     to_play = snapshot

    if snapshot.next == ("llm_call",):  # 根据你实际图结构判断
        new_config = agent_search.update_state(
            snapshot.config,
            {"messages": [HumanMessage(content="我们之前聊过宠物相关的话题吗？")]},
        )
        break

# 重放（从指定的快照开始执行）
# 参数1：state设置为None，因为重放可以从快照中获取state
# 参数2：要重放的config，里面包含了线程id，快照id
# result2 = agent_search.invoke(None,config=new_config)
# print(result2["messages"][-1])

if new_config is not None:
    result2 = agent_search.invoke(None, config=new_config)
    print(result2["messages"][-1])
else:
    print("没有匹配到用于分叉的快照")