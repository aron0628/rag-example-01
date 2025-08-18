"""디버그용 Upstage 비대칭 임베딩 클래스."""

from typing import List
from langchain_core.embeddings import Embeddings
from langchain_upstage import UpstageEmbeddings

from .config import DEFAULT_PASSAGE_MODEL, DEFAULT_QUERY_MODEL
from .logger import log_embed_documents, log_embed_query


class DebugUpstageAsymmetricEmbeddings(Embeddings):
    """디버그 로그가 포함된 Upstage 비대칭 임베딩 클래스.

    문서(passage)와 쿼리(query)에 대해 서로 다른 임베딩 모델을 사용하며,
    각 호출 시 디버그 로그를 출력합니다.
    """

    def __init__(
        self,
        passage_model: str = DEFAULT_PASSAGE_MODEL,
        query_model: str = DEFAULT_QUERY_MODEL,
        **kwargs,
    ):
        """디버그용 비대칭 임베딩 초기화.

        Args:
            passage_model: 문서 임베딩용 모델명
            query_model: 쿼리 임베딩용 모델명
            **kwargs: UpstageEmbeddings에 전달할 추가 인자
        """
        self.doc_embedder = UpstageEmbeddings(model=passage_model, **kwargs)
        self.query_embedder = UpstageEmbeddings(model=query_model, **kwargs)
        self.passage_model_name = passage_model
        self.query_model_name = query_model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """문서 텍스트들을 임베딩으로 변환.

        Args:
            texts: 임베딩할 텍스트 리스트

        Returns:
            임베딩 벡터들의 리스트
        """
        log_embed_documents(self.passage_model_name)
        return self.doc_embedder.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        """쿼리 텍스트를 임베딩으로 변환.

        Args:
            text: 임베딩할 쿼리 텍스트

        Returns:
            임베딩 벡터
        """
        log_embed_query(self.query_model_name)
        return self.query_embedder.embed_query(text)