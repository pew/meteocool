from threading import Lock

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, Namespace
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "lolCool22!"
socketio = SocketIO(app)

thread = None
thread_lock = Lock()

# flugzeug tilejson
fz = '{"name":"Aeronautical chart FAA","description":"","attribution":"","type":"overlay","version":"1","format":"png","minzoom":5,"maxzoom":11,"bounds":[-124.111656,32.028685,-116.924543,40.448629],"scale":"1","basename":"faa","profile":"mercator","tiles":["http://tileserver.maptiler.com/faa/{z}/{x}/{y}.png"],"tilejson":"2.0.0","scheme":"xyz","grids":["http://tileserver.maptiler.com/faa/{z}/{x}/{y}.grid.json"]}'
weather = '{"name":"Weather Underground","description":"","attribution":"","type":"overlay","version":"1","format":"png","minzoom":0,"maxzoom":6,"bounds":[-179.999941,-60.010742,179.993412,59.982],"scale":"1","basename":"weather","profile":"mercator","tiles":["http://tileserver.maptiler.com/weather/{z}/{x}/{y}.png"],"tilejson":"2.0.0","scheme":"xyz","grids":["http://tileserver.maptiler.com/weather/{z}/{x}/{y}.grid.json"]}'


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        if count % 2 == 0:
            socketio.emit(
                "map_update",
                json.loads(fz),
                namespace="/tile",
            )
        else:
            socketio.emit(
                "map_update",
                json.loads(weather),
                namespace="/tile",
            )



@app.route("/")
def index():
    return "OK"


@socketio.on("connect", namespace="/tile")
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit("map_update", {"data": "Connected", "count": 0})


if __name__ == "__main__":
    print("Started app.py")
    socketio.run(app)