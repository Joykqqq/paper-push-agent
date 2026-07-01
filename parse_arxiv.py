"""
arXiv 论文详情解析模块
从 arXiv 页面解析作者、摘要、分类等信息
"""

import requests
from bs4 import BeautifulSoup
from config import ARXIV_ABS_URL


def parse_paper_detail(arxiv_id, upvotes=None, retries=3, timeout=20):
    """
    解析单篇论文的详细信息
    
    Args:
        arxiv_id: arXiv ID，如 "2606.30534"
        upvotes: 社区点赞数（可选，从 HF Papers 获取）
        retries: 失败重试次数
        timeout: 请求超时时间（秒）
    
    Returns:
        dict: 包含 authors, abstract, subjects, comments, upvotes 的字典
    """
    url = ARXIV_ABS_URL.format(arxiv_id=arxiv_id)
    print(f"[arXiv解析] 正在解析 {arxiv_id}")
    
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            break
        except Exception as e:
            print(f"[arXiv解析] 第{attempt}次尝试失败: {e}")
            if attempt < retries:
                import time
                time.sleep(2 * attempt)  # 指数退避：2s, 4s
            else:
                print(f"[arXiv解析] 全部{retries}次尝试均失败，放弃")
                return None
    
    soup = BeautifulSoup(resp.text, "lxml")
    
    # 提取作者
    author_tags = soup.select('meta[name="citation_author"]')
    authors = [tag.get("content", "") for tag in author_tags]
    
    # 提取英文标题
    title_tag = soup.select_one('h1.title.mathjax')
    eng_title = title_tag.get_text(strip=True) if title_tag else ""
    if eng_title.startswith("Title:"):
        eng_title = eng_title[len("Title:"):].strip()
    
    # 提取摘要
    abstract_tag = soup.select_one('blockquote.abstract.mathjax')
    abstract = ""
    if abstract_tag:
        abstract = abstract_tag.get_text(strip=True)
        if abstract.startswith("Abstract:"):
            abstract = abstract[len("Abstract:"):].strip()
    
    # 提取研究方向
    subject_tag = soup.select_one('span.primary-subject')
    subjects = subject_tag.text.strip() if subject_tag else ""
    
    # 提取发表信息/Comments
    comments_tag = soup.select_one('td.tablecell.comments.mathjax')
    comments = comments_tag.get_text(strip=True) if comments_tag else "预印本，待同行评审"
    
    result = {
        "arxiv_id": arxiv_id,
        "eng_title": eng_title,
        "authors": authors,
        "abstract": abstract,
        "subjects": subjects,
        "comments": comments,
        "upvotes": upvotes,
    }
    
    print(f"[arXiv解析] 解析完成，作者: {authors[0] if authors else '未知'} 等")
    return result
