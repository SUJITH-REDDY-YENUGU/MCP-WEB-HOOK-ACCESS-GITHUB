
# GitHub CI Monitor (MCP + Webhooks)

This project integrates **GitHub Actions**, **Cloudflare Tunnels**, and **Claude (via MCP)** to monitor CI/CD events, analyze workflow failures, and generate human-friendly reports.

GitHub events are received through a webhook, stored locally, and later analyzed by Claude using MCP tools and prompts.

---

## Architecture Overview

```

GitHub Repository
│
│  Webhook Events
▼
Cloudflare Tunnel (public HTTPS URL)
│
▼
Local Webhook Server (webhook.py :8080)
│
▼
github_events.json (stored events)
│
▼
Claude Desktop (MCP Server: server.py)

```

---

## Folder Structure

```

github-actions-integration/
│
├── server.py          # MCP server (tools + prompts for Claude)
├── webhook.py         # Local HTTP webhook listener (port 8080)
├── github_events.json # Stored GitHub webhook events (auto-created)
├── README.md

````

---

## Components

### 1. `webhook.py`
- Runs a local HTTP server on port `8080`
- Receives GitHub webhook events
- Stores events in `github_events.json`

### 2. `server.py`
- Defines an MCP server using `FastMCP`
- Exposes tools for:
  - Reading recent GitHub events
  - Summarizing workflow statuses
- Exposes prompts for:
  - CI failure analysis
  - Deployment summaries
  - PR status reports
- Automatically launched by **Claude Desktop**

---

## Setup Instructions

### Step 1: Install Requirements

- Python 3.10+
- Cloudflare Tunnel (`cloudflared`)
- Claude Desktop (with MCP enabled)

---

### Step 2: Run the Webhook Server

```bash
cd github-actions-integration
python webhook.py
````

Expected output:

```
Webhook server running on port 8080...
```

Keep this terminal running.

---

### Step 3: Expose Webhook Using Cloudflare

Open a new terminal and run:

```bash
cloudflared tunnel --url http://localhost:8080
```

You will get a public URL like:

```
https://wild-sheep-1234.trycloudflare.com
```

Copy this URL.

---

### Step 4: Configure GitHub Webhook

In your GitHub repository:

1. Go to **Settings → Webhooks → Add webhook**
2. Set **Payload URL** to:

   ```
   https://<your-cloudflare-url>
   ```
3. Set **Content type**:

   ```
   application/json
   ```
4. Select events:

   * Workflow runs
   * Pull requests
     *(or “Send me everything”)*

Save the webhook and use **Test delivery**.

---

### Step 5: Verify Event Storage

After a workflow runs, check:

```text
github_events.json
```

You should see stored webhook events.

---

## Claude MCP Configuration

Add the MCP server to your Claude Desktop `config.json`:

```json
{
  "mcpServers": {
    "github-ci-monitor": {
      "command": "D:\\Python311\\Scripts\\uv.exe",
      "args": [
        "run",
        "python",
        "D:\\vscode_folders\\python_programs\\BASIC_LANGCHAIN\\github-actions-integration\\server.py"
      ]
    }
  }
}
```

Restart **Claude Desktop** after saving.

---

## Example Prompts in Claude

You can now ask Claude:

* “Analyze the latest CI/CD failures”
* “Summarize recent GitHub Actions workflow results”
* “Generate a PR and CI status report”
* “Troubleshoot the most recent workflow failure”

Claude will read `github_events.json` and respond using MCP tools.

---

## Notes

* `server.py` **should not be run manually**
* `webhook.py` **must be running** to receive GitHub events
* Cloudflare tunnel must stay active for GitHub deliveries
* Events persist locally in `github_events.json`

---

## Future Enhancements

* Slack notifications for workflow failures
* Auto-generated PR comments
* CI trend analytics
* Multi-repo support

---

## License

MIT

```

Just tell me 🚀
```
