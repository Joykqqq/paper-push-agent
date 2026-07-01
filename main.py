"""
主程序入口
串联所有模块，完成每日论文推送任务
"""

import sys
import datetime
from fetch_papers import fetch_top_papers
from parse_arxiv import parse_paper_detail
from summarize import generate_summary
from push_wechat import push_to_wechat
from config import PAPER_COUNT


def build_message(papers_with_summaries):
    """
    组装完整的推送消息
    
    Args:
        papers_with_summaries: list of (paper, summary) 元组
    
    Returns:
        str: 完整的Markdown消息内容
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    lines = [
        f"# 今日AI前沿论文速递",
        f"日期：{today}",
        f"（共 {len(papers_with_summaries)} 篇）",
        "",
        "---",
    ]
    
    for i, (paper, summary) in enumerate(papers_with_summaries, 1):
        lines.append("")
        # 把 "### 论文N：" 替换成正确的编号
        summary_fixed = summary.strip().replace("### 论文N：", f"### 论文{i}：")
        lines.append(summary_fixed)
        lines.append("")
        lines.append("---")
    
    lines.append("")
    lines.append("由AI助手自动整理，每日14:00推送")
    
    return "\n".join(lines)


def main():
    """主函数"""
    print("=" * 50)
    print("AI前沿论文推送 Agent 启动")
    print(f"时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 步骤1：获取热门论文
    papers = fetch_top_papers(count=PAPER_COUNT)
    if not papers:
        print("[主程序] 获取论文失败，退出")
        sys.exit(1)
    
    # 步骤2 & 3：解析详情 + 生成解读
    papers_with_summaries = []
    failed_papers = []
    
    for paper in papers:
        print(f"\n{'='*20}")
        print(f"处理论文: {paper['title']}")
        
        # 解析arXiv详情，同时传入点赞数
        detail = parse_paper_detail(paper["arxiv_id"], upvotes=paper.get("upvotes"))
        if not detail:
            print(f"[主程序] ❌ 解析失败，跳过: {paper['title']}")
            failed_papers.append(paper["title"])
            continue
        
        # 生成中文解读
        summary = generate_summary(detail)
        
        papers_with_summaries.append((paper, summary))
        print(f"[主程序] ✅ 处理完成: {paper['title']}")
    
    # 运行报告
    print(f"\n{'='*50}")
    print(f"运行报告：")
    print(f"  成功：{len(papers_with_summaries)} 篇")
    print(f"  失败：{len(failed_papers)} 篇")
    if failed_papers:
        print(f"  失败列表：{failed_papers}")
    print(f"{'='*50}\n")
    
    if not papers_with_summaries:
        print("[主程序] 没有成功处理的论文，退出")
        sys.exit(1)
    
    if len(papers_with_summaries) < PAPER_COUNT:
        print(f"[主程序] ⚠️ 警告：仅成功处理 {len(papers_with_summaries)}/{PAPER_COUNT} 篇，仍将推送已成功的内容")
    
    # 步骤4：组装推送内容
    message = build_message(papers_with_summaries)
    
    # 步骤5：推送到微信
    title = f"今日AI前沿论文速递"
    success = push_to_wechat(title, message)
    
    if success:
        print("\n[主程序] ✅ 推送成功！")
    else:
        print("\n[主程序] ❌ 推送失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
