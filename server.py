"""
server.py
---------
Local HTTP Web Server for BLXDES Salon & Spa Causal Analytics Platform.
Serves the web application at http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 65)
        print("BLXDES SALON & SPA - CAUSAL ANALYTICS WEB PLATFORM")
        print("=" * 65)
        print(f"Serving web application at: http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server.")
        print("=" * 65)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

