# 👤 تتبع المستخدمين في n8n Webhook

## دليل استخدام user_id في n8n Orchestra Agent

---

## 📋 نظرة عامة

الآن يرسل النظام **user_id** و **session_id** مع كل رسالة إلى n8n webhook، مما يسمح للوكيل بـ:
- **التعرف على المستخدم** الذي يتواصل معه
- **تخصيص الردود** حسب المستخدم
- **تتبع المحادثات** لكل مستخدم
- **الوصول إلى بيانات المستخدم** من قاعدة البيانات
- **إدارة الجلسات** بشكل أفضل

---

## 📦 البيانات المرسلة إلى n8n

### Webhook Payload

```json
{
  "message": "أضف حساب تويتر الخاص بي",
  "user_id": 123,
  "session_id": "session_1736701234567",
  "timestamp": "2026-01-12T18:30:00.000Z",
  "source": "moj_ai_chatbot",
  "type": "user_message",
  "metadata": {
    "source": "websocket"
  }
}
```

### شرح الحقول

| الحقل | النوع | الوصف | مثال |
|-------|------|-------|------|
| `message` | string | رسالة المستخدم | "أضف حساب تويتر" |
| `user_id` | integer/null | معرف المستخدم من قاعدة البيانات | 123 |
| `session_id` | string | معرف الجلسة الفريد | "session_1736701234567" |
| `timestamp` | string (ISO) | وقت إرسال الرسالة | "2026-01-12T18:30:00.000Z" |
| `source` | string | مصدر الرسالة | "moj_ai_chatbot" |
| `type` | string | نوع الرسالة | "user_message" |
| `metadata` | object | بيانات إضافية | {"source": "websocket"} |

---

## 🔧 استخدام user_id في n8n

### 1. الوصول إلى user_id

في أي Function Node في n8n:

```javascript
// الحصول على user_id من الـ webhook
const userId = $input.item.json.user_id;
const sessionId = $input.item.json.session_id;
const message = $input.item.json.message;

console.log(`User ID: ${userId}`);
console.log(`Session ID: ${sessionId}`);
console.log(`Message: ${message}`);
```

### 2. التحقق من تسجيل المستخدم

```javascript
// التحقق إذا كان المستخدم مسجل دخول
const userId = $input.item.json.user_id;

if (!userId) {
  return {
    message: "يرجى تسجيل الدخول أولاً للوصول إلى هذه الميزة",
    action: "require_login",
    login_url: "http://localhost:3001/login"
  };
}

// المستخدم مسجل، تابع العملية
return {
  message: "مرحباً بك!",
  user_id: userId,
  action: "continue"
};
```

### 3. جلب بيانات المستخدم من قاعدة البيانات

استخدم HTTP Request Node للاتصال بـ API:

```javascript
// في HTTP Request Node
{
  "method": "GET",
  "url": "http://localhost:8000/api/auth/me",
  "headers": {
    "Authorization": "Bearer {{ $json.access_token }}"
  }
}
```

أو استخدم SQL Node مباشرة:

```sql
SELECT id, email, created_at 
FROM users 
WHERE id = {{ $json.user_id }}
```

### 4. تخصيص الردود حسب المستخدم

```javascript
const userId = $input.item.json.user_id;
const message = $input.item.json.message;

// جلب بيانات المستخدم (افترض أنها موجودة)
const userData = {
  id: userId,
  email: "user@example.com",
  accounts: ["twitter", "instagram"]
};

// تخصيص الرد
if (message.includes("حساباتي")) {
  return {
    message: `لديك ${userData.accounts.length} حسابات مرتبطة: ${userData.accounts.join(", ")}`,
    user_id: userId,
    accounts: userData.accounts
  };
}

return {
  message: "كيف يمكنني مساعدتك؟",
  user_id: userId
};
```

### 5. تتبع المحادثات

