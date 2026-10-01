"""写作助手单元测试。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from writer import LLMClient, expand, rewrite, summarize_text, write_article  # noqa: E402


class FakeLLM(LLMClient):
    def chat(self, messages, temperature=0.8):
        return "[生成] " + messages[-1]["content"][:30]


class TestWriter(unittest.TestCase):
    def test_write_article(self):
        r = write_article("人工智能", llm=FakeLLM())
        self.assertIn("[生成]", r)

    def test_rewrite(self):
        r = rewrite("这句话写得一般", llm=FakeLLM())
        self.assertIn("[生成]", r)

    def test_expand(self):
        r = expand("简短内容", FakeLLM())
        self.assertIn("[生成]", r)

    def test_summarize(self):
        r = summarize_text("很长的一段内容", FakeLLM())
        self.assertIn("[生成]", r)


if __name__ == "__main__":
    unittest.main(verbosity=2)
