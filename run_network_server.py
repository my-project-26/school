import http.server
import socketserver
import socket

PORT = 8000

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Verhindert aggressive Caching-Probleme auf dem iPhone während der Entwicklung
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

local_ip = get_ip()

print("=" * 60)
print(f"🚀 LOKALER SCHUL-APP SERVER GESTARTET!")
print(f"📱 Öffne auf deinem iPhone 14 Pro folgende Adresse in Safari:")
print(f"\n    http://{local_ip}:{PORT}\n")
print("=" * 60)

with socketserver.TCPServer(("0.0.0.0", PORT), NoCacheHTTPRequestHandler) as httpd:
    httpd.serve_forever()
