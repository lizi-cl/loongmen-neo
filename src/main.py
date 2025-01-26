import logging
import weaviate
from weaviate.classes.query import Filter
from vectorize_and_store import vectorize_and_store_txt_files
from search import search_similar_documents, close_weaviate_client
from weaviate.embedded import EmbeddedOptions
from weaviate.classes.config import Property, DataType

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def initialize_weaviate(vec=False):
    """初始化 Weaviate 客户端并创建 Collection"""
    logger.info("Initializing Weaviate client...")
    
    # 连接到本地 Weaviate 实例
    client = weaviate.WeaviateClient(
        embedded_options=EmbeddedOptions(
            binary_path="./bin/",
            persistence_data_path="./weaviate_db/",
        )
    )
    client.connect()
    logger.info("Weaviate client initialized.")
    if vec==True:
        # 检查 Collection 是否已存在
        if client.collections.exists("Document"):
            logger.info("Collection 'Document' already exists.")
        else:
            # 定义 Collection 的 Schema
            schema = {
                "class": "Document",
                "properties": [
                    Property(name="filename", data_type=DataType.TEXT),
                    Property(name="chunk_id", data_type=DataType.INT),
                    Property(name="content", data_type=DataType.TEXT),
                ],
            }

            # 创建 Collection
            logger.info("Creating Collection...")
            client.collections.create(
                name="Document",
                properties=schema["properties"]
            )
            logger.info("Collection created.")

    return client

def vectorize_and_store():
    # 初始化 Weaviate 并创建 Collection
    client = initialize_weaviate(True)

    collection = client.collections.get("Document")

    # 删除所有文档
    response = collection.data.delete_many(
        where=Filter.by_property("property_name").like("*")
    )

    # 向量化并存储 .txt 文件
    txt_files_directory = "data"  # 存放 .txt 文件的目录
    logger.info(f"Starting to process directory: {txt_files_directory}")

    # 配置分段策略
    strategy = "paragraphs"  # 可选：fixed_length, sentences, paragraphs
    chunk_size = 200  # 仅当 strategy 为 fixed_length 时有效

    vectorize_and_store_txt_files(txt_files_directory, client, strategy=strategy, chunk_size=chunk_size)

    # 关闭 Weaviate 客户端连接
    close_weaviate_client(client)

def search(query, threshold=0.2):
    # 初始化 Weaviate 并创建 Collection
    client = initialize_weaviate(False)

    # 检索与查询字符串最相似的文档分段
    logger.info(f"Starting search for query: {query} with threshold: {threshold}")
    similar_docs = search_similar_documents(query, client ,threshold=threshold)
    
    # 输出搜索结果
    logger.info("Search results:")
    for doc in similar_docs:
        logger.info(f"Filename: {doc.properties['filename']}")
        logger.info(f"Chunk ID: {doc.properties['chunk_id']}")
        logger.info(f"Content: {doc.properties['content'][:200]}...")  # 只打印前200个字符
        logger.info(f"Distance: {doc.metadata.distance}")
        logger.info("-" * 40)

    # 关闭 Weaviate 客户端连接
    close_weaviate_client(client)


def main():
    # Step1 : 向量化并存储 .txt 文件
    vectorize_and_store()

    # Step2 : 检索与查询字符串最相似的文档分段
    query = "Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. They were the last people you'd expect to be involved in anything strange"
    search(query)

if __name__ == "__main__":
    main()