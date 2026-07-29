from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

# single 模式，只生成一个大文档
# 即model 默认为 "single"
loader = UnstructuredMarkdownLoader("docs/markdown/脚手架级微服务租房平台Q&A.md")
# Document列表
data = loader.load()

# 基于字符长度进行的拆分
# 定义文本分割器
# text_splitter = CharacterTextSplitter(
#     separator="\n\n",         # 分割符。一般来说，有一个默认的分割符优先级列表：["\n\n", "\n", " "]
#     chunk_size=400,           # 块大小(参考标准，为了保证段落/句子完整，会超出此设定的大小)
#     chunk_overlap=50,         # 块重叠大小
#     length_function=len,      # 测量字符长度的函数
#     is_separator_regex=False, # 是否正则表达式描写分隔符
# )

# 基于token长度划分
# text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
#     encoding_name="cl100k_base",     # cl100k_base 是tiktoken 分词器中的一种编码方式
#     chunk_size = 400,                # 块token大小(参考标准，为了保证段落/句子完整，会超出此设定的大小)
#     chunk_overlap=50,                # 块重叠大小
# )

# 利用递归形式的文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " "],        # 分割符。一般来说，有一个默认的分割符优先级列表：["\n\n", "\n", " "]
    chunk_size=100,          # 块大小(参考标准，为了保证段落/句子完整，会超出此设定的大小)
    chunk_overlap=0,        # 块重叠大小
    length_function=len,     # 测量字符长度的函数
    is_separator_regex=False,# 是否正则表达式描写分隔符吗？
)

documents = text_splitter.split_documents(data)
for document in documents[:10]:
    print("*" * 30)
    print(document)