# 流式传输
import os
import asyncio
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model = "deepseek-v4-flash",
    api_key = os.environ.get("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com",
)

# 非流式输出
# print(model.invoke("写一篇关于薛定谔的猫的短篇故事，字数在100字以内"))

# 同步流式输出
# chunk: AIMessageChunk
# 返回一个迭代器，产生的消息块
# chunks = []
# for chunk in  model.stream("写一篇关于薛定谔的猫的短篇故事，字数在100字以内"):
#     chunks.append(chunk)
#     # print(chunk.content, end=" ", flush=True)
#
# tmp_chunks = chunks[0] + chunks[1] + chunks[2] +chunks[3]
# print(tmp_chunks)

# 异步流式输出
async def async_stream():
    print("===异步调用===")
    async for chunk in model.astream("写一篇关于薛定谔的猫的短篇故事，字数在100字以内"):
        print(chunk.content,end=" ",flush=True)

asyncio.run(async_stream())
