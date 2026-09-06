from typing import Optional

from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek

# 输出解析器

# 定义聊天模型
model = ChatDeepSeek(model="deepseek-v4-flash")

# Pydantic 对象
class Joke(BaseModel):
    """给用户讲的一个笑话"""

    setup : str = Field(description="这个笑话的开头")
    punchline : str = Field(description="这个笑话的妙语")
    rating : Optional[int] = Field(default=None,description="从1-10分给这个笑话打分")

# 定义解析器
#parser = PydanticOutputParser(pydantic_object=Joke)

# JSON Schema 不好写
parser = JsonOutputParser(pydantic_object=Joke)

# 提示词模板
prompt = PromptTemplate(
    template="回复用户问题。\n返回结构说明：{format_instructions}\n用户问题：{query}\n",
    partial_variables={"format_instructions": parser.get_format_instructions()},  # 将返回的结构作为提示词发送给大模型
    input_variables=["query"],
)

# 定义链
chain = prompt | model | parser
print(chain.invoke({"query":"将一个关于薛定谔的猫的笑话"}))