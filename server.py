# server.py
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP  # ✅ correct import

# Initialize the MCP server
mcp = FastMCP("github-ci-monitor")  # ✅ global variable named 'mcp'

# Path to store GitHub webhook events
EVENTS_FILE = Path(__file__).parent / "github_events.json"

# -------------------------
# MCP Tools
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
            wf = payload["workflow_run"]["name"]
            status = payload["workflow_run"]["conclusion"]
            workflows[wf] = status
    return workflows

# -------------------------
# MCP Prompts
# -------------------------
@mcp.prompt()
def analyze_ci_results():
    return "Analyze the latest CI/CD events and summarize failures with actionable insights."

@mcp.prompt()
def create_deployment_summary():
    return "Create a team-friendly deployment summary based on recent CI/CD results."

@mcp.prompt()
def generate_pr_status_report():
    return "Generate a combined report of PR changes and CI/CD status."

@mcp.prompt()
def troubleshoot_workflow_failure():
    return "Systematically debug the most recent workflow failure."

# -------------------------
# Run the MCP server
# -------------------------
if __name__ == "__main__":
    mcp.run()
