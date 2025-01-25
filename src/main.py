import logging
from vectorize_and_store import initialize_weaviate, vectorize_and_store_txt_files
from search import search_similar_documents, close_weaviate_client

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    client = None
    try:
        # 初始化 Weaviate 并创建 Collection
        client = initialize_weaviate()

        # 向量化并存储 .txt 文件
        txt_files_directory = "data"  # 存放 .txt 文件的目录
        logger.info(f"Starting to process directory: {txt_files_directory}")

        # 配置分段策略
        strategy = "paragraphs"  # 可选：fixed_length, sentences, paragraphs
        chunk_size = 200  # 仅当 strategy 为 fixed_length 时有效

        vectorize_and_store_txt_files(txt_files_directory, client, strategy=strategy, chunk_size=chunk_size)

        # 检索与查询字符串最相似的文档分段
        query = "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. They were the last people you'd expect to be involved in anything strange or mysterious, because they just didn't hold with such nonsense."
        threshold = 0.2  # 设置阈值
        logger.info(f"Starting search for query: {query} with threshold: {threshold}")
        similar_docs = search_similar_documents(query, threshold=threshold)
        
        # 输出搜索结果
        logger.info("Search results:")
        for doc in similar_docs:
            logger.info(f"Filename: {doc.properties['filename']}")
            logger.info(f"Chunk ID: {doc.properties['chunk_id']}")
            logger.info(f"Content: {doc.properties['content'][:200]}...")  # 只打印前200个字符
            logger.info(f"Distance: {doc.metadata.distance}")
            logger.info("-" * 40)
    finally:
        # 确保客户端连接被关闭
        if client is not None:
            close_weaviate_client(client)

if __name__ == "__main__":
    main()