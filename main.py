"""命令行入口：写作助手。用法:
  python main.py article <主题> [风格]
  python main.py rewrite <文本>
  python main.py expand <文本>
  python main.py summarize <文本>
"""

import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))

from writer import LLMClient, expand, rewrite, summarize_text, write_article  # noqa: E402


def main():
    if len(sys.argv) < 3:
        print("用法：")
        print("  python main.py article <主题> [风格]")
        print("  python main.py rewrite <文本>")
        print("  python main.py expand <文本>")
        print("  python main.py summarize <文本>")
        return
    cmd = sys.argv[1]
    try:
        if cmd == "article":
            topic = sys.argv[2]
            style = sys.argv[3] if len(sys.argv) > 3 else "公众号"
            print(write_article(topic, style, LLMClient()))
        elif cmd == "rewrite":
            print(rewrite(sys.argv[2], llm=LLMClient()))
        elif cmd == "expand":
            print(expand(sys.argv[2], LLMClient()))
        elif cmd == "summarize":
            print(summarize_text(sys.argv[2], LLMClient()))
        else:
            print(f"未知命令：{cmd}")
    except RuntimeError as e:
        print(f"[错误] {e}")


if __name__ == "__main__":
    main()
