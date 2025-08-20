def register_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected') 