import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import CHROMA_DB_DIR, DEEPSEEK_API_BASE, DEEPSEEK_API_KEY, EMBED_MODEL_NAME, LLM_MODEL_NAME
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)

vectorstore = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings,
    collection_name="langchain_rag",
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(
    model=LLM_MODEL_NAME,
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_BASE,
    temperature=0.1,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "请根据下面的参考资料回答。资料里没有的内容，就说明资料中没有。\n\n参考资料：\n{context}"),
    ("user", "{question}"),
])
parser = StrOutputParser()
chain = prompt | llm | parser

def ask_question(question: str):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    return chain.invoke({"context": context, "question": question})

def stream_answer(question: str):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    for chunk in chain.stream({"context": context, "question": question}):
        yield chunk


'''import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from .config import CHROMA_DB_DIR, EMBED_MODEL_NAME, DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, LLM_MODEL_NAME

# 初始化模型
Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
Settings.llm = OpenAI(
    model=LLM_MODEL_NAME,
    api_base=DEEPSEEK_API_BASE,
    api_key=DEEPSEEK_API_KEY,
    is_chat_model=True,
    context_window=32000,
    temperature=0.1
)

def get_query_engine():
    # 连接刚才存好的向量库
    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = db.get_or_create_collection("my_rag_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # 构建查询引擎
    index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = index.as_query_engine(similarity_top_k=3)
    return query_engine

def ask_question(question: str):
    query_engine = get_query_engine()
    response = query_engine.query(question)
    return str(response)
'''