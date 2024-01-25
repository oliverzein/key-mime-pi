#!/usr/bin/env python
from flask import Flask
import time, logging, os, json, flask, flask_socketio, hid, js_to_hid
import config

root_logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-15s %(levelname)-4s %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
root_logger.addHandler(flask.logging.default_handler)
root_logger.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('werkzeug').setLevel(logging.INFO)

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

def _parse_key_event(payload):
    return js_to_hid.JavaScriptKeyEvent(meta_modifier=payload['metaKey'],
                                        alt_modifier=payload['altKey'],
                                        shift_modifier=payload['shiftKey'],
                                        ctrl_modifier=payload['ctrlKey'],
                                        key=payload['key'],
                                        key_code=payload['keyCode'])


def _parse_key_event_from_char(char):
    return js_to_hid.JavaScriptKeyEvent(meta_modifier=False,
                                        alt_modifier=False,
                                        shift_modifier=False,
                                        ctrl_modifier=False,
                                        key='x',
                                        key_code=char)

@socketio.on('string')
def test_string(message):
    string = message['string']
    logger.info('Send String: %s', string)
    for character in string:
        ascval = ord(character)
        logger.info('Char: %s = %d', character, ascval)
        control_keys, hid_keycode = js_to_hid.convert2(ascval)
        logger.info(hid_keycode)
        hid.send(hid_path, control_keys, hid_keycode)
        # if ascval == 34 or ascval == 39:
        #    hid.send(hid_path, 0, 0x2c)
        time.sleep(0.03)

@socketio.on('keystroke')
def socket_keystroke(message):
    key_event = _parse_key_event(message)
    hid_keycode = None
    success = False
    try:
        control_keys, hid_keycode = js_to_hid.convert(key_event)
    except js_to_hid.UnrecognizedKeyCodeError:
        logger.warning('Unrecognized key: %s (keycode=%d)', key_event.key,
                       key_event.key_code)
    if hid_keycode is None:
        logger.info('Ignoring %s key (keycode=%d)', key_event.key,
                    key_event.key_code)
    else:
        hid.send(hid_path, control_keys, hid_keycode)
        success = True

    socketio.emit('keystroke-received', {'success': success})

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
