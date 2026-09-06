from typing import Optional, List

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import tool_example_to_messages
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field

model = ChatDeepSeek(model = "deepseek-v4-flash")

# 1. 定义结构化输出
class Person(BaseModel):
    """一个人的信息"""

    # 注意:
    # 1. 每个字段都是 Optional “可选的” —— 允许 LLM 在不知道答案时输出 None。
    # 2. 每个字段都有一个 description “描述” —— LLM使用这个描述。
    # 有一个好的描述可以帮助提高提取结果。
    name: Optional[str] = Field(default=None, description="这个人的名字")
    hair_color: Optional[str] = Field(default=None, description="如果知道这个人头发的颜色")
    skin_color: Optional[str] = Field(default=None, description="如果知道这个人的肤色")
    height_in_meters: Optional[str] = Field(default=None, description="以米为单位的高度")

class Data(BaseModel):
    """人物列表数据"""
    people: List[Person] = Field(description="人物列表")

# 2. 定义示例（不是 Message）
examples = [
    (
        "海洋是广阔的、蓝色的。它有两万多英尺深",
        Data(people=[])
    ),
    (
        "小明在跳舞,1米78的身高看起来很灵活",
        Data(people=[
            Person(name='小明', hair_color=None, skin_color=None, height_in_meters='1.78'),
        ]),
    )
]

# 3. 定义提示词模板
prompt_template = ChatPromptTemplate(
    [
        SystemMessage(content="你是一个提取信息的专家，只从文本中提取相关信息。如果您不知道要提取的属性的值，属性值返回null"),
        MessagesPlaceholder("example_messages"), # 消息占位符，将示例转换为Message后插入进来
        ("user", "{new_message}"),
    ]
)

# 4. 将实例转换为Messages
example_messages = []
for txt,tool_call in examples:
    if tool_call.people:
        ai_response = "检测到人"
    else:
        ai_response = "未检测到人"
    example_messages.extend(tool_example_to_messages(
        txt, # 示例的输入
        [tool_call], # (工具 Data(people=[]) 准确的参考标准)
        ai_response=ai_response # 让 LLM 强制返回ai_response
    ))

# print(example_messages)
# # 结果
# [
#     HumanMessage(content='海洋是广阔的、蓝色的。它有两万多英尺深', additional_kwargs={}, response_metadata={}),
#     AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'e938c190-e7c3-4a5d-ab74-470db300ec50', 'type': 'function', 'function': {'name': 'Data', 'arguments': '{"people":[]}'}}]}, response_metadata={}, tool_calls=[{'name': 'Data', 'args': {'people': []}, 'id': 'e938c190-e7c3-4a5d-ab74-470db300ec50', 'type': 'tool_call'}], invalid_tool_calls=[]),
#     ToolMessage(content='You have correctly called this tool.', tool_call_id='e938c190-e7c3-4a5d-ab74-470db300ec50'),
#     AIMessage(content='未检测到人', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]),
#     HumanMessage(content='小明在跳舞,1米78的身高看起来很灵活', additional_kwargs={}, response_metadata={}),
#     AIMessage(content='', additional_kwargs={'tool_calls': [{'id': '17ad246b-f678-4631-8865-c973b2434288', 'type': 'function', 'function': {'name': 'Data', 'arguments': '{"people":[{"name":"小明","hair_color":null,"skin_color":null,"height_in_meters":"1.78"}]}'}}]}, response_metadata={}, tool_calls=[{'name': 'Data', 'args': {'people': [{'name': '小明', 'hair_color': None, 'skin_color': None, 'height_in_meters': '1.78'}]}, 'id': '17ad246b-f678-4631-8865-c973b2434288', 'type': 'tool_call'}], invalid_tool_calls=[]),
#     ToolMessage(content='You have correctly called this tool.', tool_call_id='17ad246b-f678-4631-8865-c973b2434288'), AIMessage(content='检测到人', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[])
# ]

# 5. 定义的结构化模型
structured_model = model.with_structured_output(schema=Data)

# 6. 定义链(没有强制结构化输出)
chain = prompt_template | model
chain.invoke(
    {
        "example_messages": example_messages,
        "new_message": "篮球场上，身高两米的中锋王伟默契地将球传给一米七的后卫挚友李明，完成一记绝杀。这对老友用十年配合弥补了身高的差距。"
    }
).pretty_print()
