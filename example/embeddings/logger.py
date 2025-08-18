"""디버그 로깅 유틸리티."""

from .config import DEBUG_PREFIX


def log_embed_documents(model_name: str) -> None:
    """문서 임베딩 호출 시 디버그 로그 출력.
    
    Args:
        model_name: 사용된 모델명
    """
    print(f"{DEBUG_PREFIX} embed_documents() 호출 → 모델: {model_name}")


def log_embed_query(model_name: str) -> None:
    """쿼리 임베딩 호출 시 디버그 로그 출력.
    
    Args:
        model_name: 사용된 모델명
    """
    print(f"{DEBUG_PREFIX} embed_query() 호출 → 모델: {model_name}")