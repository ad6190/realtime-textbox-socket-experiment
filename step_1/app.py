from gevent import monkey
monkey.patch_all()

import cgi
import redis
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)
db.set('text', '')


@app.route('/sample')
def sample():
    return render_template('sample.html')


@socketio.on('connect', namespace='/pypy')
def ws_conn():
    c = db.get('text')
    socketio.emit('text', {'text': cgi.escape(c)},
                  namespace="/pypy")


@socketio.on('text', namespace='/pypy')
def ws_sample(message):
    db.set('text', message['text'])
    socketio.emit('text', {'text': cgi.escape(message['text'])},
                  namespace="/pypy", broadcast=True)

if __name__ == '__main__':
    socketio.run(app)