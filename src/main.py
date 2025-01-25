import logging
from vectorize_and_store import initialize_weaviate, vectorize_and_store_txt_files
from search import search_similar_documents

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    # 初始化 Weaviate 并创建 schema
    client = initialize_weaviate()

    # 向量化并存储 .txt 文件
    txt_files_directory = "data"  # 存放 .txt 文件的目录
    logger.info(f"Starting to process directory: {txt_files_directory}")
    vectorize_and_store_txt_files(txt_files_directory, client)

    # 检索与查询字符串最相似的文档
    query = "This is a sample query string."
    logger.info(f"Starting search for query: {query}")
    similar_docs = search_similar_documents(query)
    
    # 输出搜索结果
    logger.info("Search results:")
    for doc in similar_docs:
        logger.info(f"Filename: {doc['filename']}")
        logger.info(f"Content: {doc['content'][:200]}...")  # 只打印前200个字符
        logger.info("-" * 40)

if __name__ == "__main__":
    main()