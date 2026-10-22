from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(model = "deepseek-flash")

store = {}
# 根据会话 id 查询会话里的消息列表
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # InMemoryChatMessageHistory() 帮助我们将AIMessage、HumanMessage等消息自动添加进来
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_history_message_model = RunnableWithMessageHistory(model,get_session_history)

# model: Runnable 实例
# invoke: config: 配置 Runnable 实例
config = {"configurable":{"session_id":"1"}}

with_history_message_model.invoke(
    [HumanMessage(content="我是小明，你好!")],
    config = config
).pretty_print()

with_history_message_model.invoke(
    [HumanMessage(content="你知道我是谁吗？")],
    config = config,
).pretty_print()