from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import json
from datetime import datetime
from typing import List
import asyncio
from pathlib import Path

from app.services.ai_service import AIService
from app.services.webhook_service import WebhookService
from app.core.config import settings
from app.db.database import init_db
from app.auth.routes import router as auth_router
from app.api.intent_routes import router as intent_router

app = FastAPI(title="كنق الاتمته - Chatbot API", version="1.0.0")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized")

# Include auth routes
app.include_router(auth_router)

# Include intent recognition routes
app.include_router(intent_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = Path(__file__).parent.parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

ai_service = AIService()
webhook_service = WebhookService()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

manager = ConnectionManager()

# Models for API requests
class MessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    html_file = Path(__file__).parent.parent / "templates" / "chat.html"
    if html_file.exists():
        return FileResponse(html_file)
    return HTMLResponse(content="<h1>Chat interface not found</h1>", status_code=404)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            session_id = message_data.get("session_id", None)
            user_id = message_data.get("user_id", None)
            user_email = message_data.get("user_email", None)
            
            await manager.send_message({
                "type": "user_message",
                "message": user_message,
                "timestamp": datetime.now().isoformat()
            }, websocket)
            
            await manager.send_message({
                "type": "typing",
                "status": True
            }, websocket)
            
            try:
                # الحصول على الرد من n8n webhook فقط
                n8n_response = await webhook_service.send_message_to_n8n(
                    user_message=user_message,
                    session_id=session_id,
                    user_id=user_id,
                    user_email=user_email,
                    metadata={"source": "websocket"}
                )
                
                await manager.send_message({
                    "type": "typing",
                    "status": False
                }, websocket)
                
                # إذا كان هناك رد من n8n، أرسله
                if n8n_response:
                    await manager.send_message({
                        "type": "assistant_message",
                        "message": n8n_response,
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
                else:
                    # إذا لم يكن هناك رد من n8n، أرسل رسالة خطأ
                    await manager.send_message({
                        "type": "error",
                        "message": "عذراً، لم أتمكن من الحصول على رد من النظام. يرجى المحاولة مرة أخرى.",
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
            except Exception as e:
                await manager.send_message({
                    "type": "typing",
                    "status": False
                }, websocket)
                await manager.send_message({
                    "type": "error",
                    "message": f"حدث خطأ: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/send-message")
async def send_message_to_n8n(request: MessageRequest):
    """
    Endpoint POST لإرسال رسالة إلى n8n webhook واستقبال الرد
    
    يمكن استخدام هذا الـ endpoint لإرسال رسائل مباشرة إلى n8n والحصول على الرد
    """
    try:
        n8n_response = await webhook_service.send_message_to_n8n(
            user_message=request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            metadata=request.metadata
        )
        
        if n8n_response:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "تم إرسال الرسالة إلى n8n بنجاح",
                    "response": n8n_response,
                    "timestamp": datetime.now().isoformat()
                }
            )
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "error",
                    "message": "فشل الحصول على رد من n8n. يرجى التحقق من أن n8n webhook يعمل بشكل صحيح.",
                    "timestamp": datetime.now().isoformat()
                }
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء إرسال الرسالة: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
