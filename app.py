from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time  # For calculating execution time

app = Flask(__name__)

def get_status_code(url):
    execution_times = {}

    with sync_playwright() as p:
        # Measure time to launch the browser
        start_time = time.time()
        browser = p.chromium.launch(headless=False,
                                        args=["--no-sandbox", 
                                              "--disable-setuid-sandbox", 
                                              "--disable-dev-shm-usage",
                                              "--remote-debugging-port=9222",  # Enable remote debugging
                                              "--window-position=-10000,-10000"  # Move the window offscreen (hidden)
        ])
        execution_times['launch_browser'] = time.time() - start_time

        # Measure time to create a new page
        start_time = time.time()
        page = browser.new_page()
        execution_times['create_new_page'] = time.time() - start_time

        # Measure time to navigate to the URL
        start_time = time.time()
        try:
            response = page.goto(url)
            execution_times['navigate_to_url'] = time.time() - start_time

            # Measure time to get the status code
            start_time = time.time()
            status_code = response.status
            execution_times['get_status_code'] = time.time() - start_time
        except Exception as e:
            status_code = f"Error: {e}"
            execution_times['navigate_to_url'] = time.time() - start_time
            execution_times['get_status_code'] = 0  # No status code due to the error

        # Measure time to close the browser
        start_time = time.time()
        browser.close()
        execution_times['close_browser'] = time.time() - start_time

    return status_code, execution_times

@app.route('/get_status', methods=['GET'])
def get_status():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    # Get the status code and execution times for each operation
    status_code, execution_times = get_status_code(url)

    # Return the result along with the execution times
    return jsonify({
        "url": url,
        "status_code": status_code,
        "execution_times": execution_times
    })

if __name__ == '__main__':
    app.run(debug=True)
