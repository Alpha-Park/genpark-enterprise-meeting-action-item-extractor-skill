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
