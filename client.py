"""
Enterprise Meeting Action Item Extractor (Zero External Dependencies)
Parses conversational utterances, identifies commitment verbs, deduces assignees, and grades Eisenhower priority.
"""
import time
import math
import hashlib
import json
import re
from typing import Dict, Any, List, Optional

COMMITMENT_PATTERNS = [
    r"(?:i will|i'll|i can|i am going to|i'm going to)\s+([\w\s]{5,60})",
    r"(?:will take ownership of|take care of|follow up on)\s+([\w\s]{5,60})",
    r"(?:please ensure|let's make sure)\s+([\w\s]{5,60})",
    r"(?:action item for\s+(\w+):)\s*([\w\s]{5,60})"
]

DEADLINE_PATTERNS = [
    r"by\s+(friday|monday|tuesday|wednesday|thursday|tomorrow|eod|end of week|next week|[0-9]{1,2}/[0-9]{1,2})",
    r"before\s+(the weekend|tomorrow|launch|eod|eop)",
    r"due\s+(friday|monday|tomorrow|next week)"
]

class EnterpriseMeetingActionItemExtractor:
    def __init__(self):
        self.compiled_commitments = [re.compile(p, re.IGNORECASE) for p in COMMITMENT_PATTERNS]
        self.compiled_deadlines = [re.compile(p, re.IGNORECASE) for p in DEADLINE_PATTERNS]

    def extract_action_items(
        self,
        transcript_lines: List[str],
        meeting_title: str = "Weekly Team Sync",
        default_assignee: str = "Unassigned"
    ) -> List[Dict[str, Any]]:
        """Extracts structured tasks, assignees, deadlines, and urgency levels."""
        action_items = []

        for idx, line in enumerate(transcript_lines):
            line_str = line.strip()
            if not line_str:
                continue

            # Parse speaker if format is 'Speaker: text'
            speaker = default_assignee
            text = line_str
            if ":" in line_str:
                parts = line_str.split(":", 1)
                speaker = parts[0].strip()
                text = parts[1].strip()

            # Check commitment matches
            found_task = None
            for pat in self.compiled_commitments:
                m = pat.search(text)
                if m:
                    found_task = m.group(1).strip()
                    break

            if not found_task and any(k in text.lower() for k in ["need to", "action item", "todo", "make sure to"]):
                found_task = text

            if found_task:
                # Find deadline
                deadline = "Next Sprint"
                for dpat in self.compiled_deadlines:
                    dm = dpat.search(text)
                    if dm:
                        deadline = dm.group(1).strip().upper()
                        break

                # Determine Eisenhower priority
                is_urgent = any(u in text.lower() for u in ["asap", "today", "eod", "tomorrow", "urgent", "blocker"])
                is_important = any(imp in text.lower() for imp in ["p0", "launch", "security", "customer", "contract", "financial", "board"])

                if is_urgent and is_important:
                    matrix = "P0_URGENT_IMPORTANT"
                elif is_important and not is_urgent:
                    matrix = "P1_IMPORTANT_STRATEGIC"
                elif is_urgent and not is_important:
                    matrix = "P2_URGENT_DELEGATE"
                else:
                    matrix = "P3_STANDARD_BACKLOG"

                item_id = f"ACT-{hashlib.md5((speaker + found_task + str(idx)).encode('utf-8')).hexdigest()[:6].upper()}"

                action_items.append({
                    "item_id": item_id,
                    "task_description": found_task[:100],
                    "assignee": speaker,
                    "deadline": deadline,
                    "eisenhower_matrix": matrix,
                    "source_utterance": text[:120]
                })

        return action_items

    def generate_task_card(self, action_items: List[Dict[str, Any]], meeting_title: str) -> Dict[str, Any]:
        """Generates Tencent Docs / WeChat Work collaborative task markdown card."""
        lines = [
            f"📋 **【会议任务清单】{meeting_title}**",
            f"提取时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
            f"待办事项总数: {len(action_items)} 项",
            "---"
        ]

        for item in action_items:
            priority_emoji = "🔴" if "P0" in item["eisenhower_matrix"] else ("🟡" if "P1" in item["eisenhower_matrix"] else "🟢")
            lines.append(f"{priority_emoji} **[{item['item_id']}] {item['task_description']}**")
            lines.append(f"  - 责任人: `@{item['assignee']}` | 截止期限: `{item['deadline']}` | 级别: `{item['eisenhower_matrix']}`")

        card_markdown = "\n".join(lines)
        return {
            "meeting_title": meeting_title,
            "total_items": len(action_items),
            "card_markdown": card_markdown,
            "action_items": action_items
        }
