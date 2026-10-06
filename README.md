# genpark-enterprise-meeting-action-item-extractor-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Skill-blue.svg)](https://genpark.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Enterprise Multi-Speaker Meeting Action Item Extractor & WeChat Work Task Dispatcher. Analyzes conversational meeting transcripts from Tencent Meeting, Zoom, and Teams, extracts explicit commitments, dates, and assignees, performs Eisenhower urgency-importance matrix prioritization, and formats collaborative task cards.

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
"""Example usage for EnterpriseMeetingActionItemExtractor."""
import sys
import json
from client import EnterpriseMeetingActionItemExtractor

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Enterprise WorkBuddy Meeting Action Item Extractor Demo ===")
    extractor = EnterpriseMeetingActionItemExtractor()

    transcript = [
        "David: Good morning everyone, let's review the Q4 cloud infrastructure roadmap.",
        "ZhangSan: I will prepare the Tencent Cloud compute reservation forecast by Friday.",
        "LiSi: Please ensure the Merkle audit verification connector is deployed today, this is an urgent blocker for finance.",
        "WangWu: I'll coordinate the WeChat Work notification bot endpoints before tomorrow EOD."
    ]

    print("\n--- 1. Extracting Structured Tasks from Utterances ---")
    items = extractor.extract_action_items(transcript, "Tencent Cloud Infrastructure Sync")
    print(f"Discovered {len(items)} action items:")
    for item in items:
        print(f"[{item['item_id']}] ({item['eisenhower_matrix']}) @{item['assignee']} -> {item['task_description']} (Due: {item['deadline']})")

    print("\n--- 2. Generating WeChat Work Collaborative Card ---")
    card = extractor.generate_task_card(items, "Tencent Cloud Infrastructure Sync")
    print(card["card_markdown"])

if __name__ == "__main__":
    main()

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License

Licensed under the [MIT License](LICENSE). Copyright © 2026 GenPark AI.
