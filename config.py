"""
配置管理模块
从 .env 文件读取环境变量
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Server酱 配置
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY", "")

# 推送配置
PAPER_COUNT = int(os.getenv("PAPER_COUNT", "3"))
TARGET_HOUR = int(os.getenv("TARGET_HOUR", "14"))

# HuggingFace Papers 页面
HF_PAPERS_URL = "https://huggingface.ac.cn/papers"

# arXiv 摘要页面模板
ARXIV_ABS_URL = "https://arxiv.org/abs/{arxiv_id}"
