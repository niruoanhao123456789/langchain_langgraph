# 同步IO
import  time

def boil_water():
    print("开始烧水...")
    time.sleep(5)       # 模拟烧水5s, CPU 完全空闲
    print("烧水结束...")

def send_message():
    print("开始发消息...")
    time.sleep(2)
    print("发消息完成...")

def main():
    boil_water()
    send_message()

# 共耗时7s
main()

# 异步IO
import asyncio

# 协程
async def boil_water_async():
    print("开始烧水...")
    await asyncio.sleep(5)
    print("烧水结束...")

async def send_message_async():
    print("开始发消息...")
    await asyncio.sleep(2)
    print("发消息完成...")

async def main_async():
    task1 = asyncio.create_task(boil_water_async())
    task2 = asyncio.create_task(send_message_async())
    await task1
    await task2

# 5s
asyncio.run(main_async())