from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app,host='0.0.0.0', debug=True,allow_unsafe_werkzeug=True) 