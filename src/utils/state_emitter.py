from collections import defaultdict

class EventEmitter:
    def __init__(self):
        self._listeners = defaultdict(list)

    def on(self, event, listener):
        self._listeners[event].append(listener)
        return self

    def off(self, event, listener=None):
        if listener is None:
            self._listeners.pop(event, None)
        else:
            if event in self._listeners:
                try:
                    self._listeners[event].remove(listener)
                except ValueError:
                    pass
        return self

    def emit(self, event, *args, **kwargs):
        listeners = list(self._listeners.get(event, []))
        for listener in listeners:
            try:
                listener(*args, **kwargs)
            except Exception:
                pass
        return True

class StateEmitter:
    def __init__(self):
        self._emitter = EventEmitter()

    def on(self, event, listener):
        self._emitter.on(event, listener)

    def off(self, event, listener=None):
        self._emitter.off(event, listener)

    def emit(self, event, *args, **kwargs):
        self._emitter.emit(event, *args, **kwargs)

# Create a global instance of the StateEmitter
state_emitter = StateEmitter()

__all__ = ['state_emitter', 'StateEmitter']
