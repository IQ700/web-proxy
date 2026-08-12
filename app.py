from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Simple Web Proxy</h1>
        <form action="/proxy" method="get">
            URL: <input name="url" type="text" placeholder="https://example.com" required>
            <input type="submit" value="Go">
        </form>
    '''

@app.route('/proxy')
def proxy():
    tgt_url = request.args.get('url')
    if not tgt_url:
        return "No URL provided."
    
    try:
        resp = requests.get(tgt_url, timeout=10)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() 
                   if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
