# server.py
import json
import os
import requests
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# -------------------------
# MCP Server
# -------------------------
mcp = FastMCP("github-ci-monitor")

EVENTS_FILE = Path(__file__).parent / "github_events.json"

# -------------------------
# MCP Tools (Module 2)
# -------------------------
@mcp.tool()
def get_recent_actions_events(limit: int = 10):
    """Return the most recent GitHub events."""
    if not EVENTS_FILE.exists():
        return []
    events = json.loads(EVENTS_FILE.read_text())
    return events[-limit:]

@mcp.tool()
def get_workflow_status():
    """Summarize workflow_run statuses."""
    if not EVENTS_FILE.exists():
        return {}
    events = json.loads(EVENTS_FILE.read_text())
    workflows = {}

    for e in events:
        payload = e.get("payload", {})
        if "workflow_run" in payload:
            wf = payload["workflow_run"].get("name")
            status = payload["workflow_run"].get("conclusion")
            workflows[wf] = status

    return workflows

# -------------------------
# ✅ NEW MCP TOOL (Module 3)
# -------------------------
@mcp.tool()
def send_slack_notification(message: str) -> str:
    """
    Send a formatted Slack notification using Incoming Webhooks.
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return "Error: SLACK_WEBHOOK_URL environment variable not set"

    payload = {
        "text": message,
        "mrkdwn": True
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code != 200:
            return f"Slack error {response.status_code}: {response.text}"
        return "Slack notification sent successfully"
    except Exception as e:
        return f"Error sending Slack notification: {str(e)}"

# -------------------------
# MCP Prompts (Module 3)
# -------------------------
@mcp.prompt()
def format_ci_failure_alert():
    """Create a Slack alert for CI/CD failures."""
    return """
Format this GitHub Actions failure as a Slack message:

:rotating_light: *CI Failure Alert* :rotating_light:

A CI workflow has failed:
*Workflow*: workflow_name
*Branch*: branch_name
*Status*: Failed
*View Details*: <LOGS_LINK|View Logs>

Please check the logs and address any issues.

Use Slack markdown formatting and keep it concise.
"""

@mcp.prompt()
def format_ci_success_summary():
    """Create a Slack message celebrating successful deployments."""
    return """
Format this successful GitHub Actions run as a Slack message:

:white_check_mark: *Deployment Successful* :white_check_mark:

Deployment completed successfully for [Repository Name]

*Changes:*
- Key feature or fix 1
- Key feature or fix 2

*Links:*
<PR_LINK|View Changes>

Keep it celebratory but informative.
"""

# -------------------------
# Run MCP Server
# -------------------------
if __name__ == "__main__":
    mcp.run()
