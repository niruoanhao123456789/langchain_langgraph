from langchain_deepseek import ChatDeepSeek
from langsmith import Client
import os

client = Client()
# prompt 就是一个提示词模板 ， Runnable 实例
prompt = client.pull_prompt(
    "hardkothari/prompt-maker:c5db8eee",
    dangerously_pull_public_prompt=True
)

model = ChatDeepSeek(model = "deepseek-v4-flash")

chain = prompt | model

while True:
    task = input("\n你的任务是什么？ （输入 quit 退出聊天）\n")
    if task == 'quit':
        break

    lazy_prompt = input("\n你当前任务对应的提示词是什么？ （输入 quit 退出聊天）\n")
    if lazy_prompt == 'quit':
        break

    chain.invoke({"task": task, "lazy_prompt": lazy_prompt}).pretty_print()