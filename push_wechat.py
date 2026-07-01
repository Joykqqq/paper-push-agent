"""
微信推送模块
通过 Server酱 API 推送到微信
"""

import requests
from config import SERVERCHAN_SENDKEY


def push_to_wechat(title, content):
    """
    推送消息到微信
    
    Args:
        title: 消息标题
        content: 消息内容（支持Markdown）
    
    Returns:
        bool: 是否推送成功
    """
    if not SERVERCHAN_SENDKEY:
        print("[推送] 错误：未配置 SERVERCHAN_SENDKEY")
        return False
    
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    
    payload = {
        "title": title,
        "desp": content,
    }
    
    print(f"[推送] 正在推送到微信...")
    
    try:
        resp = requests.post(url, json=payload, timeout=15)
        result = resp.json()
        
        if result.get("code") == 0:
            print(f"[推送] 推送成功！pushid: {result.get('data', {}).get('pushid')}")
            return True
        else:
            print(f"[推送] 推送失败: {result}")
            return False
    except Exception as e:
        print(f"[推送] 推送异常: {e}")
        return False
