import unittest
from src.utils.state_emitter import StateEmitter, state_emitter

class TestStateEmitter(unittest.TestCase):
    def test_state_emitter_emit_and_on(self):
        emitter = StateEmitter()
        received_events = []

        def on_event(data):
            received_events.append(data)

        emitter.on("test-event", on_event)
        emitter.emit("test-event", {"info": "hello"})

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0]["info"], "hello")

    def test_state_emitter_off(self):
        emitter = StateEmitter()
        received_events = []

        def on_event(data):
            received_events.append(data)

        emitter.on("test-event", on_event)
        emitter.off("test-event", on_event)
        emitter.emit("test-event", {"info": "hello"})

        self.assertEqual(len(received_events), 0)

    def test_global_state_emitter(self):
        received_events = []

        def on_event(data):
            received_events.append(data)

        state_emitter.on("global-event", on_event)
        state_emitter.emit("global-event", {"val": 42})
        state_emitter.off("global-event", on_event)

        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0]["val"], 42)

if __name__ == '__main__':
    unittest.main()
