import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

model = ChatOpenAI(
    model='deepseek-v4-flash',
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

# 结构化输出常见使用场景：与工具结合使用

tool = TavilySearch(max_results=4)

model_with_tools = model.bind_tools([tool])

messages = [
    HumanMessage("北京今天的天气怎么样？")
]
ai_message = model_with_tools.invoke(messages)
messages.append(ai_message)

for tool_call in ai_message.tool_calls:
    tool_message = tool.invoke(tool_call)
    messages.append(tool_message)

class SearchResult(BaseModel):
    """结构化搜索对象"""

    query: str = Field(description="搜索查询")
    findings: str = Field(description="查询结果摘要")

model_with_structured = model_with_tools.with_structured_output(SearchResult)
print(model_with_structured.invoke(messages))