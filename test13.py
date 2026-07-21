from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from typing import Iterator, List

# 自定义输出格式

# 组件1: 聊天模型
model = ChatDeepSeek(model="deepseek-v4-flash")

# 组件2: 输出解析器
parser = StrOutputParser()

# 组件3: 自定义生成器
def split_into_list(input: Iterator[str])->Iterator[List[str]]:
    buffer = ""
    for chunk in input:
        buffer += chunk
        # 设为遇到。就需要刷新
        while "。" in buffer:
            # 找到句号的位置
            stop_index = buffer.index("。")
            # yield 用于创造生成器
            yield [buffer[:stop_index + 1].strip()]
            buffer = buffer[stop_index + 1:]
    # 处理buffer最后几个字
    yield [buffer.strip()]

# 定义链
chain = model | parser | split_into_list

# 返回一个迭代器，产生的消息块
for chunk in chain.stream("写一段关于爱情的歌词，共5句话，每句用中文句号“。”隔开"):
    print(chunk,end=" ",flush=True)