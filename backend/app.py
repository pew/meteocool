from threading import Lock

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, Namespace

app = Flask(__name__)
app.config["SECRET_KEY"] = "lolCool22!"
socketio = SocketIO(app)

thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    url = "https://www.monster.com/"
    while True:
        socketio.sleep(2)
        count += 1
        socketio.emit(
            "map_update",
            {"data": "this could be map tile url", "count": count, "url": url},
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
    socketio.run(app)