# GitHub Actions Integration

## Setup
1. Install dependencies:
   uv sync

2. Start webhook server:
   python webhook_server.py

3. Expose locally with Cloudflare Tunnel:
   cloudflared tunnel --url http://localhost:8080

4. Add webhook in GitHub repo settings:
   Payload URL = https://<cloudflare-url>/webhook/github

5. Start MCP server:
   uv run server.py
