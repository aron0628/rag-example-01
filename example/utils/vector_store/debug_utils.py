"""벡터스토어 디버깅 유틸리티."""

from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def debug_embedding_process(documents: List[Document], embedding: Embeddings) -> None:
    """임베딩 프로세스를 디버그합니다.
    
    Args:
        documents: 임베딩할 문서 리스트
        embedding: 사용할 임베딩 객체
    """
    print("=== 임베딩 디버그 정보 ===")
    print(f"📊 총 문서 수: {len(documents)}")
    
    # 임베딩 모델 정보 출력
    if hasattr(embedding, 'passage_model_name'):
        print(f"📄 문서 임베딩 모델: {embedding.passage_model_name}")
    if hasattr(embedding, 'query_model_name'):
        print(f"🔍 쿼리 임베딩 모델: {embedding.query_model_name}")
    
    # 첫 번째 문서로 테스트
    if documents:
        print(f"🧪 첫 번째 문서로 임베딩 테스트 중...")
        test_text = documents[0].page_content[:100] + "..."
        print(f"테스트 텍스트: {test_text}")
        
        # 직접 임베딩 호출하여 로그 확인
        embedding.embed_documents([documents[0].page_content])
        print("✅ 문서 임베딩 테스트 완료")
    
    print("========================\n")


def debug_retrieval_process(vector_store, query: str, k: int = 5) -> None:
    """검색 프로세스를 디버그합니다.
    
    Args:
        vector_store: 벡터스토어
        query: 검색 쿼리
        k: 검색할 문서 수
    """
    print("=== 검색 디버그 정보 ===")
    print(f"🔍 검색 쿼리: {query}")
    print(f"📊 검색할 문서 수: {k}")
    
    # 유사도 점수와 함께 검색
    results = vector_store.similarity_search_with_score(query, k=k)
    
    print(f"✅ 검색된 문서 수: {len(results)}")
    
    for i, (doc, score) in enumerate(results):
        print(f"\n[문서 {i+1}] 유사도: {score:.4f}")
        print(f"내용: {doc.page_content[:200]}...")
        if doc.metadata:
            print(f"메타데이터: {doc.metadata}")
    
    print("========================\n")