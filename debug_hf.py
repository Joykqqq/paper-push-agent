import urllib.request, re

req = urllib.request.Request(
    "https://huggingface.ac.cn/papers",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode("utf-8", errors="replace")

with open("C:/Users/joy/paper_push_agent/hf_debug.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"页面大小: {len(html)} 字符")
print(f"已保存到 hf_debug.html")

# 找所有 <article> 标签内容（前800字符）
articles = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
print(f"\n<article> 标签数: {len(articles)}")
if articles:
    snippet = articles[0][:800]
    with open("C:/Users/joy/paper_push_agent/article_snippet.txt", "w", encoding="utf-8") as f:
        f.write(snippet)
    print(f"第一个 article 片段已保存到 article_snippet.txt")
    print(snippet)

# 找点赞数 - 尝试多种模式
for pattern in [r'❤️', r'👍', r'upvote', r'vote.count', r'likes', r'data-reaction.+?count']:
    matches = [m.start() for m in re.finditer(pattern, html, re.IGNORECASE)]
    if matches:
        print(f"\n找到 '{pattern}': {len(matches)} 处, 前3处上下文:")
        for pos in matches[:3]:
            start = max(0, pos - 80)
            end = min(len(html), pos + 150)
            print(f"  '{html[start:end]}'")
