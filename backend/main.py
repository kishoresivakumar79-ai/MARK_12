"""
MARK 12 Master Server
FastAPI Application with Static HUD Mounting, REST Endpoints, and WebSocket Gateway.
Includes standard-library HTTP fallback server for immediate zero-dependency execution.
"""
import os
import sys
import json
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.repository import Repository
from core.orchestrator import global_orchestrator
from core.assistant import mark_12
from backend.config import settings

# Initialize database tables on server startup
Repository.init_tables()
global_orchestrator.startup()

# Check for FastAPI / Uvicorn availability
FASTAPI_AVAILABLE = False
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, HTMLResponse
    from backend.api import chat, voice, memory, tasks, files, vision, automation, agents, system, auth
    from backend.websocket.connection import global_ws_manager
    from backend.websocket.events import handle_websocket_message
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="MARK 12 – AI Personal Life Assistant",
        description="Personal AI Operating System with Multi-Agent Intelligence, Computer Automation & Memory",
        version="2.0.0"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API routers
    app.include_router(chat.router)
    app.include_router(voice.router)
    app.include_router(memory.router)
    app.include_router(tasks.router)
    app.include_router(files.router)
    app.include_router(vision.router)
    app.include_router(automation.router)
    app.include_router(agents.router)
    app.include_router(system.router)
    app.include_router(auth.router)

    # WebSocket gateway
    @app.websocket("/ws/assistant")
    async def websocket_assistant_endpoint(websocket: WebSocket):
        await global_ws_manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await handle_websocket_message(websocket, data)
        except WebSocketDisconnect:
            global_ws_manager.disconnect(websocket)
        except Exception:
            global_ws_manager.disconnect(websocket)

    # Mount storage directory
    storage_path = BASE_DIR / "storage"
    storage_path.mkdir(parents=True, exist_ok=True)
    app.mount("/storage", StaticFiles(directory=str(storage_path)), name="storage")

    # Mount static frontend directory
    static_path = BASE_DIR / "backend" / "static"
    static_path.mkdir(parents=True, exist_ok=True)

    @app.get("/")
    async def root():
        index_file = static_path / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return HTMLResponse("<h1>MARK 12 Core Online</h1><p>Navigate to /api/system/status for telemetry.</p>")

    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")

else:
    # High-Performance Standard-Library Fallback Server
    import http.server
    import urllib.parse
    from backend.api import chat, memory, tasks, system, agents, automation

    class StandardLibraryJarvisHandler(http.server.BaseHTTPRequestHandler):
        def _send_json(self, data, code=200):
            payload = json.dumps(data).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.end_headers()
            self.wfile.write(payload)

        def _send_file(self, file_path, mime_type="text/html"):
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
            else:
                self._send_json({"error": "File not found"}, 404)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            self.end_headers()

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            params = urllib.parse.parse_qs(parsed.query)

            if path == "/":
                self._send_file(str(BASE_DIR / "backend" / "static" / "index.html"), "text/html")
            elif path.startswith("/static/") or path.endswith((".css", ".js", ".png", ".jpg", ".svg")):
                clean_rel = path.lstrip("/")
                target = BASE_DIR / "backend" / "static" / clean_rel
                mime = "text/css" if path.endswith(".css") else ("application/javascript" if path.endswith(".js") else "text/html")
                self._send_file(str(target), mime)
            elif path.startswith("/storage/"):
                clean_rel = path.replace("/storage/", "")
                target = BASE_DIR / "storage" / clean_rel
                mime = "image/png" if path.endswith(".png") else ("image/jpeg" if path.endswith(".jpg") else "audio/mpeg")
                self._send_file(str(target), mime)
            elif path == "/api/system/status":
                self._send_json(system.get_telemetry())
            elif path == "/api/agents":
                self._send_json(agents.get_agent_overview())
            elif path == "/api/tasks":
                view = params.get("view", ["flat"])[0]
                status = params.get("status", [None])[0]
                self._send_json(tasks.list_tasks(status=status, view=view))
            elif path == "/api/memory":
                q = params.get("query", [""])[0]
                self._send_json(memory.list_or_search_memories(query=q))
            elif path == "/api/chat/history":
                conv_id = params.get("conversation_id", ["default"])[0]
                self._send_json(chat.handle_get_history(conv_id))
            elif path == "/api/automation/logs":
                self._send_json(automation.get_automation_logs())
            else:
                # Try serving from backend/static
                cand = BASE_DIR / "backend" / "static" / path.lstrip("/")
                if cand.exists() and cand.is_file():
                    self._send_file(str(cand))
                else:
                    self._send_json({"error": "Endpoint not found"}, 404)

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            content_length = int(self.headers.get('Content-Length', 0))
            body_bytes = self.rfile.read(content_length)
            body_json = {}
            if body_bytes:
                try:
                    body_json = json.loads(body_bytes.decode('utf-8'))
                except Exception:
                    body_json = {}

            if path == "/api/chat":
                res = chat.handle_chat_message(body_json)
                self._send_json(res)
            elif path == "/api/memory":
                res = memory.save_memory(body_json)
                self._send_json(res)
            elif path == "/api/tasks":
                res = tasks.create_task(body_json)
                self._send_json(res)
            elif path == "/api/agents/workflow":
                obj = body_json.get("objective", "")
                self._send_json(agents.run_agent_workflow(obj))
            elif path == "/api/automation/execute":
                act = body_json.get("action", "")
                target = body_json.get("target", "")
                self._send_json(automation.execute_automation(act, target))
            else:
                self._send_json({"error": "Post route not recognized"}, 404)

        def log_message(self, format, *args):
            return # Suppress default noisy access logging

    app = None

def start_server():
    host = settings.HOST
    port = settings.PORT
    print(f"\n=======================================================")
    print(f"  ⚡ MARK 12 – AI Personal Life Assistant ⚡")
    print(f"  Mode: {'FastAPI ASGI' if FASTAPI_AVAILABLE else 'Standard Python HTTP'}")
    print(f"  Address: http://{host}:{port}")
    print(f"  Voice, Memory, Multi-Agent & Automation Online.")
    print(f"=======================================================\n")

    if FASTAPI_AVAILABLE:
        import uvicorn
        uvicorn.run("backend.main:app", host=host, port=port, reload=False)
    else:
        server = http.server.ThreadingHTTPServer((host, port), StandardLibraryJarvisHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()

if __name__ == "__main__":
    start_server()
