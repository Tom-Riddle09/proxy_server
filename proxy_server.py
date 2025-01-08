from flask import Flask, request, Response,jsonify
import requests

app = Flask(__name__)

@app.route('/bypass', methods=['GET'])
def fetch_data():
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # print(target_url)
    # Get the target URL from query parameters
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "Target URL not provided"}), 400
    
    try:
        # Make the request to the target URL
        response = requests.get(target_url,headers=headers)
        print(response)
        # print(response.text)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        
        # Forward the response as-is
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/octet-stream')
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
