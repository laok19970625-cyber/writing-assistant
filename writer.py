"""AI 写作助手：按主题/关键词生成文章、文案、改写、扩写、缩写。

纯标准库实现，可配置 LLM。
"""

from __future__ import annotations

import json
import os
import urllib.request


class LLMClient:
    def __init__(self, api_key=None, api_base=None, model=None):
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.api_base = (api_base or os.environ.get("LLM_API_BASE", "https://open.bigmodel.cn/api/paas/v4")).rstrip("/")
        self.model = model or os.environ.get("LLM_MODEL", "glm-4-flash")

    def chat(self, messages, temperature=0.8):
        if not self.api_key:
            raise RuntimeError("未配置 LLM_API_KEY，请设置环境变量后重试。")
        url = f"{self.api_base}/chat/completions"
        payload = {"model": self.model, "messages": messages, "temperature": temperature}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]


def write_article(topic: str, style: str = "公众号", llm: LLMClient | None = None) -> str:
    """按主题生成文章。style: 公众号/新闻稿/产品介绍/小红书等。"""
    llm = llm or LLMClient()
    prompt = (
        f"请以「{style}」的风格，围绕主题「{topic}」写一篇文章。"
        "要求结构清晰、有标题和小标题、内容充实、语言自然，600-1000 字。"
    )
    return llm.chat([{"role": "user", "content": prompt}])


def rewrite(text: str, tone: str = "更专业", llm: LLMClient | None = None) -> str:
    """改写文本，调整语气。tone: 更专业/更口语/更简洁/更有感染力。"""
    llm = llm or LLMClient()
    prompt = f"请把下面的文本改写得更{tone}，保持原意不变：\n\n{text}"
    return llm.chat([{"role": "user", "content": prompt}])


def expand(text: str, llm: LLMClient | None = None) -> str:
    """扩写。"""
    llm = llm or LLMClient()
    prompt = f"请把下面的内容扩写成更详细、更充实的版本，补充细节和过渡：\n\n{text}"
    return llm.chat([{"role": "user", "content": prompt}])


def summarize_text(text: str, llm: LLMClient | None = None) -> str:
    """摘要。"""
    llm = llm or LLMClient()
    prompt = f"请用简洁的语言概括下面的内容，突出核心要点：\n\n{text}"
    return llm.chat([{"role": "user", "content": prompt}])
