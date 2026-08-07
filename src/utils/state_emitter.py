import eventemitter3

class StateEmitter:
    def __init__(self):
        self._emitter = eventemitter3.EventEmitter()

    def on(self, event, listener):
        self._emitter.on(event, listener)

    def off(self, event, listener=None):
        self._emitter.off(event, listener)

    def emit(self, event, *args, **kwargs):
        self._emitter.emit(event, *args, **kwargs)

# Create a global instance of the StateEmitter
state_emitter = StateEmitter()

__all__ = ['state_emitter']
