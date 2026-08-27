import http.server
import socketserver
import os
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Load .env file
env_path = Path(__file__).parent / ".env"
ENV_VARS = {}
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                ENV_VARS[k.strip()] = v.strip()

PORT = int(ENV_VARS.get("PORT", 8000))
CLIENT_ID = ENV_VARS.get("SENTINEL_HUB_CLIENT_ID", "fc4ce036-bc23-42f7-813f-2c3af0b184cb")
CLIENT_SECRET = ENV_VARS.get("SENTINEL_HUB_CLIENT_SECRET", "1RdWAHetSwhKoEx4GSdybkQQr2fr1Qov")

cached_token = None
token_expiry = 0

def get_sentinel_token():
    global cached_token, token_expiry
    now = time.time()
    if cached_token and now < token_expiry - 60:
        return cached_token
    
    try:
        data = urllib.parse.urlencode({
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }).encode('utf-8')
        
        req = urllib.request.Request(
            'https://services.sentinel-hub.com/oauth/token',
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            cached_token = res_json.get('access_token')
            expires_in = res_json.get('expires_in', 3600)
            token_expiry = now + expires_in
            print(f"[Sentinel Hub] New OAuth 2.0 token obtained (Expires in {expires_in}s)")
            return cached_token
    except Exception as e:
        print(f"[Sentinel Hub] Token fetch error: {e}")
        return None

class SkyRaiHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            token = get_sentinel_token()
            config = {
                "status": "connected" if token else "error",
                "provider": "Sentinel Hub (Copernicus Sentinel-2 10m L2A)",
                "clientId": CLIENT_ID,
                "hasToken": bool(token),
                "resolution": "10m Sentinel-2",
                "soilGridsUrl": ENV_VARS.get("SOILGRIDS_REST_URL", "https://rest.isric.org/soilgrids/v2.0"),
                "openMeteoUrl": ENV_VARS.get("OPEN_METEO_BASE_URL", "https://api.open-meteo.com/v1/forecast")
            }
            self.wfile.write(json.dumps(config, ensure_ascii=False).encode('utf-8'))
            return
        elif self.path == '/api/sentinel/token':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            token = get_sentinel_token()
            resp = {
                "access_token": token,
                "token_type": "Bearer",
                "client_id": CLIENT_ID,
                "status": "live"
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return
        elif self.path == '/' or self.path == '/index.html':
            self.path = '/skyrai.html'
        
        super().do_GET()

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    with socketserver.TCPServer(("", PORT), SkyRaiHandler) as httpd:
        print(f"[SKYRAI] Server active at http://localhost:{PORT}")
        print(f"[SKYRAI] Sentinel Hub OAuth Client: {CLIENT_ID[:8]}... (Sentinel-2 10m)")
        httpd.serve_forever()
