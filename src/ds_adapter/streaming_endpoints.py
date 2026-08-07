import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# --- Placeholder for State Emitter Access ---
# In a real application, the state_emitter would be managed via dependency injection
# or imported from a central configuration. For this example, we simulate an emitter.

class MockStateEmitter:
    """A mock emitter that simulates events using an asyncio.Queue."""
    def __init__(self):
        self._queue = asyncio.Queue()

    async def emit(self, state: dict):
        """Put an event into the queue."""
        await self._queue.put(state)

    async def get_events(self):
        """An async generator to yield events from the queue."""
        while True:
            try:
                # Wait for an event, with a timeout to allow checking for client disconnection
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                yield event
                self._queue.task_done()
            except asyncio.TimeoutError:
                # If timeout occurs, continue loop to check for client disconnection
                continue
            except asyncio.CancelledError:
                print("MockStateEmitter event generator cancelled.")
                break
            except Exception as e:
                print(f"Error in MockStateEmitter event generator: {e}")
                await asyncio.sleep(1) # Avoid tight loop on persistent errors

# Instantiate the mock emitter globally for simplicity in this example.
# In a DI system, this would be managed by the container.
_mock_state_emitter_instance = MockStateEmitter()

async def simulate_background_events():
    """Simulates events being emitted in the background."""
    i = 0
    while True:
        await _mock_state_emitter_instance.emit({
            "event_id": i,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {"message": f"System update {i}", "level": "info"}
        })
        i += 1
        await asyncio.sleep(2) # Emit an event every 2 seconds

# Start the simulation task if not already running
if not hasattr(simulate_background_events, "task") or simulate_background_events.task.done():
    simulate_background_events.task = asyncio.create_task(simulate_background_events())

def get_global_state_emitter():
    """Provides access to the global mock state emitter instance."""
    return _mock_state_emitter_instance

# --- SSE Endpoint Definition ---

async def state_event_stream(request: Request):
    """Server-Sent Events endpoint that streams state events."""
    state_emitter = get_global_state_emitter()
    
    async def event_generator():
        async for event_data in state_emitter.get_events():
            # Check if the client is still connected
            if await request.is_disconnected():
                print("SSE Client disconnected.")
                break
            
            try:
                # Format the event data for SSE
                # The data should be JSON serializable
                data_str = json.dumps(event_data)
                
                # SSE format: data: <json_string>\n\n
                # Including event type and ID for better client handling
                sse_message = f"event: system_update\nid: {event_data.get('event_id', '')}\ndata: {data_str}\n\n"
                yield sse_message
                
            except Exception as e:
                print(f"Error formatting or sending SSE event: {e}")
                # Optionally, send an error event to the client
                yield f"event: error\ndata: {{json.dumps({{'error': str(e)}})}}\\n\n"
                await asyncio.sleep(5) # Wait before retrying after an error

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# --- Example of how this endpoint could be integrated into a FastAPI app ---
# from fastapi import FastAPI
# from datetime import datetime # Ensure datetime is imported if used in simulation

# app = FastAPI()
# app.add_api_route("/stream/state", state_event_stream, methods=["GET"])

# To run this example:
# 1. Save the code as src/ds_adapter/streaming_endpoints.py
# 2. Create a main.py with:
#    from fastapi import FastAPI
#    from src.ds_adapter.streaming_endpoints import state_event_stream
#    app = FastAPI()
#    app.add_api_route("/stream/state", state_event_stream, methods=["GET"])
# 3. Run with: uvicorn main:app --reload
# 4. Access http://127.0.0.1:8000/stream/state in your browser or with curl.
