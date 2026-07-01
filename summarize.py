"""
LLM 解读生成模块
调用 DeepSeek API 生成适合理工科本科生（有代码和LLM基础）阅读的深度解读
"""

import openai
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL


def generate_summary(paper_detail):
    """
    为单篇论文生成中文解读
    
    Args:
        paper_detail: parse_arxiv.parse_paper_detail 的返回结果
    
    Returns:
        str: 格式化后的中文解读文本
    """
    arxiv_id = paper_detail["arxiv_id"]
    eng_title = paper_detail.get("eng_title", "")
    authors = paper_detail.get("authors", [])
    abstract = paper_detail.get("abstract", "")
    subjects = paper_detail.get("subjects", "")
    comments = paper_detail.get("comments", "预印本，待同行评审")
    upvotes = paper_detail.get("upvotes", 0)
    
    # 格式化
    author_str = "、".join(authors[:3]) + (" 等" if len(authors) > 3 else "")
    upvotes_str = f"❤️ {upvotes} 赞" if upvotes else "暂无数据"
    
    prompt = f"""你是一位AI研究学者，擅长将前沿学术论文转化为准确、有深度的解读。

目标读者：理工科本科生，有Python编程基础，了解机器学习基本概念（如神经网络、损失函数、Transformer），不需要你从"什么是神经网络"讲起，但也不要假设读者熟悉该论文的具体细分领域。

---

## 论文信息

- 英文标题：{eng_title}
- 作者：{author_str}（共{len(authors)}位作者）
- 研究方向：{subjects}
- 发表信息：{comments}
- arXiv：https://arxiv.org/abs/{arxiv_id}
- 社区热度：{upvotes_str}
- 摘要原文：
{abstract}

---

## 输出格式（严格按此格式，不要加 ``` 包裹）

### 论文N：[根据核心贡献起一个准确、有吸引力的中文标题]

**原文标题：** {eng_title}

**作者：** {author_str}

**arXiv链接：** https://arxiv.org/abs/{arxiv_id}

**期刊/状态：** {comments}

**社区热度：** {upvotes_str}

**一句话概括：** [说明：针对什么任务/问题，提出了什么方法/模型，核心结果如何。控制在2行内。]

**为什么重要：** [这篇论文解决了什么长期存在的痛点或开放问题？对学术界或工业界有什么实际影响？用具体场景说明，不要泛泛而谈"推动了AI发展"。]

**研究方法与原理：** [这是重点，要有深度。说明：1）技术路线是什么；2）核心公式或算法思路（用类比帮助理解，但类比不能替代准确描述）；3）和已有方法的关键区别。假设读者有技术背景，可以适当使用专业术语，但要解释清楚。]

**创新点：** [列出1-3个具体的新贡献，要技术性的，不要写"提高了性能"这种空话。例如："用X替代了Y，消除了Z瓶颈"。]

**关键结果：** [列出1-2个最重要的实验数据，用数字说话。例如："在XXX benchmark上达到XX%，超过前SOTA X个百分点，推理速度提升X倍"。]

---

## 写作要求

- **准确优先**：术语要解释，但不能为了通俗而牺牲准确性
- **有信息密度**：每篇400-500字，不要废话，不要重复摘要原文
- **读者定位**：理工科本科生，有代码和ML基础，不需要解释什么是Transformer/注意力机制，但需要解释本文特有的技术细节
- **社区热度**：直接填写「{upvotes_str}」，不要写「[点赞数]」或留空
- **不要**在输出开头或结尾加任何说明性文字（如"以下是解读..."）

现在请开始输出。
"""
    
    print(f"[LLM解读] 正在为 {arxiv_id} 生成中文解读...")
    
    try:
        client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位资深AI研究学者，精通机器学习、NLP、计算机视觉等前沿方向。你的解读以准确、有深度、信息密度高著称。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        summary = response.choices[0].message.content
        print(f"[LLM解读] 生成完成")
        return summary.strip()
    except Exception as e:
        print(f"[LLM解读] 生成失败: {e}")
        return f"### 论文解读生成失败\n\n摘要原文：\n{abstract}"
