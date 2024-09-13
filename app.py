from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright


app = Flask(__name__)

def get_status_code(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
                                        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"])  # headless=True to run without opening the browser window
        page = browser.new_page()
        try:
            response = page.goto(url)
            status_code = response.status
        except Exception as e:
            status_code = f"Error: {e}"
        browser.close()
        return status_code

@app.route('/get_status', methods=['GET'])
def get_status():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    status_code = get_status_code(url)
    return jsonify({"url": url, "status_code": status_code})

if __name__ == '__main__':
    app.run(debug=True)
