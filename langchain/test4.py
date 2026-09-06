from langchain_core.tools import tool
from pydantic import BaseModel,Field
from typing_extensions import Annotated

# 1.
# @tool
# def add(x:int,y:int)->int:
#     '''两数相加
#
#     Args:
#         x: 第一个整数
#         y: 第二个整数
#     '''
#     return x + y


# 2.
# class AddInput(BaseModel):
#     '''两数相加'''
#
#     x : int = Field(...,description='第一个整数')
#     y : int = Field(...,description='第二个整数')
#
#
# @tool(args_schema=AddInput)
# def add(x:int,y:int)->int:
#     return x+y


# 3.
@tool
def add(
    x:Annotated[int,...,'第一个整数'],
    y:Annotated[int,...,'第二个整数'],
)->int:
    """两数相加

    Args:
        x: 第一个整数
        y: 第二个整数
    """
    return x + y


print(add.invoke({'x':1,'y':2}))
print(add.name)
print(add.description)
print(add.args)