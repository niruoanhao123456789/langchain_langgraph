from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from pydantic_core.core_schema import arguments_schema

# 1.
# def add(x:int,y:int)->int:
#     """两数相加
#
#     Args:
#         x: 第一个整数
#         y: 第二个整数
#     """
#     return x + y
#
# add_tool = StructuredTool.from_function(func= add)

# 2. 只有结果的返回
# class addInput(BaseModel):
#     x:int = Field(...,description="第一个整数")
#     y:int = Field(...,description="第二个整数")
#
# def add(x:int,y:int)->int:
#     return x+y
#
# add_tool = StructuredTool.from_function(
#     func = add,
#     description='两数相加',
#     arguments_schema=addInput
# )
#
# print(add_tool.invoke({'x':1,'y':2}))

# 3. 返回过程与结果
class addInput(BaseModel):
    x:int = Field(...,description="第一个整数")
    y:int = Field(...,description="第二个整数")

def add(x:int,y:int)->tuple[str,list[int]]:
    nums = [x,y]
    content = f"{nums} 相加结果是{x+y}"
    return content,nums

add_tool = StructuredTool.from_function(
    func = add,
    description='两数相加',
    arguments_schema=addInput,
    response_format='content_and_artifact',
)

print(add_tool.invoke(
    {
        "name": "add",
        "args": {'x': 3, 'y': 6},
        "type": "tool_call",  # 必填
        'id': "111",  # 必填，用来将工具调用请求和结果关联起来
    }
))

#print(add_tool.invoke({'x':1,'y':2}))