import requests
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # রিকোয়েস্টের বডি থেকে ডেটা পড়া
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data)
            uid = req_data.get('uid')

            if not uid:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "UID is missing"}).encode())
                return

            # Garena API-কে কল করার জন্য প্রয়োজনীয় তথ্য
            url = "https://shop.garena.sg/api/auth/player_id_login"
            payload = {"account_id": uid, "app_id": 100067}

            res = requests.post(url, json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
            
            # সফল উত্তর পাঠানো
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        except Exception as e:
            # কোনো সমস্যা হলে এরর পাঠানো
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Internal Server Error", "details": str(e)}).encode())
            
        return
