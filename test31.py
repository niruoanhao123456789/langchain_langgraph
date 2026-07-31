from typing import List

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.runnables import chain
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import CharacterTextSplitter

embeddings = DashScopeEmbeddings(model="text-embedding-v4")

vector_store = InMemoryVectorStore(embedding=embeddings)

loader = UnstructuredMarkdownLoader("docs/markdown/脚手架级微服务租房平台Q&A.md")

data = loader.load()

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", # cl100k_base 是tiktoken 分词器中的一种编码方式
    chunk_size=400,              # 块token大小(参考标准，为了保证段落/句子完整，会超出此设定的大小)
    chunk_overlap=50,            # 块重叠大小
)

docs = text_splitter.split_documents(data)

ids = vector_store.add_documents(docs)
print(f"共有{len(docs)}个文档，编排了{len(ids)}个索引")

# 检索器依赖向量库(Runnable)
# retriever = vector_store.as_retriever(search_kwargs={"k":2})

# 使用@chain，定义检索器函数，当作具有Runnable的"检索器"使用
@chain
def retriever(query:str) -> List[Document]:
    return vector_store.similarity_search(query=query,k=2)

search_docs = retriever.invoke("项目介绍")
for doc in search_docs:
    print("*" * 30)
    print(doc.page_content)