#!/usr/bin/env python
from flask import Flask
import logging, os, json, flask, flask_socketio, config, time
from zero_hid import Keyboard, Mouse

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
moverActive = False

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

@socketio.on('mover')
def mover():
    global moverActive
    logger.info('mover')
    moverActive = not moverActive
    if moverActive:
        socketio.start_background_task(mover_thread())
        
    return moverActive

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
    return flask.render_template('index.html', moverActive=moverActive)

@app.route('/v2', methods=['GET'])
def indexv2_get():
    return flask.render_template('indexv2.html', moverActive=moverActive)

def mover_thread():
    global moverActive
    print(" Mover Thread started")
    while moverActive:
        print("Moving ...")
        try:
            with Mouse() as m:
                m.move(5,0)
                m.move(0,-5)
                m.move(-5,0)
                m.move(0,5)
        except:
            pass
        time.sleep(60)
    print(" Mover Thread stopped")

def startMouseMover():        
    logger.info('startMouseMover')
    global moverActive   
    if moverActive:
        logger.info("Mouse Mover already active.")
    else:
        logger.info("Starting Mouse Mover.")
        moverActive = True
        socketio.start_background_task(mover_thread())        

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    debug = 'DEBUG' in os.environ
    
    loadMoverOnStartup = True
    if loadMoverOnStartup:
        startMouseMover()

    socketio.run(app,
                 host=host,
                 port=port,
                 debug=True,
                 allow_unsafe_werkzeug=True)    
