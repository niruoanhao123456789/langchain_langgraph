import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

# 1. 定义模型
model = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
    temperature = 2
)

# 2. 定义消息
#    用户消息 HumanMessage
#    系统消息 SystemMessage  通常作为第一条消息传入
#    AI消息 AIMessage
messages = [
    SystemMessage(content="请补全一段故事，50字以内"),
    HumanMessage(content="薛定谔的猫"),
]

# 3. 调用大模型
# result = model.invoke(messages)
# print(result)  # 打印内容

# 4. 输出解析器
parser = StrOutputParser()
# print(parser.invoke(result))

# 5. 定义链并调用
chain = model | parser
# chain = RunnableSequence(first=model,last=parser)
# chain = model.pipe(parser)
print(chain.invoke(messages))