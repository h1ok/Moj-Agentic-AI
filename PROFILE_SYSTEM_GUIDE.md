# دليل نظام البروفايل - Profile System Guide

## نظرة عامة
تم إضافة نظام بروفايل كامل للمستخدمين يتضمن:
- صفحة بروفايل لتعديل المعلومات الشخصية
- تغيير كلمة المرور
- رفع وتحديث الصورة الشخصية
- قائمة إعدادات منسدلة تظهر عند الضغط على اسم المستخدم

## التغييرات في قاعدة البيانات

### 1. تحديث جدول المستخدمين
تم إضافة حقلين جديدين لجدول `users`:
- `name` (String 255) - اسم المستخدم
- `profile_picture` (String 500) - رابط أو base64 للصورة الشخصية

### 2. تشغيل Migration
لتطبيق التغييرات على قاعدة البيانات:

```bash
# من مجلد المشروع الرئيسي
python -m alembic upgrade head
```

أو يمكنك تشغيل SQL مباشرة:
```sql
ALTER TABLE users ADD COLUMN name VARCHAR(255);
ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500);
```

## API Endpoints الجديدة

### 1. الحصول على معلومات المستخدم الحالي
```
GET /api/auth/me
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "اسم المستخدم",
  "profile_picture": "base64_or_url",
  "created_at": "2026-01-20T12:00:00"
}
```

### 2. تحديث البروفايل
```
PUT /api/auth/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "الاسم الجديد",
  "email": "newemail@example.com"
}
```

### 3. تغيير كلمة المرور
```
POST /api/auth/change-password
Authorization: Bearer {token}
Content-Type: application/json

{
  "current_password": "كلمة المرور الحالية",
  "new_password": "كلمة المرور الجديدة"
}
```

### 4. رفع صورة البروفايل
```
POST /api/auth/profile-picture
Authorization: Bearer {token}
Content-Type: application/json

{
  "profile_picture": "base64_encoded_image_or_url"
}
```

## المكونات الأمامية (Frontend)

### 1. صفحة البروفايل
**المسار:** `/profile`
**الملف:** `frontend/src/pages/Profile.jsx`

**المميزات:**
- عرض وتحديث الصورة الشخصية
- تعديل الاسم والبريد الإلكتروني
- تغيير كلمة المرور
- رسائل نجاح/خطأ تفاعلية
- دعم الوضع الليلي

### 2. قائمة الإعدادات في Sidebar
**الملف:** `frontend/src/components/Sidebar.jsx`

**التحديثات:**
- قائمة منسدلة تظهر عند الضغط على اسم المستخدم
- عرض الصورة الشخصية في الـ Avatar
- خيارات: إعدادات الحساب، البروفايل
- أيقونة سهم للإشارة إلى القائمة

### 3. تحديثات App.jsx
- إضافة route جديد: `/profile`
- حماية الصفحة بـ authentication
- تمرير `user` و `setUser` للصفحة

## كيفية الاستخدام

### للمستخدم النهائي:
1. سجل الدخول إلى النظام
2. اضغط على اسمك في الـ Sidebar (أسفل اليسار)
3. اختر "إعدادات الحساب" أو "البروفايل"
4. قم بتحديث معلوماتك:
   - اضغط على أيقونة الكاميرا لتغيير الصورة
   - عدل الاسم والبريد الإلكتروني
   - غير كلمة المرور من القسم المخصص
5. اضغط "حفظ التغييرات"

### للمطور:
1. تأكد من تشغيل الـ migration
2. شغل الـ Backend:
   ```bash
   python run.py
   ```
3. شغل الـ Frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## الأمان
- جميع endpoints محمية بـ JWT authentication
- التحقق من كلمة المرور الحالية قبل تغييرها
- التحقق من عدم تكرار البريد الإلكتروني
- حد أقصى لحجم الصورة: 5 ميجابايت

## الملفات المعدلة

### Backend:
- `app/db/models.py` - إضافة حقول name و profile_picture
- `app/auth/routes.py` - إضافة endpoints جديدة
- `alembic/versions/add_user_profile_fields.py` - migration جديد

### Frontend:
- `frontend/src/pages/Profile.jsx` - صفحة البروفايل (جديد)
- `frontend/src/components/Sidebar.jsx` - قائمة الإعدادات المنسدلة
- `frontend/src/App.jsx` - route البروفايل
- `frontend/src/pages/Login.jsx` - جلب بيانات المستخدم الكاملة
- `frontend/src/pages/Register.jsx` - حفظ الاسم عند التسجيل

## ملاحظات
- الصورة الشخصية يمكن أن تكون base64 أو URL
- الاسم اختياري، إذا لم يتم تعيينه يظهر البريد الإلكتروني
- جميع التحديثات تحفظ في localStorage و state
- الواجهة متجاوبة وتدعم الوضع الليلي
