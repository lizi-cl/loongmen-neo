import ollama
import weaviate
import logging
import weaviate.classes as wvc
from weaviate.embedded import EmbeddedOptions

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def search_similar_documents(query, client ,top_k=5, threshold=0.5):
    """检索与查询字符串最相似的文档分段"""
    logger.info(f"Starting search for query: {query}")
     
    # 生成查询字符串的嵌入向量
    logger.info("Generating embedding for query...")
    # 使用 Ollama 生成嵌入向量
    embedding_result = ollama.embed("bge-m3", query)
                
    # 提取嵌入向量
    embedding = embedding_result.get('embeddings', [])[0] if embedding_result and 'embeddings' in embedding_result else None
    
    # 检查并提取向量
    if isinstance(embedding, dict) and "embedding" in embedding:
        vector = embedding["embedding"]
    else:
        vector = embedding  # 假设直接返回向量
    
    # 确保向量是一维浮点数列表
    if not isinstance(vector, list) or not all(isinstance(x, float) for x in vector):
        logger.error(f"Invalid query vector format: {vector}")
        return []
    
    logger.info("Embedding generated for query.")
    
    # 获取 Collection
    documents = client.collections.get("Document")
    
    # 在 Weaviate 中执行向量搜索
    logger.info(f"Executing vector search in Weaviate... ")
    response = documents.query.near_vector(
        near_vector=vector,
        distance=threshold,
        return_metadata=wvc.query.MetadataQuery(distance=True),
        limit=top_k
    )
    
    logger.info("Vector search completed.")
    return response.objects

def close_weaviate_client(client):
    """关闭 Weaviate 客户端"""
    client.close()
    logger.info("Weaviate client closed.")