"""
论文获取模块
优先从 arXiv API 获取，完全不依赖 HuggingFace
"""
import urllib.request
import xml.etree.ElementTree as ET
from config import PAPER_COUNT


def fetch_top_papers(count=PAPER_COUNT):
    print(f"[论文获取] 正在从 arXiv API 获取最新 {count} 篇 AI 论文")

    query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.CV"
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=5"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "paper-push-agent/1.0"})
        resp = urllib.request.urlopen(req, timeout=30)
        data = resp.read().decode("utf-8")
    except Exception as e:
        print(f"[论文获取] arXiv API 访问失败: {e}")
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(data)
    entries = root.findall("atom:entry", ns)

    papers = []
    for entry in entries[:count]:
        title_el = entry.find("atom:title", ns)
        title = title_el.text.strip().replace("\n", " ") if title_el is not None else ""

        id_el = entry.find("atom:id", ns)
        arxiv_id = id_el.text.strip().split("/abs/")[-1] if id_el is not None else ""

        summary_el = entry.find("atom:summary", ns)
        abstract = summary_el.text.strip().replace("\n", " ") if summary_el is not None else ""

        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns) if a.find("atom:name", ns) is not None]

        cats = [c.get("term") for c in entry.findall("atom:category", ns) if c.get("term")]

        if arxiv_id:
            papers.append({
                "title": title,
                "arxiv_id": arxiv_id,
                "authors": authors,
                "abstract": abstract,
                "categories": cats,
                "upvotes": 0,
            })
            print(f"[论文获取] 已获取: {title[:60]}...")

    print(f"[论文获取] 共获取 {len(papers)} 篇论文")
    return papers
