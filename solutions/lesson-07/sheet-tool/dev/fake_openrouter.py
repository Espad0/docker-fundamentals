"""A fake OpenRouter for local testing: same URL path and JSON shape, no real model, no cost.

Only the Python standard library, so it runs in the plain python image.
"""
import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DELAY = float(os.getenv("FAKE_DELAY", "0.05"))  # seconds per answer, to imitate a real model


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.reply(200, {"status": "ok"})

    def do_POST(self):
        if self.path != "/api/v1/chat/completions":
            return self.reply(404, {"error": "not found"})
        if not self.headers.get("Authorization", "").startswith("Bearer "):
            return self.reply(401, {"error": "missing API key"})
        request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        prompt = request["messages"][-1]["content"]
        time.sleep(DELAY)
        answer = f"fake answer ({len(prompt.split())} words in)"
        self.reply(200, {"model": request["model"], "choices": [{"message": {"role": "assistant", "content": answer}}]})


ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
