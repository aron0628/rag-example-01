"""벡터스토어 관리 유틸리티."""

import os
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from .config import DEFAULT_DB_PATH, DEFAULT_COLLECTION_NAME


def create_vector_store(
    documents: List[Document],
    embedding: Embeddings,
    persist_directory: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Chroma:
    """문서들로부터 새로운 벡터스토어를 생성합니다.
    
    Args:
        documents: 벡터화할 문서 리스트
        embedding: 사용할 임베딩 객체
        persist_directory: 벡터스토어 저장 경로
        collection_name: 컬렉션 이름
        
    Returns:
        생성된 Chroma 벡터스토어
    """
    # 디렉토리가 없으면 생성
    if persist_directory and not os.path.exists(persist_directory):
        os.makedirs(persist_directory, exist_ok=True)
        print(f"디렉토리 생성: {persist_directory}")
    
    return Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )


def load_vector_store(
    embedding: Embeddings,
    persist_directory: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Optional[Chroma]:
    """기존 벡터스토어를 로드합니다.
    
    Args:
        embedding: 사용할 임베딩 객체
        persist_directory: 벡터스토어 저장 경로
        collection_name: 컬렉션 이름
        
    Returns:
        로드된 Chroma 벡터스토어 또는 None (실패시)
    """
    if not os.path.exists(persist_directory):
        return None
        
    try:
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding,
            collection_name=collection_name,
        )
    except Exception as e:
        print(f"벡터스토어 로드 실패: {e}")
        return None


def get_or_create_vector_store(
    documents: Optional[List[Document]] = None,
    embedding: Optional[Embeddings] = None,
    persist_directory: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Chroma:
    """기존 벡터스토어를 로드하거나 새로 생성합니다.
    
    Args:
        documents: 새로 생성할 때 사용할 문서 리스트
        embedding: 사용할 임베딩 객체
        persist_directory: 벡터스토어 저장 경로
        collection_name: 컬렉션 이름
        
    Returns:
        로드되거나 생성된 Chroma 벡터스토어
    """
    if embedding is None:
        raise ValueError("embedding 객체는 필수입니다.")
    
    # 기존 벡터스토어 로드 시도
    db = load_vector_store(embedding, persist_directory, collection_name)
    
    if db is not None:
        print(f"기존 벡터스토어를 로드했습니다: {persist_directory}")
        return db
    
    # 새로 생성
    if documents is None:
        raise ValueError("기존 벡터스토어가 없고 documents도 제공되지 않았습니다.")
    
    print(f"새로운 벡터스토어를 생성합니다: {persist_directory}")
    return create_vector_store(documents, embedding, persist_directory, collection_name)