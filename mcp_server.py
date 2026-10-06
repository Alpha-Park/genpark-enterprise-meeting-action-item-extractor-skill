"""MCP Server for Enterprise Meeting Action Item Extractor."""
import sys
import json
import time
from client import EnterpriseMeetingActionItemExtractor

extractor = EnterpriseMeetingActionItemExtractor()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "extract_meeting_action_items":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "extract_action_items")
    transcript = args.get("transcript_lines", [])
    title = args.get("meeting_title", "General Project Sync")

    if action == "extract_action_items":
        items = extractor.extract_action_items(transcript, meeting_title=title)
        return {"total_items": len(items), "action_items": items}
    elif action == "generate_task_card":
        items = extractor.extract_action_items(transcript, meeting_title=title)
        return extractor.generate_task_card(items, meeting_title=title)
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        sample_transcript = [
            "Bob: I will prepare the financial audit slide deck by Friday.",
            "Alice: Please ensure the security boundary review is completed today, it is an urgent blocker.",
            "Charlie: Let's make sure to order pizza for tomorrow's hackathon."
        ]
        items = extractor.extract_action_items(sample_transcript, "Q3 Security & Finance Sync")
        assert len(items) >= 2
        p0_items = [i for i in items if "P0" in i["eisenhower_matrix"]]
        assert len(p0_items) >= 1
        card = extractor.generate_task_card(items, "Q3 Security & Finance Sync")
        assert "会议任务清单" in card["card_markdown"]
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "EnterpriseMeetingActionItemExtractor", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "extract_meeting_action_items",
                            "description": "Extract action items, assignees, deadlines, and Eisenhower priority matrix from multi-speaker meeting transcripts, generating WeChat Work notification cards.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["extract_action_items", "generate_task_card"]},
                                    "transcript_lines": {"type": "array"},
                                    "meeting_title": {"type": "string"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
