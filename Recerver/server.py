from flask import Flask, request, render_template_string
import uuid
import os

app = Flask(__name__)

# Directory to store keys
KEYS_DIR = "keys"
os.makedirs(KEYS_DIR, exist_ok=True)

# HTML Template for the GUI
HTML_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>Retrieve Encryption Key</title>
    </head>
    <body>
        <h1>Retrieve Encryption Key</h1>
        <form action="/get_key" method="POST">
            <label for="unique_id">Enter your unique ID:</label><br>
            <input type="text" id="unique_id" name="unique_id" required><br><br>
            <button type="submit">Retrieve Key</button>
        </form>
        {% if key %}
        <h2>Your Key:</h2>
        <p>{{ key }}</p>
        {% endif %}
    </body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, key=None)

@app.route('/store_key', methods=['POST'])
def store_key():
    key = request.data.decode('utf-8')  # Get the key from the POST request
    unique_id = str(uuid.uuid4())  # Generate a unique ID
    key_file_path = os.path.join(KEYS_DIR, f"{unique_id}.key")
    
    # Save the key to a file
    with open(key_file_path, "wb") as f:
        f.write(key.encode())
    
    return f"Key received and stored as '{unique_id}.key'! Your unique ID is {unique_id}"

@app.route('/get_key', methods=['POST'])
def get_key():
    unique_id = request.form.get('unique_id')  # Get the ID from the form
    key_file_path = os.path.join(KEYS_DIR, f"{unique_id}.key")
    
    # Retrieve the key
    if os.path.exists(key_file_path):
        with open(key_file_path, "rb") as f:
            key = f.read().decode('utf-8')
        return render_template_string(HTML_TEMPLATE, key=key)
    else:
        return render_template_string(HTML_TEMPLATE, key="Key not found. Please check your unique ID.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4998)  # Run on port 4998

