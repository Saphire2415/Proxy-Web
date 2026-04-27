from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/api/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "URL is missing", 400
    
    try:
        # Gerçek bir tarayıcı gibi görünmek için Header ekliyoruz
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        res = requests.get(target_url, headers=headers, timeout=15)
        
        # Güvenlik engellerini (X-Frame-Options vb.) temizleyen filtre
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'x-frame-options', 'content-security-policy']
        response_headers = {k: v for k, v in res.headers.items() if k.lower() not in excluded_headers}
        
        return Response(res.content, status=res.status_code, headers=response_headers)
    except Exception as e:
        return f"Proxy Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
