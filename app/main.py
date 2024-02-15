#!/usr/bin/env python
from flask import Flask
import logging, os, json, flask, flask_socketio, config
from zero_hid import Keyboard

root_logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-15s %(levelname)-4s %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
root_logger.addHandler(flask.logging.default_handler)
root_logger.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('werkzeug').setLevel(logging.INFO)
logging.getLogger('zero_hid').setLevel(logging.INFO)

# Location of HID file handle in which to write keyboard HID input.
hid_path = os.environ.get('HID_PATH', '/dev/hidg0')

logger.info('Starting app')

config.loadConfig()
socketio = flask_socketio.SocketIO()

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio.init_app(app, async_mode=None, logger=False, engineio_logger=False)
       
    return app

app = createApp()

@socketio.on('string')
def test_string(message):
    string = message['string']
    logger.info('Send String: %s', string)
    k = Keyboard()
    k.set_layout(language='DE_ASCII')
    k.type(string)

@socketio.on('connect')
def test_connect():
    logger.info('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    logger.info('Client disconnected')

@socketio.on('favourites_load')
def favourites_load():
    logger.info('favourites_load')    
    favs_json = json.dumps(config.commands)
    #socketio.emit('favourites_load', favs_json)
    return favs_json

@socketio.on('favourite_add')
def favourite_add(command):
    logger.info('favourite_add: ' + command)
    config.addCommand(command=command)
    
@socketio.on('favourite_remove')
def favourite_remove(command):
    logger.info('favourite_remove: ' + command)
    config.removeCommand(command=command)    

@app.route('/', methods=['GET'])
def index_get():
    return flask.render_template('index.html')

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    debug = 'DEBUG' in os.environ
    
    socketio.run(app,
                 host=host,
                 port=port,
                 debug=True,
                 allow_unsafe_werkzeug=True)
