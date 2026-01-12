# N8N Response Workflow - دليل استقبال الردود من n8n

## 📋 نظرة عامة

تم تحديث النظام ليستقبل الردود من n8n webhook ويعرضها مباشرة في واجهة الشات، بدلاً من الاعتماد فقط على OpenAI.

## 🔄 كيفية عمل الـ Workflow

### 1. إرسال الرسالة
عندما يرسل المستخدم رسالة:
- يتم إرسال الرسالة إلى n8n webhook عبر POST request
- ينتظر النظام الرد من n8n
- إذا استجاب n8n، يتم عرض رده في الشات
- إذا لم يستجب n8n، يتم استخدام OpenAI كبديل احتياطي

### 2. تنسيق الرد من n8n
n8n يرجع البيانات في أحد التنسيقات التالية:

#### تنسيق Array (الأكثر شيوعاً)
```json
[
  {
    "message": "هذا هو الرد من n8n",
    "timestamp": "2026-01-11T16:42:00"
  }
]
```

#### تنسيق Object
```json
{
  "response": "هذا هو الرد من n8n",
  "timestamp": "2026-01-11T16:42:00"
}
```

### 3. استخراج الرد
النظام يبحث عن الرد في الحقول التالية بالترتيب:
1. `response`
2. `message`
3. `reply`
4. `output`
5. إذا لم يجد أي منها، يستخدم كامل الـ object كنص

## 🛠️ إعداد n8n Workflow

### الخطوة 1: إنشاء Webhook Node
```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "moj-ai-chat",
        "responseMode": "responseNode",
        "options": {}
      },
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [0, 0],
      "name": "Webhook"
    }
  ]
}
```

### الخطوة 2: معالجة الرسالة
أضف nodes لمعالجة الرسالة (مثل AI Agent، Database Query، إلخ)

### الخطوة 3: إرجاع الرد
```json
{
  "nodes": [
    {
      "parameters": {
        "respondWith": "allIncomingItems",
        "options": {}
      },
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.5,
      "position": [400, 0],
      "name": "Respond to Webhook"
    }
  ]
}
```

## 📝 مثال على Workflow كامل

```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "moj-ai-chat",
        "responseMode": "responseNode"
      },
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [0, 0],
      "name": "Webhook"
    },
    {
      "parameters": {
        "jsCode": "// معالجة الرسالة\nconst userMessage = $input.item.json.message;\n\n// هنا يمكنك إضافة منطق معالجة الرسالة\n// مثل استدعاء AI، قاعدة بيانات، إلخ\n\nreturn {\n  message: `تم استقبال رسالتك: ${userMessage}`,\n  timestamp: new Date().toISOString(),\n  processed: true\n};"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [200, 0],
      "name": "Process Message"
    },
    {
      "parameters": {
        "respondWith": "allIncomingItems"
      },
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.5,
      "position": [400, 0],
      "name": "Respond to Webhook"
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Process Message", "type": "main", "index": 0 }]]
    },
    "Process Message": {
      "main": [[{ "node": "Respond to Webhook", "type": "main", "index": 0 }]]
    }
  }
}
```

## 🔧 التكوين في .env

تأكد من إضافة إعدادات n8n في ملف `.env`:

```env
# N8N Webhook Configuration
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/moj-ai-chat
N8N_WEBHOOK_ENABLED=True
```

## 📊 تنسيق البيانات المرسلة إلى n8n

عندما يرسل المستخدم رسالة، يتم إرسال البيانات التالية إلى n8n:

```json
{
  "message": "رسالة المستخدم",
  "timestamp": "2026-01-11T16:42:00.000Z",
  "source": "moj_ai_chatbot",
  "type": "user_message",
  "session_id": "optional-session-id",
  "user_id": "optional-user-id",
  "metadata": {
    "source": "websocket"
  }
}
```

## 🎯 أمثلة على حالات الاستخدام

### 1. رد بسيط
```json
{
  "message": "مرحباً! كيف يمكنني مساعدتك؟"
}
```

### 2. رد مع بيانات إضافية
```json
{
  "response": "تم معالجة طلبك بنجاح",
  "data": {
    "order_id": "12345",
    "status": "completed"
  },
  "timestamp": "2026-01-11T16:42:00"
}
```

### 3. رد من AI Agent
```json
{
  "message": "بناءً على تحليل البيانات، أوصي بـ...",
  "confidence": 0.95,
  "sources": ["database", "api"]
}
```

## 🔍 استكشاف الأخطاء

### المشكلة: لا يتم استقبال الرد من n8n
**الحل:**
1. تحقق من أن `N8N_WEBHOOK_ENABLED=True` في `.env`
2. تأكد من صحة `N8N_WEBHOOK_URL`
3. تحقق من أن n8n workflow يحتوي على "Respond to Webhook" node
4. راجع logs في `app/services/webhook_service.py`

### المشكلة: الرد فارغ أو غير صحيح
**الحل:**
1. تحقق من تنسيق الرد من n8n
2. تأكد من أن الرد يحتوي على أحد الحقول: `response`, `message`, `reply`, `output`
3. راجع logs لمعرفة البيانات المستقبلة

### المشكلة: timeout error
**الحل:**
1. زيادة timeout في `webhook_service.py` (حالياً 10 ثواني)
2. تحسين أداء n8n workflow
3. استخدام async processing في n8n

## 📈 التحسينات المستقبلية

- [ ] إضافة retry mechanism
- [ ] دعم streaming responses
- [ ] إضافة caching للردود المتكررة
- [ ] دعم multiple webhooks
- [ ] إضافة rate limiting

## 🔐 الأمان

- تأكد من استخدام HTTPS في production
- أضف authentication headers إذا لزم الأمر
- قم بتشفير البيانات الحساسة
- استخدم rate limiting لمنع الإساءة

## 📚 المراجع

- [n8n Webhook Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [FastAPI WebSocket](https://fastapi.tiangolo.com/advanced/websockets/)
- [httpx Documentation](https://www.python-httpx.org/)

---

**تم التحديث:** 11 يناير 2026
**الإصدار:** 2.0
