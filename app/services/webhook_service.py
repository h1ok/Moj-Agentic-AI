import httpx
from app.core.config import settings
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class WebhookService:
    def __init__(self):
        self.webhook_url = settings.N8N_WEBHOOK_URL
        self.enabled = settings.N8N_WEBHOOK_ENABLED and self.webhook_url is not None
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def send_message_to_n8n(
        self,
        user_message: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        إرسال رسالة المستخدم إلى n8n webhook واستقبال الرد
        
        Args:
            user_message: الرسالة التي أرسلها المستخدم
            session_id: معرف الجلسة (اختياري)
            user_id: معرف المستخدم (اختياري)
            metadata: بيانات إضافية (اختياري)
        
        Returns:
            Optional[str]: الرد من n8n إذا نجح، None خلاف ذلك
        """
        if not self.enabled:
            logger.debug("N8N webhook is disabled")
            return None
        
        try:
            payload = {
                "message": user_message,
                "timestamp": datetime.now().isoformat(),
                "source": "moj_ai_chatbot",
                "type": "user_message"
            }
            
            # إضافة البيانات الاختيارية
            if session_id:
                payload["session_id"] = session_id
            
            if user_id:
                payload["user_id"] = user_id
            
            if metadata:
                payload["metadata"] = metadata
            
            # إرسال الطلب إلى n8n webhook وانتظار الرد
            response = await self.client.post(
                self.webhook_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Moj-AI-Chatbot/2.0"
                }
            )
            
            response.raise_for_status()
            logger.info(f"Message sent to n8n webhook successfully. Status: {response.status_code}")
            
            # استخراج الرد من n8n
            response_data = response.json()
            logger.info(f"Full n8n response: {response_data}")
            
            # n8n يرجع البيانات في صيغة array، نأخذ أول عنصر
            if isinstance(response_data, list) and len(response_data) > 0:
                n8n_response = response_data[0]
                logger.info(f"First item in array: {n8n_response}")
                
                # البحث عن الرد في جميع الحقول الممكنة
                reply = None
                if isinstance(n8n_response, dict):
                    # أولاً: تحقق من وجود output.reply (التنسيق الجديد من n8n)
                    if "output" in n8n_response and isinstance(n8n_response["output"], dict):
                        reply = n8n_response["output"].get("reply")
                    
                    # إذا لم نجد في output.reply، ابحث في الحقول الأخرى
                    if not reply:
                        reply = (
                            n8n_response.get("response") or 
                            n8n_response.get("message") or 
                            n8n_response.get("reply") or
                            n8n_response.get("output") or
                            n8n_response.get("text") or
                            n8n_response.get("content") or
                            n8n_response.get("data")
                        )
                
                # إذا لم نجد رد في الحقول المعروفة، استخدم كامل الـ object
                if not reply:
                    reply = str(n8n_response)
                
                logger.info(f"Extracted reply type: {type(reply)}, length: {len(str(reply))}")
                logger.info(f"Extracted reply: {reply[:200] if len(str(reply)) > 200 else reply}")
                
                # تأكد من إرجاع الرد حتى لو كان string فارغ ظاهرياً
                return reply if reply else str(n8n_response)
                
            elif isinstance(response_data, dict):
                logger.info(f"Response is dict: {response_data}")
                # إذا كان الرد dictionary مباشرة
                reply = (
                    response_data.get("response") or 
                    response_data.get("message") or 
                    response_data.get("reply") or
                    response_data.get("output") or
                    response_data.get("text") or
                    response_data.get("content") or
                    response_data.get("data")
                )
                
                if not reply:
                    reply = str(response_data)
                    
                logger.info(f"Extracted reply: {reply[:200] if len(str(reply)) > 200 else reply}")
                return reply
            else:
                logger.warning(f"Unexpected response format from n8n: {response_data}")
                # حتى لو كان التنسيق غير متوقع، أرجع البيانات
                return str(response_data) if response_data else None
            
        except httpx.TimeoutException:
            logger.error("Timeout while sending message to n8n webhook")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while sending to n8n webhook: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Error sending message to n8n webhook: {str(e)}")
            return None
    
    async def send_ai_response_to_n8n(
        self,
        user_message: str,
        ai_response: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> bool:
        """
        إرسال استجابة AI إلى n8n webhook (اختياري)
        
        Args:
            user_message: الرسالة الأصلية للمستخدم
            ai_response: استجابة AI
            session_id: معرف الجلسة (اختياري)
            user_id: معرف المستخدم (اختياري)
        
        Returns:
            bool: True إذا تم الإرسال بنجاح، False خلاف ذلك
        """
        if not self.enabled:
            return False
        
        try:
            payload = {
                "user_message": user_message,
                "ai_response": ai_response,
                "timestamp": datetime.now().isoformat(),
                "source": "moj_ai_chatbot",
                "type": "ai_response"
            }
            
            if session_id:
                payload["session_id"] = session_id
            
            if user_id:
                payload["user_id"] = user_id
            
            response = await self.client.post(
                self.webhook_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Moj-AI-Chatbot/2.0"
                }
            )
            
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Error sending AI response to n8n webhook: {str(e)}")
            return False
    
    async def close(self):
        """إغلاق العميل HTTP"""
        await self.client.aclose()