```javascript
const userId = $input.item.json.user_id;
const sessionId = $input.item.json.session_id;
const message = $input.item.json.message;

// حفظ الرسالة في قاعدة البيانات أو ذاكرة مؤقتة
return {
  conversation_log: {
    user_id: userId,
    session_id: sessionId,
    message: message,
    timestamp: new Date().toISOString(),
    saved: true
  }
};
```

---

## 🎯 أمثلة عملية

### مثال 1: التحقق من الصلاحيات

```javascript
// Function Node: Check User Permissions
const userId = $input.item.json.user_id;
const intent = $input.item.json.intent;

// الميزات التي تتطلب تسجيل دخول
const requiresAuth = [
  "add_account",
  "remove_account",
  "create_post",
  "schedule_post",
  "get_analytics"
];

if (requiresAuth.includes(intent) && !userId) {
  return {
    error: true,
    message: "هذه الميزة تتطلب تسجيل الدخول",
    action: "redirect_to_login"
  };
}

return {
  authorized: true,
  user_id: userId,
  intent: intent
};
```

### مثال 2: إدارة الحسابات حسب المستخدم

```javascript
// Function Node: Get User Accounts
const userId = $input.item.json.user_id;

// استدعاء API للحصول على حسابات المستخدم
// (يمكن استخدام HTTP Request Node قبل هذا)
const userAccounts = $input.item.json.accounts || [];

if (userAccounts.length === 0) {
  return {
    message: "ليس لديك أي حسابات مرتبطة حالياً. هل تريد إضافة حساب؟",
    user_id: userId,
    action: "suggest_add_account"
  };
}

return {
  message: `لديك ${userAccounts.length} حسابات مرتبطة`,
  user_id: userId,
  accounts: userAccounts,
  action: "display_accounts"
};
```

### مثال 3: تخزين تفضيلات المستخدم

```javascript
// Function Node: Save User Preferences
const userId = $input.item.json.user_id;
const message = $input.item.json.message;

// استخراج التفضيلات من الرسالة
const preferences = {
  user_id: userId,
  preferred_platform: "twitter", // مثال
  auto_post_time: "10:00 AM",
  language: "ar"
};

// حفظ في قاعدة البيانات أو Redis
return {
  message: "تم حفظ تفضيلاتك بنجاح",
  user_id: userId,
  preferences: preferences,
  saved: true
};
```

---

## 🔄 Workflow مثالي في n8n

### البنية الموصى بها

```
[Webhook Trigger]
    ↓
[Extract User Data]
    ↓
[Check Authentication] ──→ [Require Login Flow]
    ↓
[Intent Detection API]
    ↓
[Process Intent]
    ↓
[Check User Permissions] ──→ [Unauthorized Flow]
    ↓
[Route by Intent]
    ↓
├─→ [Add Account Flow] ──→ [Save to User's Accounts]
├─→ [Create Post Flow] ──→ [Post to User's Platform]
├─→ [Analytics Flow] ──→ [Fetch User's Analytics]
└─→ [Help Flow]
    ↓
[Response with User Context]
```

### كود مثالي لـ Extract User Data Node

```javascript
// Function Node: Extract User Data
const userId = $input.item.json.user_id;
const sessionId = $input.item.json.session_id;
const message = $input.item.json.message;

// إذا لم يكن هناك user_id، استخدم session_id كمعرف مؤقت
const identifier = userId || sessionId;

return {
  user_id: userId,
  session_id: sessionId,
  message: message,
  identifier: identifier,
  is_authenticated: !!userId,
  timestamp: new Date().toISOString()
};
```

---

## 📊 تتبع نشاط المستخدم

### حفظ سجل المحادثات

