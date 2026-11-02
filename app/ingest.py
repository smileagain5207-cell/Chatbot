import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

'''
import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
'''
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from .config import DATA_DIR, CHROMA_DB_DIR, EMBED_MODEL_NAME

'''
def ingest_documents():
    print("正在加载本地嵌入模型...")
    # 设置全局嵌入模型
    HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)

    print("正在读取文档...")
    # 读取 data 目录下的所有文档
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    if not documents:
        print("data 目录下没有文档，请放入 pdf 或 txt 文件！")
        return

    print("正在存入向量数据库...")
    # 初始化 ChromaDB
    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = db.get_or_create_collection("langchain_rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 构建索引并存储
    VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    print(f"成功入库！共处理 {len(documents)} 个文档片段。")
'''


def ingest_documents():
    print("正在加载本地嵌入模型...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)

    print("正在读取文档...")
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    if not documents:
        print("data 目录下没有文档，请放入 pdf 或 txt 文件！")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = splitter.split_documents(documents)

    print("正在存入向量数据库...")
    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
        collection_name="langchain_rag",
    )
    print(f"成功入库！共处理 {len(splits)} 个文档片段。")
    
if __name__ == "__main__":
    ingest_documents()


