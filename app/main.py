import os
from slack_bolt import App
from network_check import MiloNetworkTool
from dotenv import load_dotenv

from flask import Flask, request, render_template
from slack_bolt.adapter.flask import SlackRequestHandler

import threading

# Load env variable form .env file, only local development
load_dotenv()

host = "example.host.com"
services = {
    "ftp": [145, "tcp"],
}

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.command("/network")
def nestowk_status(ack):
    mi = MiloNetworkTool()
    mi.check_all_services(host, services)
    ack(
        blocks=mi.create_slack_block(),
    )


# Init flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/")
def hello():
    return render_template("index.html")


def start_flask():
    flask_app.run()


def start_bolt():
    app.start(port=3000)


# Start your app / only for local development'
if __name__ == "__main__":
    # app.start(port=3000)
    x = threading.Thread(target=start_flask, args=())
    y = threading.Thread(target=start_bolt, args=())
    x.start()
    y.start()
