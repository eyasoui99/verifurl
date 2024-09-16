from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time  # For calculating execution time

app = Flask(__name__)

def get_status_code(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
                                        args=["--no-sandbox", 
                                              "--disable-setuid-sandbox", 
                                              "--disable-dev-shm-usage",
                                              "--remote-debugging-port=9222",  # Enable remote debugging
                                              "--window-position=-10000,-10000"  # Move the window offscreen (hidden)
            ])  # headless=True to run without opening the browser window
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

    # Start the timer
    start_time = time.time()

    # Get the status code
    status_code = get_status_code(url)

    # Calculate execution time
    execution_time = time.time() - start_time

    # Return the result along with execution time
    return jsonify({
        "url": url,
        "status_code": status_code,
        "execution_time_seconds": execution_time
    })

if __name__ == '__main__':
    app.run(debug=True)
