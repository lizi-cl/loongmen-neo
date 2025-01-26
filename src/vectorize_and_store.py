import os
import glob
import ollama
import weaviate
import logging
from weaviate.embedded import EmbeddedOptions
from weaviate.classes.config import Property, DataType

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def split_by_fixed_length(text, chunk_size=200):
    """按固定长度分段"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def split_by_sentences(text):
    """按句子分段"""
    from nltk.tokenize import sent_tokenize
    return sent_tokenize(text)

def split_by_paragraphs(text):
    """按段落分段"""
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def split_text_into_chunks(text, strategy="fixed_length", **kwargs):
    """根据策略将文本分段"""
    if strategy == "fixed_length":
        return split_by_fixed_length(text, **kwargs)
    elif strategy == "sentences":
        return split_by_sentences(text)
    elif strategy == "paragraphs":
        return split_by_paragraphs(text)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def vectorize_and_store_txt_files(directory, client, strategy="fixed_length", **kwargs):
    """读取并向量化所有 .txt 文件，存储到 Weaviate"""
    logger.info(f"Starting to vectorize and store .txt files from directory: {directory}")
    for filepath in glob.glob(os.path.join(directory, "*.txt")):
        logger.info(f"Processing file: {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            filename = os.path.basename(filepath)
            
            # 将文本分段
            chunks = split_text_into_chunks(content, strategy=strategy, **kwargs)
            logger.info(f"Split file into {len(chunks)} chunks using strategy: {strategy}")
            
            # 获取 Collection
            documents = client.collections.get("Document")
            
            # 对每个分段生成嵌入向量并存储
            for chunk_id, chunk in enumerate(chunks):
                logger.info(f"Generating embedding for chunk {chunk_id + 1} of file: {filename}")
                
                # 使用 Ollama 生成嵌入向量
                embedding_result = ollama.embed("bge-m3", chunk)
                
                # 提取嵌入向量
                embedding = embedding_result.get('embeddings', [])[0] if embedding_result and 'embeddings' in embedding_result else None
                
                # 确保向量是一维浮点数列表
                if not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
                    logger.error(f"Invalid vector format for chunk {chunk_id + 1}: {embedding}")
                    continue
                
                logger.info(f"Embedding generated for chunk {chunk_id + 1} of file: {filename}")
                
                # 将分段存储到 Weaviate
                data_object = {
                    "filename": filename,
                    "chunk_id": chunk_id,
                    "content": chunk,
                }
                
                logger.info(f"Storing chunk {chunk_id + 1} in Weaviate: {filename}")
                documents.data.insert(
                    properties=data_object,
                    vector=embedding  # 直接传入向量
                )
                logger.info(f"Chunk {chunk_id + 1} stored in Weaviate: {filename}")
    logger.info("Finished vectorizing and storing .txt files.")