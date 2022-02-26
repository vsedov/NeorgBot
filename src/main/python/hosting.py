from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "Your bot is ready"

def run():
    app.run(host="0.0.0.0", port=8000)

def keep_running():
    server = Thread(target=run)
    server.start()