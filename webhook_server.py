from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from datetime import datetime

EVENTS_FILE = Path(__file__).parent / "github_events.json"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {"raw": body.decode("utf-8")}

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": self.headers.get("X-GitHub-Event"),
            "payload": payload
        }

        # Append to file
        if EVENTS_FILE.exists():
            events = json.loads(EVENTS_FILE.read_text())
        else:
            events = []
        events.append(event)
        EVENTS_FILE.write_text(json.dumps(events, indent=2))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Event received")

def run(server_class=HTTPServer, handler_class=WebhookHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print("Webhook server running on port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
