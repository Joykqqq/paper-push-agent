"""
论文获取模块
从 arXiv API 获取最新 AI 论文（GitHub Actions 友好，无访问限制）
"""

import requests
from bs4 import BeautifulSoup
from config import PAPER_COUNT


def fetch_top_papers(count=PAPER_COUNT):
    """
    从 arXiv API 获取最新 AI 论文
    
    Returns:
        list[dict]: 每篇论文的字典，包含 title, arxiv_id, upvotes
    """
    print(f"[论文获取] 正在从 arXiv API 获取最新 {count} 篇 AI 论文")
    
    # 查询 AI 相关领域的最新论文
    # cs.AI: 人工智能
    # cs.LG: 机器学习  
    # cs.CL: 计算语言学（LLM相关）
    # cs.CV: 计算机视觉
    query = "cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cs.CV"
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={count}"
    
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"[论文获取] arXiv API 访问失败: {e}")
        return []
    
    soup = BeautifulSoup(resp.text, "xml")
    entries = soup.select("entry")
    
    papers = []
    for entry in entries[:count]:
        # 提取标题
        title_tag = entry.select_one("title")
        title = title_tag.text.strip().replace("\n", " ") if title_tag else "未知标题"
        
        # 提取 arXiv ID
        id_tag = entry.select_one("id")
        arxiv_id = id_tag.text.strip().split("/abs/")[-1] if id_tag else ""
        
        # 提取作者
        authors = []
        for author in entry.select("author")[:3]:
            name_tag = author.select_one("name")
            if name_tag:
                authors.append(name_tag.text.strip())
        
        # 提取摘要
        summary_tag = entry.select_one("summary")
        abstract = summary_tag.text.strip().replace("\n", " ") if summary_tag else ""
        
        if arxiv_id:
            papers.append({
                "title": title,
                "arxiv_id": arxiv_id,
                "authors": authors,
                "abstract": abstract,
                "upvotes": 0,  # arXiv 没有点赞数
            })
            print(f"[论文获取] 已获取: {title[:60]}...")
    
    print(f"[论文获取] 共获取 {len(papers)} 篇论文")
    return papers
