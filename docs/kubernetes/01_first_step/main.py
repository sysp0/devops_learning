# app.py
from flask import Flask
import socket

app = Flask(__name__)

@app.route('/')
def show_hostname():
    pod_name = socket.gethostname()
    return f"""
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Hello from Kubernetes! 🚀</h1>
            <p>This app is running inside Pod:</p>
            <h2 style="color: blue;">{pod_name}</h2>
            <p>Feel free to visit again to see this in action!</p>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
