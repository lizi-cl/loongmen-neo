import ollama
import weaviate
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def search_similar_documents(query, top_k=5):
    """检索与查询字符串最相似的文档"""
    logger.info(f"Starting search for query: {query}")
    
    # 初始化 Weaviate 客户端
    client = weaviate.Client("http://localhost:8080")
    
    # 生成查询字符串的嵌入向量
    logger.info("Generating embedding for query...")
    query_embedding = ollama.embed("bge-m3", query)
    logger.info("Embedding generated for query.")
    
    # 在 Weaviate 中执行向量搜索
    logger.info("Executing vector search in Weaviate...")
    result = client.query.get(
        "Document", ["filename", "content"]
    ).with_near_vector(
        {"vector": query_embedding, "certainty": 0.7}
    ).with_limit(top_k).do()
    
    logger.info("Vector search completed.")
    return result["data"]["Get"]["Document"]