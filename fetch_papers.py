"""
论文获取模块
从 HuggingFace Papers 页面获取每日热门论文
"""

import requests
from bs4 import BeautifulSoup
from config import HF_PAPERS_URL, PAPER_COUNT


def fetch_top_papers(count=PAPER_COUNT):
    """
    获取 HuggingFace Daily Papers 热门论文
    
    Returns:
        list[dict]: 每篇论文的字典，包含 title, arxiv_id, upvotes
    """
    print(f"[论文获取] 正在访问 {HF_PAPERS_URL}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        resp = requests.get(HF_PAPERS_URL, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"[论文获取] 访问失败: {e}")
        return []
    
    soup = BeautifulSoup(resp.text, "lxml")
    
    papers = []
    # 每篇论文是一个 <a class="paper ..."> 标签
    paper_links = soup.select("a.paper")
    
    for tag in paper_links[:count]:
        # 提取 arXiv ID
        href = tag.get("href", "")
        arxiv_id = href.split("/")[-1] if href else ""
        
        # 提取标题（中文翻译）—— 在 div.text-primary 里
        title_tag = tag.select_one("div.text-primary")
        title = title_tag.text.strip() if title_tag else "未知标题"
        
        # 提取点赞数
        # HTML结构：
        # <div class="d-flex flex-column ...">
        #   <div style="line-height: 1;">❤️</div>
        #   <div style="line-height: 1.2;">81</div>
        # </div>
        upvotes = 0
        flex_col = tag.select_one("div.flex-column")
        if flex_col:
            # 取 flex-column 容器内的第二个 div（第一个是 ❤️，第二个是数字）
            num_divs = flex_col.select("div")
            if len(num_divs) >= 2:
                try:
                    upvotes = int(num_divs[1].text.strip())
                except (ValueError, IndexError):
                    pass
        
        if arxiv_id:
            papers.append({
                "title": title,
                "arxiv_id": arxiv_id,
                "upvotes": upvotes,
            })
            print(f"[论文获取] 已获取: {title} (upvotes={upvotes})")
    
    print(f"[论文获取] 共获取 {len(papers)} 篇论文")
    return papers
