import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated
from langchain_core.tools import tool


@tool
def add(
        x: Annotated[int,...,'第一个整数'],
        y: Annotated[int,...,'第二个整数'],
)->int:
    """两数相加"""
    return x + y

@tool
def multiply(
        x:Annotated[int,...,'第一个整数'],
        y:Annotated[int,...,'第二个整数'],
)->int:
    """两数相乘"""
    return x * y

model = ChatOpenAI(
    model = "deepseek-v4-flash",
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

# 绑定工具
tools = [add, multiply]
model_with_tools = model.bind_tools(tools=tools)

# 强制选择工具
# model_with_tools = model.bind_tools(tools=tools,tool_choice="any")

# 调用工具
# print(model_with_tools.invoke("2乘以3等于多少?"))
# print(model_with_tools.invoke("who are you?"))
# 模型在没有强制选择工具的情况下，会根据问题来决定是否使用工具

# 定义消息列表，添加要传递给聊天模型的消息
messages = [
    HumanMessage("2乘以3等于多少？6加3等于多少？")
]
ai_msg = model_with_tools.invoke(messages)
# print(ai_msg)
messages.append(ai_msg)

# 构造ToolMessage,并添加到消息列表中去
for tool_call in ai_msg.tool_calls:
    selected_tool = {"add":add,"multiply":multiply}[tool_call['name'].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

print(messages)
print(model_with_tools.invoke(messages).content)

# tool_result = multiply.invoke(ai_msg.tool_calls[0])
# print(tool_result)