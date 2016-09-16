from  gevent import monkey
monkey.patch_all()

import redis
from flask import Flask, render_template
from flask.ext.socketio import SocketIO

app= Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

@app.route('/')
def main():
	c = db.incr('counter')
	return render_template('main.html', counter=c)

if __name__ == '__main__':
	app.run(debug=True)