"""
목차 필터링 유틸리티 모듈

PDF 문서에서 목차 패턴을 식별하고 제거하는 범용 필터링 기능을 제공합니다.
다양한 문서 형식(한글, 영문, 일문)과 목차 스타일을 지원합니다.
"""

import re
from typing import List
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.schema import Document


def load_pdf_with_toc_filter(file_path: str) -> List[Document]:
    """
    PDF 파일을 로드하고 목차를 필터링합니다.
    
    Args:
        file_path (str): PDF 파일 경로
        
    Returns:
        List[Document]: 목차가 필터링된 문서 리스트
    """
    # PDF 로드
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()
    print(f"✅파싱된 문서의 수: {len(docs)}")
    
    # 목차 필터링 적용
    original_content_length = sum(len(doc.page_content) for doc in docs)
    filtered_docs = filter_toc_content(docs)
    filtered_content_length = sum(len(doc.page_content) for doc in filtered_docs)
    
    print(f"✅목차 필터링 후 문서의 수: {len(filtered_docs)}")
    print(f"✅내용 감소량: {original_content_length - filtered_content_length} 문자")
    
    return filtered_docs


def filter_toc_content(docs: List[Document]) -> List[Document]:
    """
    목차 패턴을 포함한 라인들을 제거하는 범용 함수
    
    Args:
        docs (List[Document]): 원본 문서 리스트
        
    Returns:
        List[Document]: 목차가 필터링된 문서 리스트
    """
    filtered_docs = []
    
    for doc in docs:
        # 원본 문서 복사
        filtered_doc = doc.copy()
        
        # 내용을 라인별로 분리
        lines = doc.page_content.split('\n')
        clean_lines = []
        
        for line in lines:
            if not is_toc_line(line):  # 목차 라인이 아니면 유지
                clean_lines.append(line)
        
        # 정제된 내용으로 업데이트
        clean_content = '\n'.join(clean_lines).strip()
        if clean_content:  # 내용이 남아있으면 추가
            filtered_doc.page_content = clean_content
            filtered_docs.append(filtered_doc)
    
    return filtered_docs


def is_toc_line(line: str) -> bool:
    """
    목차 라인인지 판별하는 범용 함수
    
    Args:
        line (str): 검사할 텍스트 라인
        
    Returns:
        bool: 목차 라인이면 True, 아니면 False
    """
    line_clean = line.strip()
    
    # 빈 라인은 유지
    if not line_clean:
        return False
    
    # 매우 짧은 라인 (페이지 번호만 있는 경우)
    if len(line_clean) <= 3 and line_clean.isdigit():
        return True
    
    # 범용 목차 패턴들 (모든 문서 유형에 적용)
    toc_patterns = [
        # 점선 패턴 (다양한 점 문자)
        r'.*[\.·…‥]{3,}.*\d+\s*$',                    # "항목명........1", "항목명···1"
        r'^[▹▸►▪•]\s*.*[\.·…‥]{3,}.*\d+',           # "▹ 항목명.....1"
        
        # 숫자-숫자 페이지 형식
        r'.*[\.·…‥]{3,}.*\d+-\d+\s*$',               # "항목명.....1-1"
        r'^\d+-\d+\s*$',                              # "1-1" (단독)
        
        # 장/절 표시
        r'^\d+장\s*$',                                # "1장"
        r'^\d+\.\d+\s*$',                             # "1.1"
        r'^제\d+장',                                   # "제1장"
        
        # 로마숫자 패턴
        r'^[IVX]+\s*\.',                              # "I.", "II.", "III."
        r'^[ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ]+\s*\.',               # "ⅰ.", "ⅱ."
        
        # 목차 키워드
        r'^\s*(목차|차례|contents?|table\s+of\s+contents)\s*$',  # "목차", "Contents"
        
        # 페이지 참조 패턴
        r'.*\s+\d+\s*$',                              # 끝에 숫자만 있는 경우 (페이지 번호)
        
        # 특수 기호 시작 + 페이지 번호
        r'^[▹▸►▪•]\s*.*\s+\d+\s*$',                  # "▹ 제목 1"
    ]
    
    # 패턴 매칭
    for pattern in toc_patterns:
        if re.search(pattern, line_clean, re.IGNORECASE):
            # 너무 긴 라인은 제외 (실제 내용일 가능성)
            if len(line_clean) > 200:
                continue
            # 특정 키워드가 있으면 실제 내용으로 간주
            if any(keyword in line_clean.lower() for keyword in ['는', '이', '가', '을', '를', 'the', 'and', 'or']):
                if not any(dot in line for dot in ['...', '···', '…']):
                    continue
            return True
    
    return False


def analyze_toc_patterns(file_path: str, max_pages: int = 5) -> None:
    """
    PDF 파일의 목차 패턴을 분석하고 출력합니다. (디버깅용)
    
    Args:
        file_path (str): PDF 파일 경로
        max_pages (int): 분석할 최대 페이지 수
    """
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()
    
    print(f"=== {file_path} 목차 패턴 분석 ===")
    print(f"총 페이지 수: {len(docs)}")
    
    for i, doc in enumerate(docs[:max_pages]):
        print(f"\n--- Page {i} ---")
        lines = doc.page_content.split('\n')
        
        for j, line in enumerate(lines[:20]):  # 각 페이지의 처음 20줄만
            if line.strip():
                is_toc = is_toc_line(line)
                status = "🗑️" if is_toc else "✅"
                print(f"{status} {j:2d}: {repr(line[:80])}")