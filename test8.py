from typing import Optional, List, Union, TypedDict

from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field

model = ChatDeepSeek(model='deepseek-chat')

# 聊天模型提供的结构化输出能力

# 结构化返回 Pydantic
# class Joke(BaseModel):
#     """给用户讲的一个笑话"""
#     setup:str = Field(description="笑话的开头")
#     punchline: str = Field(description='笑话的妙语')
#     rating: Optional[int] = Field(default=None,description="从1-10分，给这个笑话评分")
#
# class Data(BaseModel):
#     """获取关于笑话的数据列表"""
#     jokes: List[Joke]
#
# # print(model.invoke("讲一个关于薛定谔的猫的笑话").content)
# #
# model_with_structured = model.with_structured_output(Data)
# print(model_with_structured.invoke("讲一个关于薛定谔的猫的笑话"))


# 结构化返回 TypedDict
# class Joke(TypedDict):
#     """给用户讲的一个笑话"""
#     setup:str = Field(description="笑话的开头")
#     punchline: str = Field(description='笑话的妙语')
#     rating: Optional[int] = Field(description="从1-10分，给这个笑话评分")
#
# model_with_structured = model.with_structured_output(Joke,include_raw=True)
# print(model_with_structured.invoke("讲一个关于薛定谔的猫的笑话"))


# 结构化返回 JSON Schema
# json_schema = {
#     "title": "joke",
#     "description": "给用户讲一个笑话。",
#     "type": "object",
#     "properties": {
#         "setup": {
#             "type": "string",
#             "description": "这个笑话的开头",
#         },
#         "punchline": {
#             "type": "string",
#             "description": "这个笑话的妙语",
#         },
#         "rating": {
#             "type": "integer",
#             "description": "从1到10分，给这个笑话评分",
#             "default": None,
#         },
#     },
#     "required": ["setup", "punchline"],
# }
#
# model_with_structured = model.with_structured_output(json_schema)
# print(model_with_structured.invoke("讲一个关于薛定谔的猫的笑话"))
# print(model_with_structured.invoke("who are you ?"))


# 结构选择
class Joke(BaseModel):
    """给用户讲的一个笑话"""

    setup: str = Field(description="这个笑话的开头")
    punchline: str = Field(description="这个笑话的妙语")
    rating: Optional[int] = Field(default=None, description="从1-10分，给这个笑话评分")

class Response(BaseModel):
    """以对话的方式回应"""

    content: str = Field(description="用于对用户查询的会话响应")

class FinalResponse(BaseModel):
    """最终回复，选择合适的输出结构"""

    final_output: Union[Joke, Response]

model_with_structured = model.with_structured_output(FinalResponse)
print(model_with_structured.invoke("讲一个关于薛定谔的猫的笑话"))
print(model_with_structured.invoke("你是谁？"))