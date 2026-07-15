from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

# 1. 基本用法
# langchain 封装了更上层的方法，用于初始化各类模型
# gdp_model = init_chat_model("gpt-4o-mini",model_provider = 'openai')
# deepseek_model = init_chat_model('deepseek-chat',model_provider = 'deepseek')
#
# print(deepseek_model.invoke('hello'))

# 2. 定制可配置的模型（模型模拟器）
# config_model = init_chat_model(temperature = 0.3)
# messages = [
#     SystemMessage(content="请补全一段故事，50字以内"),
#     HumanMessage(content="薛定谔的猫"),
# ]
# # .invoke()的config参数才真正定义了模型
# print(f'config_model = {config_model.invoke(input=messages,config={'configurable':{'model':'deepseek-chat'}}).content}')

# 3. 可配置的模型（默认参数）
# 原本输出
# 精简输出
# model = init_chat_model(
#     model = 'deepseek-chat',
#     temperature = 0.5,
#     max_tokens = 1024,
#     configurable_fields = ('temperature', 'max_tokens'),
#     config_prefix = 'first'
# )
#
# messages = [
#     SystemMessage(content="请补全一段故事，50字以内"),
#     HumanMessage(content="薛定谔的猫"),
# ]
#
# print(model.invoke(messages).content)
#
# result = model.invoke(
#     input = messages,
#     config = {
#         'configurable':
#         {
#             'first_temperature': 0,
#             'first_max_tokens': 10,
#         }
#     }
# )
#
# print(result.content)