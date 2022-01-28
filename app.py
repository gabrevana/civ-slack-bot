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

lst = [os.getenv('PLAYER1'), os.getenv('PLAYER2'), os.getenv('PLAYER3'), os.getenv('PLAYER4'), os.getenv('PLAYER5')]
lst_len = len(lst)
index = 0


@bolt_app.message("!t")
def greetings(say: Say):
    """ Checks all messages and if it has '!t' in it the bot will send a channel message @ the current player ready
    to play """
    say(f"It is currently <@{lst[index]}> turn")


@bolt_app.message("!c")
def greetings(say: Say):
    """ Checks all messages and if it has '!c' in it the bot will send a channel message @ the next player ready to
    play """
    global index
    index = (index + 1) % lst_len
    say(f"Next one to play is: <@{lst[index]}>")


handler = SlackRequestHandler(bolt_app)


@app.route("/civ/events", methods=["POST"])
def slack_events():
    """ Declaring the route where slack will post a request """
    return handler.handle(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
