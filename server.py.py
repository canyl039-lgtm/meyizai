from http.server import HTTPServer, SimpleHTTPRequestHandler
import requests
import json

API_KEY = "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"
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
            }

            payload = {
                "model": "google/gemma-4-31b-it",
                "messages": body.get("messages", []),
                "max_tokens": 16384,
                "temperature": 1.00,
                "top_p": 0.95,
                "stream": True,
                "chat_template_kwargs": {"enable_thinking": True}
            }

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self._cors()
            self.end_headers()

            with requests.post(NVIDIA_URL, headers=headers, json=payload, stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        self.wfile.write(line + b"\n\n")
                        self.wfile.flush()
        else:
            super().do_POST()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/meyizaiapi.html"
        super().do_GET()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        print(f"[meyizAi] {args[0]} {args[1]}")

if __name__ == "__main__":
    port = 8080
    print(f"✅ meyizAi server başlatıldı → http://localhost:{port}")
    print("   Durdurmak için Ctrl+C")
    HTTPServer(("", port), ProxyHandler).serve_forever()
