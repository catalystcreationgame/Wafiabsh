1: app.py ✅

الكود الكامل للتطبيق

550+ سطر

متكامل مع Allam LLM

الرابط: artifact_id: 198

الملف 2: requirements.txt ✅

text
streamlit==1.51.0
pandas==2.2.2
numpy==2.0.2
requests==2.31.0
python-dotenv==1.0.0
الرابط: artifact_id: 183

الملف 3: .env ✅

text
HUGGINGFACE_API_KEY=hf_YOUR_ACTUAL_API_KEY_HERE
الرابط: artifact_id: 199

⚠️ استبدل hf_YOUR_ACTUAL_API_KEY_HERE برقمك الحقيقي

الملف 4: .gitignore ✅

text
.env
__pycache__/
*.pyc
.streamlit/
.DS_Store
*.egg-info/
dist/
build/
الرابط: artifact_id: 200

📥 كيفية التحميل:
اذهب إلى كل ملف أعلاه (artifact_id)

اضغط على "Download" أو "Save"

احفظ في مجلد واحد باسم: wafi-absher-v003

📂 هيكل المجلد النهائي:
text
wafi-absher-v003/
├── app.py                         (550+ سطر)
├── requirements.txt               (5 مكتبات)
├── .env                          (1 مفتاح)
├── .gitignore                    (7 ملفات إخفاء)
└── synthetic_users_1000-2.json   (من البيانات القديمة)
🚀 خطوات النشر - بدون Git (مباشرة في GitHub):
الخطوة 1: حضّر المجلد

text
انسخ الملفات الأربعة في مجلد واحد
الخطوة 2: أضف البيانات

text
احفظ synthetic_users_1000-2.json (من البيانات القديمة)
في نفس المجلد
الخطوة 3: حدّث .env

text
استبدل: hf_YOUR_ACTUAL_API_KEY_HERE
بـ: مفتاحك الفعلي من Hugging Face
الخطوة 4: إنشاء Repository على GitHub (بدون Git)

اذهب: https://github.com/new

الاسم: wafiabsh

الوصف: Wafi Absher with Allam LLM

اختر: Public

اضغط: Create repository

الخطوة 5: رفع الملفات (مباشرة في GitHub)

بعد إنشاء Repository:

اضغط على زر: Add files (أعلى اليمين)

اختر: Upload files

اختر الملفات الخمسة:

app.py

requirements.txt

.env

.gitignore

synthetic_users_1000-2.json

اضغط: Commit changes

الخطوة 6: على Render

اذهب: https://render.com

Sign Up with GitHub (أو Sign In)

اضغط: New +

اختر: Web Service

اضغط: Connect account

اختر Repository: wafi-absher-v003

اضغط: Connect

الخطوة 7: الإعدادات

في الصفحة التالية، املأ:

text
Name: wafi-absher-v003
Runtime: Python 3.11
Region: (اختر الأقرب)
Branch: main
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port=10000 --server.headless=true --server.enableCORS=false
اضغط: Create Web Service

الخطوة 8: API Key

في Render Dashboard، اختر: Environment

اضغط: Add Environment Variable

أضف:

text
Key: HUGGINGFACE_API_KEY
Value: hf_YOUR_ACTUAL_KEY_HERE
اضغط: Save Changes

الخطوة 9: Deploy

text
اضغط: Redeploy
انتظر 5-10 دقائق
الرابط سيظهر: https://wafi-absher-v003.onrender.com
⏱️ وقت الانتظار:
text
البناء: 5-10 دقائق
التحميل الأول: 30-60 ثانية
بعدها سريع جداً ⚡
✅ علامات النجاح:
text
✅ في Render Dashboard:
   "Your service is live" = نجح ✓
   
✅ الرابط في الأعلى:
   https://wafi-absher-v003.onrender.com = اضغط عليه ✓
   
✅ الصفحة تفتح:
   الواجهة العربية ظاهرة = نجح ✓
🔧 لو حصل خطأ:
خطأ: "Build failed"

الحل:

اذهب: Render Dashboard

اختر: Logs

اقرأ الخطأ

غالباً: ملف غير موجود أو اسم خاطئ

خطأ: "API Key invalid"

الحل:

تأكد من المفتاح صحيح

اذهب: https://huggingface.co/settings/tokens

انسخ المفتاح الجديد

اذهب: Render → Environment → Edit

اضغط: Redeploy

الموقع بطيء جداً

الحل:

أول مرة تحميل يأخذ وقت (60 ثانية تقريباً)

بعدها سريع

لو استمر: Render Plan الحالي ضعيف → اشترك بـ Paid
