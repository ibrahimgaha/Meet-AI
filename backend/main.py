import asyncio
import json
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.meetings import router as meetings_router
from backend.services.meeting_service import meeting_service
from meet.browser import launch_chrome_with_debug, is_chrome_debug_running


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically ensure Chrome is running on port 9222 at app startup
    if not is_chrome_debug_running():
        print("⚡ Startup: Launching Chrome with remote debugging...")
        launch_chrome_with_debug()
    else:
        print("⚡ Startup: Chrome CDP already active on port 9222.")
    yield


app = FastAPI(
    title="Meet-AI API",
    description="Local AI Meeting Assistant API Layer",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(meetings_router)


@app.websocket("/ws/meetings/{meeting_id}")
async def websocket_meeting_events(websocket: WebSocket, meeting_id: str):
    """
    WebSocket endpoint providing real-time live events, state transitions,
    and participant updates for a given meeting session.
    """
    await websocket.accept()
    queue = meeting_service.subscribe(meeting_id)

    # Send current state snapshot immediately upon connection
    active = meeting_service.get_active_meeting()
    if active and active.meeting_id == meeting_id:
        await websocket.send_text(json.dumps(active.to_dict()))

    try:
        while True:
            # Wait for event from queue with timeout to allow ping/liveness checks
            try:
                event_data = await asyncio.wait_for(queue.get(), timeout=1.0)
                await websocket.send_text(json.dumps(event_data))
            except asyncio.TimeoutError:
                # Keep-alive ping if connection remains open
                pass
    except (WebSocketDisconnect, ConnectionResetError):
        pass
    finally:
        meeting_service.unsubscribe(meeting_id, queue)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Meet-AI"}


# Mount static production frontend build if available
frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
