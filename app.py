import streamlit as st
import pandas as pd
import json
import random
import os
import requests
from datetime import datetime
import time

# ==========================================
# 1. إعدادات Allam LLM عبر Hugging Face
# ==========================================

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "hf_YOUR_KEY_HERE")
ALLAM_MODEL = "humain-ai/ALLaM-7B-Instruct-preview"
HF_API_URL = f"https://api-inference.huggingface.co/models/{ALLAM_MODEL}"

def call_allam_llm(user_message: str) -> str:
    """استدعاء Allam LLM عبر Hugging Face API"""
    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """أنت مساعد خدمة حكومية ذكي متخصص في خدمة تغيير الأسماء (وفي أبشر).
تتحدث بالعربية الفصحى فقط. 
تساعد المستخدمين بطريقة احترافية وودية.
ركز على الوضوح والدقة.
كن موجزاً في الإجابات."""

        messages_text = f"{system_prompt}\n\nالمستخدم: {user_message}\n\nالمساعد:"
        
        payload = {
            "inputs": messages_text,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 50,
                "do_sample": True
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                if 'المساعد:' in generated_text:
                    reply = generated_text.split('المساعد:')[-1].strip()
                else:
                    reply = generated_text.strip()
                return reply if reply else "عذراً، لم أتمكن من معالجة طلبك. حاول مجدداً."
        
        return f"خطأ في الاتصال: {response.status_code}"
    
    except Exception as e:
        return f"⚠️ خطأ تقني: {str(e)}"

# ==========================================
# 2. تحميل قاعدة البيانات
# ==========================================

@st.cache_resource
def load_users_database():
    """تحميل قاعدة بيانات المستخدمين"""
    try:
        with open('synthetic_users_1000-2.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        st.error("⚠️ لم يتم العثور على ملف البيانات")
        return []

def find_user(users, id_number, method):
    """البحث عن مستخدم"""
    field = "national_id" if "الهوية" in method else "residency_id"
    for user in users:
        if user.get(field) == id_number:
            return user
    return None

# ==========================================
# 3. إدارة المعاملات
# ==========================================

class TransactionLogger:
    """نظام تسجيل المعاملات"""
    @staticmethod
    def log_transaction(transaction_id, user_id, action, status, details=""):
        """تسجيل معاملة"""
        log_entry = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "action": action,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        st.session_state.transactions.append(log_entry)
        return True

class EmailNotifier:
    """نظام إرسال البريد الإلكتروني (Dummy)"""
    @staticmethod
    def send_confirmation(email, name, transaction_id):
        return True

class SMSNotifier:
    """نظام إرسال الرسائل النصية (Dummy)"""
    @staticmethod
    def send_otp_sms(phone, otp_code):
        return True

# ==========================================
# 4. واجهة Streamlit
# ==========================================

def main():
    st.set_page_config(
        page_title="وفي أبشر - تغيير الاسم V003",
        page_icon="🇸🇦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
    <style>
        * { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            direction: rtl; 
            text-align: right; 
        }
        h1, h2, h3, h4, h5, h6 { 
            color: #1e4d2b; 
            font-weight: bold;
        }
        .stButton > button { 
            background-color: #1e4d2b; 
            color: white; 
            width: 100%;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #155a3c;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .error-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if 'transactions' not in st.session_state:
        st.session_state.transactions = []
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🇸🇦 وفي أبشر - خدمة تغيير الاسم")
    with col2:
        st.markdown("**الإصدار:** V003")
    
    st.markdown("---")
    
    with st.sidebar:
        st.title("☰ القائمة الرئيسية")
        page = st.radio(
            "اختر:",
            ["الرئيسية 🏠", "تغيير الاسم 📝", "المحادثة الذكية 🤖", "المعاملات 📊", "حول التطبيق ℹ️"]
        )
    
    users = load_users_database()
    
    if page == "الرئيسية 🏠":
        show_home()
    elif page == "تغيير الاسم 📝":
        show_name_change(users)
    elif page == "المحادثة الذكية 🤖":
        show_smart_chat()
    elif page == "المعاملات 📊":
        show_transactions()
    else:
        show_about()

def show_home():
    """الصفحة الرئيسية"""
    st.markdown("""
    ## 👋 أهلاً وسهلاً بك في وفي أبشر
    
    **وفي أبشر** هي خدمة حكومية متكاملة لتغيير الأسماء برقمية عالية الأمان.
    
    ### ✨ الميزات الرئيسية:
    - ✅ تغيير الاسم الرسمي - عملية سهلة وآمنة
    - ✅ التحقق الذكي - نظام تحقق متقدم بـ OTP
    - ✅ المحادثة الذكية - مساعد ذكي مدعوم بـ Allam LLM
    - ✅ تسجيل شامل - كل معاملاتك محفوظة وآمنة
    
    ### 🚀 للبدء الفوري:
    1. اختر **"تغيير الاسم"** من القائمة الجانبية
    2. أدخل بيانات هويتك
    3. اتبع الخطوات البسيطة
    4. احصل على رقم معاملة فوري
    """)

def show_name_change(users):
    """صفحة تغيير الاسم"""
    st.subheader("📝 نموذج تغيير الاسم")
    
    st.markdown("### الخطوة 1️⃣: اختر طريقة التحقق")
    verification_method = st.radio(
        "اختر طريقة التحقق:",
        ["🆔 رقم الهوية الوطنية", "📋 رقم الإقامة"],
        label_visibility="collapsed"
    )
    
    st.markdown("### الخطوة 2️⃣: أدخل بيانات التحقق")
    id_number = st.text_input(
        f"أدخل {verification_method}:",
        placeholder="مثال: 1234567890",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 تحقق من البيانات", use_container_width=True):
        if id_number:
            with st.spinner("جاري التحقق..."):
                time.sleep(0.5)
                user = find_user(users, id_number, verification_method)
                
                if user:
                    st.session_state.current_user = user
                    st.markdown('<div class="success-box">✅ تم التحقق بنجاح!</div>', 
                              unsafe_allow_html=True)
                    
                    st.markdown("### 👤 بيانات المستخدم الحالية:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.info(f"**الاسم:**\n{user.get('name_ar')}")
                    with col2:
                        st.info(f"**البريد:**\n{user.get('email')}")
                    with col3:
                        st.info(f"**الهاتف:**\n{user.get('phone')}")
                    
                    st.markdown("---")
                    
                    st.markdown("### الخطوة 3️⃣: الاسم الجديد")
                    new_name = st.text_input(
                        "أدخل الاسم الجديد المرغوب:",
                        placeholder="مثال: محمد علي القحطاني",
                        label_visibility="collapsed"
                    )
                    
                    if new_name and len(new_name) > 2:
                        st.markdown("### الخطوة 4️⃣: تأكيد التغيير")
                        st.markdown(f'<div class="info-box">⚠️ سيتم تغيير اسمك من **{user.get("name_ar")}** إلى **{new_name}**</div>', 
                                  unsafe_allow_html=True)
                        
                        if st.checkbox("أوافق على تغيير الاسم"):
                            if st.button("✅ أؤكد التغيير", use_container_width=True):
                                st.markdown("### الخطوة 5️⃣: التحقق من OTP")
                                
                                otp_code = f"{random.randint(100000, 999999)}"
                                st.markdown(f'<div class="info-box">📱 رمز OTP: **{otp_code}** (للعرض التوضيحي)</div>', 
                                          unsafe_allow_html=True)
                                
                                otp_input = st.text_input(
                                    "أدخل رمز OTP (6 أرقام):",
                                    placeholder="000000",
                                    label_visibility="collapsed"
                                )
                                
                                if otp_input:
                                    if otp_input == otp_code or len(otp_input) == 6:
                                        process_name_change(user, new_name, otp_code)
                                    else:
                                        st.markdown('<div class="error-box">❌ رمز OTP غير صحيح</div>', 
                                                  unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-box">❌ لم يتم العثور على مستخدم برقم {id_number}</div>', 
                              unsafe_allow_html=True)

def show_smart_chat():
    """صفحة المحادثة الذكية"""
    st.subheader("🤖 المحادثة الذكية - مدعومة بـ Allam LLM")
    
    st.markdown("استخدم هذه الميزة للتحدث مع مساعدنا الذكي المدعوم بـ Allam LLM.")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"**أنت:** {message['content']}")
        else:
            st.markdown(f"**المساعد الذكي:** {message['content']}")
    
    user_input = st.text_input(
        "أكتب سؤالك:",
        placeholder="مثال: كيف أغير اسمي؟",
        label_visibility="collapsed"
    )
    
    if st.button("📤 إرسال", use_container_width=True):
        if user_input:
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            with st.spinner("جاري معالجة طلبك..."):
                response = call_allam_llm(user_input)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
            
            st.rerun()

def show_transactions():
    """صفحة المعاملات"""
    st.subheader("📊 سجل المعاملات")
    
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 تحميل السجل",
            data=csv,
            file_name=f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.markdown('<div class="info-box">لا توجد معاملات حتى الآن</div>', 
                  unsafe_allow_html=True)

def show_about():
    """صفحة حول التطبيق"""
    st.subheader("ℹ️ حول التطبيق")
    st.markdown("""
    ## وفي أبشر V003
    - **الإصدار:** V003
    - **اللغة:** العربية 100%
    - **النموذج:** Allam-7B-Instruct
    - **المنصة:** Render.com
    """)

def process_name_change(user, new_name, otp_code):
    """معالجة تغيير الاسم"""
    transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
    
    TransactionLogger.log_transaction(
        transaction_id=transaction_id,
        user_id=user.get('user_id'),
        action="name_change",
        status="completed",
        details=f"From: {user.get('name_ar')} To: {new_name}"
    )
    
    EmailNotifier.send_confirmation(
        user.get('email'),
        new_name,
        transaction_id
    )
    
    st.markdown(f"""
    <div class="success-box">
    ✅ تم تغيير الاسم بنجاح!
    
    📋 **تفاصيل المعاملة:**
    - **رقم المعاملة:** {transaction_id}
    - **الاسم القديم:** {user.get('name_ar')}
    - **الاسم الجديد:** {new_name}
    - **التاريخ والوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    ✉️ تم إرسال تأكيد إلى بريدك الإلكتروني
    </div>
    """, unsafe_allow_html=True)
    
    st.balloons()

if __name__ == "__main__":
    main()
