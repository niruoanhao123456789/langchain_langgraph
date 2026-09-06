from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, merge_message_runs

model = ChatDeepSeek(model = "deepseek-v4-flash")

# 消息合并

messages = [
    SystemMessage("你是一个聊天助手。"),
    SystemMessage("你总是以笑话回应。"),
    HumanMessage("为什么要使用 LangChain?"),
    HumanMessage("为什么要使用 LangGraph?"),
    AIMessage("因为当你试图让你的代码更有条理时，LangGraph 会让你感到“节点”是个好主意！"),
    AIMessage("不过别担心，它不会“分散”你的注意力！"),
    HumanMessage("选择LangChain还是LangGraph?"),
]

# 方式1
# merger_message = merge_message_runs(messages)
# model.invoke(merger_message).pretty_print()

# 方式2
merger = merge_message_runs()
chain = merger | model
chain.invoke(messages).pretty_print()