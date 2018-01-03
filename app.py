import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '392749767:AAGxUv82yrs-tvNbQvVj0EP2T_RwPGj8C2k'
WEBHOOK_URL = 'https://fc5dac28.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'play',
        'ask',
        'arrest',
        'John',
        'Sam',
        'Mary'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'play',
            'conditions': 'user_to_play'
        },
        {
            'trigger': 'advance',
            'source': 'play',
            'dest': 'ask',
            'conditions': 'play_to_ask'
        }, 
        {
            'trigger': 'advance',
            'source': 'play',
            'dest': 'arrest',
            'conditions': 'play_to_arrest'
        }, 
        {
            'trigger': 'advance',
            'source': 'arrest',
            'dest': 'user',
            'conditions': 'arrest_to_John'
        }, 
        {
            'trigger': 'advance',
            'source': 'arrest',
            'dest': 'user',
            'conditions': 'arrest_to_Sam'
        }, 
        {
            'trigger': 'advance',
            'source': 'arrest',
            'dest': 'user',
            'conditions': 'arrest_to_Mary'
        }, 
        {
            'trigger': 'advance',
            'source': 'ask',
            'dest': 'John',
            'conditions': 'ask_to_John'
        },
        {
            'trigger': 'advance',
            'source': 'ask',
            'dest': 'Sam',
            'conditions': 'ask_to_Sam'
        },
        {
            'trigger': 'advance',
            'source': 'ask',
            'dest': 'Mary',
            'conditions': 'ask_to_Mary'
        },
        {
            'trigger': 'go_back',
            'source': [
                'John',
                'Sam',
                'Mary'
            ],
            'dest': 'play'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