```javascript
// Function Node: Log Conversation
const userId = $input.item.json.user_id;
const sessionId = $input.item.json.session_id;
const message = $input.item.json.message;
const response = $input.item.json.response;

// بيانات السجل
const logEntry = {
  user_id: userId,
  session_id: sessionId,
  user_message: message,
  bot_response: response,
  timestamp: new Date().toISOString(),
  intent: $input.item.json.intent,
  platform: $input.item.json.platform
};

// حفظ في قاعدة البيانات
// يمكن استخدام HTTP Request Node أو Database Node

return {
  logged: true,
  log_entry: logEntry
};
```

### تحليل نشاط المستخدم

```javascript
// Function Node: User Activity Analytics
const userId = $input.item.json.user_id;

// جلب سجل المستخدم من قاعدة البيانات
// (افترض أن البيانات موجودة)
const userActivity = {
  user_id: userId,
  total_messages: 150,
  most_used_intent: "create_post",
  preferred_platform: "twitter",
  active_hours: ["10:00-12:00", "18:00-20:00"],
  last_active: "2026-01-12T18:30:00Z"
};

return {
  user_id: userId,
  activity: userActivity,
  insights: [
    "المستخدم نشط في الصباح والمساء",
    "يفضل النشر على تويتر",
    "يستخدم ميزة النشر التلقائي بكثرة"
  ]
};
```

---

## 🔐 أمان وخصوصية

### أفضل الممارسات

1. **عدم تخزين بيانات حساسة**
   ```javascript
   // ❌ خطأ
   const password = $input.item.json.password;
   
   // ✅ صحيح
   const userId = $input.item.json.user_id;
   // استخدم user_id للوصول إلى البيانات من قاعدة البيانات
   ```

2. **التحقق من الصلاحيات**
   ```javascript
   const userId = $input.item.json.user_id;
   const requestedAccountId = $input.item.json.account_id;
   
   // تحقق أن الحساب يخص المستخدم
   if (account.user_id !== userId) {
     return {
       error: true,
       message: "ليس لديك صلاحية للوصول إلى هذا الحساب"
     };
   }
   ```

3. **تشفير البيانات الحساسة**
   ```javascript
   // عند حفظ بيانات اعتماد المنصات
   const encryptedCredentials = encrypt(credentials, userId);
   ```

---

## 🧪 الاختبار

### اختبار مع user_id

```bash
# اختبار webhook مع user_id
curl -X POST "http://localhost:5678/webhook/moj-ai-chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "أضف حساب تويتر",
    "user_id": 123,
    "session_id": "test_session_123",
    "timestamp": "2026-01-12T18:30:00.000Z",
    "source": "moj_ai_chatbot",
    "type": "user_message"
  }'
```

### اختبار بدون user_id (مستخدم غير مسجل)

```bash
curl -X POST "http://localhost:5678/webhook/moj-ai-chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "مرحباً",
    "user_id": null,
    "session_id": "guest_session_456",
    "timestamp": "2026-01-12T18:30:00.000Z",
    "source": "moj_ai_chatbot",
    "type": "user_message"
  }'
```

---

## 📝 ملاحظات مهمة

1. **user_id يمكن أن يكون null**
   - إذا كان المستخدم غير مسجل دخول
   - استخدم session_id كبديل للتتبع

2. **session_id دائماً موجود**
   - يتم إنشاؤه تلقائياً إذا لم يكن موجوداً
   - يُحفظ في localStorage في المتصفح

3. **التكامل مع Intent System**
   - يمكن استخدام user_id مع Intent Detection API
   - لتخصيص النوايا حسب المستخدم

---

## 🚀 الخطوات التالية

1. ✅ تم إضافة user_id إلى webhook payload
2. ✅ تم تحديث Frontend لإرسال user_id
3. ✅ Backend يرسل user_id إلى n8n
4. 📝 قم بتحديث n8n workflows لاستخدام user_id
5. 🔐 أضف التحقق من الصلاحيات في n8n
6. 📊 أضف تتبع نشاط المستخدم

---

**تم التحديث:** يناير 2026  
**الإصدار:** 1.0.0  
**الحالة:** ✅ جاهز للاستخدام
