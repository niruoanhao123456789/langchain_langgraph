from langchain_openai import OpenAIEmbeddings

# 定义嵌入模型
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",

)

# 将query转换成向量表示
query_vector = embeddings.embed_query("你好")
print(f"text-embedding-3-large 向量维度：{len(query_vector)}")
print(f"向量前五个数值：{query_vector[:5]}")