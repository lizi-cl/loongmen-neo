import os
import glob
import ollama
import weaviate
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def initialize_weaviate():
    """初始化 Weaviate 客户端并创建 schema"""
    logger.info("Initializing Weaviate client...")
    client = weaviate.Client("http://localhost:8080")
    logger.info("Weaviate client initialized.")

    # 定义 Weaviate 的 schema
    schema = {
        "classes": [
            {
                "class": "Document",
                "description": "A document with text content",
                "properties": [
                    {
                        "name": "filename",
                        "dataType": ["string"],
                        "description": "The name of the file",
                    },
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "The content of the document",
                    },
                    {
                        "name": "vector",
                        "dataType": ["number[]"],
                        "description": "The embedding vector of the document",
                    },
                ],
            }
        ]
    }

    # 创建 Weaviate schema
    logger.info("Creating Weaviate schema...")
    client.schema.create(schema)
    logger.info("Weaviate schema created.")
    return client

def vectorize_and_store_txt_files(directory, client):
    """读取并向量化所有 .txt 文件，存储到 Weaviate"""
    logger.info(f"Starting to vectorize and store .txt files from directory: {directory}")
    for filepath in glob.glob(os.path.join(directory, "*.txt")):
        logger.info(f"Processing file: {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            filename = os.path.basename(filepath)
            
            # 使用 Ollama 生成嵌入向量
            logger.info(f"Generating embedding for file: {filename}")
            embedding = ollama.embed("bge-m3", content)
            logger.info(f"Embedding generated for file: {filename}")
            
            # 将文档存储到 Weaviate
            logger.info(f"Storing document in Weaviate: {filename}")
            client.data_object.create(
                data_object={
                    "filename": filename,
                    "content": content,
                    "vector": embedding,
                },
                class_name="Document",
            )
            logger.info(f"Document stored in Weaviate: {filename}")
    logger.info("Finished vectorizing and storing .txt files.")