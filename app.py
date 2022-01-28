""" Civilization 6 Bot for slack """
import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
bolt_app = App(token=os.getenv('SLACK_BOT_TOKEN'), signing_secret=os.getenv('SLACK_SIGNING_SECRET'))

user = None


@bolt_app.message('!c')
def greetings(payload: dict, say: Say):
    """ This will check all the message and pass only those which has 'hello slacky' in it """
    global user
    user = payload.get("user")

    match user:
        case os.getenv('PLAYER1'):
            say(f"It is your <@{os.getenv('PLAYER2')}>")
            user = os.getenv('PLAYER2')

        case os.getenv('PLAYER2'):
            say(f"It is your <@{os.getenv('PLAYER3')}>")
            user = os.getenv('PLAYER3')

        case os.getenv('PLAYER3'):
            say(f"It is your <@{os.getenv('PLAYER4')}>")
            user = os.getenv('PLAYER4')

        case os.getenv('PLAYER4'):
            say(f"It is your <@{os.getenv('PLAYER5')}>")
            user = os.getenv('PLAYER5')

        case os.getenv('PLAYER5'):
            say(f"It is your <@{os.getenv('PLAYER1')}>")
            user = os.getenv('PLAYER1')


@bolt_app.message('!t')
def greetings(say: Say):
    """ Checks all messages and if it has '!t' in it the bot will send a channel message @ the current player ready
    to play """
    say(f"It is currently <@{user}> turn")


handler = SlackRequestHandler(bolt_app)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
