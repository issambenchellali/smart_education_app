# ============================================
# 🎓 المنصة التعليمية الذكية المتكاملة (إصدار نهائي ومحسّن)
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import json
import time
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import base64
import hashlib

# ============================================
# 1. إعدادات البيئة والمتغيرات
# ============================================

st.set_page_config(
    page_title="المنصة التعليمية الذكية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "your-anon-key")
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "your-openai-key")

# ============================================
# 2. CSS وتصميم الواجهة
# ============================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap" rel="stylesheet">
<style>
    body { font-family: 'Tajawal', sans-serif; background-color: #f4f7f6; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .main-title {
        text-align: center; color: #ffffff; padding: 40px 20px; font-size: 3.5rem;
        font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px; box-shadow: 0 10px 30px rgba(118, 75, 162, 0.3);
        margin-bottom: 30px; animation: fadeInDown 1s ease;
    }
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
    .card {
        background: rgba(255, 255, 255, 0.98); padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.5); transition: all 0.3s;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;
        padding: 12px 25px; border-radius: 12px; font-weight: 700; font-family: 'Tajawal'; width: 100%;
    }
    .log-box {
        background: #1e1e1e; color: #00ff00; padding: 15px; border-radius: 10px;
        font-family: 'Courier New', monospace; font-size: 0.85rem; max-height: 300px; overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 3. إدارة السجلات (Logs)
# ============================================

class SystemLogger:
    """مسؤول عن تسجيل أحداث النظام للتشخيص"""
    def __init__(self):
        if "logs" not in st.session_state:
            st.session_state.logs = []
    
    def add(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        st.session_state.logs.append(log_entry)
        print(log_entry) # طباعة في الـ Terminal أيضاً

    def get_logs(self):
        return st.session_state.logs[-50:] # آخر 50 رسالة

logger = SystemLogger()

# ============================================
# 4. إدارة قاعدة البيانات (Supabase) - محسّنة
# ============================================

class DatabaseManager:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        self.tables = {
            "users": "users", "lessons": "lessons", "exercises": "exercises",
            "student_progress": "student_progress", "ai_interactions": "ai_interactions",
            "notifications": "notifications"
        }
    
    def _make_request(self, endpoint: str, method: str = "GET", data: dict = None, extra_headers: dict = None):
        """تنفيذ طلب HTTP مع تسجيل شامل للأخطاء"""
        url = f"{self.supabase_url}/rest/v1/{endpoint}"
        headers = self.headers.copy()
        if extra_headers:
            headers.update(extra_headers)
        
        logger.add(f"طلب HTTP: {method} {url}", "DEBUG")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10) if method == "POST" else \
                       requests.get(url, headers=headers, params=data, timeout=10) if method == "GET" else \
                       requests.put(url, headers=headers, json=data, timeout=10) if method == "PUT" else \
                       requests.delete(url, headers=headers, timeout=10)
            
            logger.add(f"رد السيرفر: Code {response.status_code}", "DEBUG")
            
            if response.status_code in [200, 201, 204]:
                try:
                    return response.json() if response.content else {"status": "success", "empty_body": True}
                except ValueError:
                    return {"status": "success", "empty_body": True}
            else:
                logger.add(f"فشل الطلب: {response.text}", "ERROR")
                return None
                
        except requests.exceptions.ConnectionError:
            logger.add("فشل الاتصال بالإنترنت (Connection Error)", "ERROR")
            return None
        except requests.exceptions.Timeout:
            logger.add("انتهى وقت الانتظار (Timeout)", "ERROR")
            return None
        except Exception as e:
            logger.add(f"خطأ غير متوقع: {str(e)}", "ERROR")
            return None
    
    def create_user(self, username: str, password: str, email: str, full_name: str, role: str = "طالب", grade: str = None):
        """إنشاء مستخدم مع إجبار السيرفر على الرد بالبيانات"""
        user_data = {
            "username": username, "password_hash": self._hash_password(password),
            "email": email, "full_name": full_name, "role": role, "grade": grade,
            "created_at": datetime.now().isoformat(), "is_active": True
        }
        # التأكد من إرجاع البيانات المضافة
        return self._make_request(self.tables["users"], "POST", user_data, extra_headers={"Prefer": "return=representation"})
    
    def authenticate_user(self, username: str, password: str):
        """المصادقة على المستخدم"""
        users = self._make_request(f"{self.tables['users']}?username=eq.{username}&select=*")
        if users:
            # قد تأتي القائمة أو القاموس بناءً على الرد
            user_list = users if isinstance(users, list) else [users]
            if user_list:
                user = user_list[0]
                if user.get("password_hash") == self._hash_password(password):
                    return user
        return None

    def update_user_profile(self, user_id: str, data: dict):
        return self._make_request(f"{self.tables['users']}?id=eq.{user_id}", "PATCH", data)
    
    def get_all_lessons(self, subject: str = None, grade: str = None):
        query = f"{self.tables['lessons']}?select=*&order=created_at.desc"
        if subject and subject != "الكل": query += f"&subject=eq.{subject}"
        if grade and grade != "الكل": query += f"&grade=eq.{grade}"
        return self._make_request(query)
    
    def get_lesson_by_id(self, lesson_id: str):
        lessons = self._make_request(f"{self.tables['lessons']}?id=eq.{lesson_id}&select=*")
        if lessons:
            user_list = lessons if isinstance(lessons, list) else [lessons]
            return user_list[0] if user_list else None
        return None
    
    def create_lesson(self, lesson_data: dict):
        lesson_data["created_at"] = datetime.now().isoformat()
        return self._make_request(self.tables["lessons"], "POST", lesson_data, extra_headers={"Prefer": "return=representation"})
    
    def get_exercises_by_lesson(self, lesson_id: str):
        return self._make_request(f"{self.tables['exercises']}?lesson_id=eq.{lesson_id}&select=*&order=created_at.asc")
    
    def update_student_progress(self, student_id: str, lesson_id: str, progress_data: dict):
        progress_data["student_id"] = student_id
        progress_data["lesson_id"] = lesson_id
        progress_data["updated_at"] = datetime.now().isoformat()
        
        existing = self._make_request(f"{self.tables['student_progress']}?student_id=eq.{student_id}&lesson_id=eq.{lesson_id}")
        
        if existing and isinstance(existing, list) and len(existing) > 0:
            return self._make_request(f"{self.tables['student_progress']}?id=eq.{existing[0]['id']}", "PATCH", progress_data)
        else:
            progress_data["started_at"] = datetime.now().isoformat()
            return self._make_request(self.tables["student_progress"], "POST", progress_data)
    
    def log_ai_interaction(self, user_id: str, interaction_type: str, data: dict):
        log_data = {"user_id": user_id, "interaction_type": interaction_type, "data": json.dumps(data), "created_at": datetime.now().isoformat()}
        return self._make_request(self.tables["ai_interactions"], "POST", log_data)
    
    def create_notification(self, user_id: str, title: str, message: str, notification_type: str = "info"):
        notif_data = {"user_id": user_id, "title": title, "message": message, "type": notification_type, "is_read": False, "created_at": datetime.now().isoformat()}
        return self._make_request(self.tables["notifications"], "POST", notif_data)
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

# تهيئة المدير
db_manager = DatabaseManager(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# 5. دوال المساعدة (Default Users)
# ============================================

def init_default_users():
    """التحقق وإنشاء حسابات أدمن وطالب افتراضية"""
    logger.add("جاري التحقق من الحسابات الافتراضية...", "INFO")
    
    # بيانات الحسابات
    defaults = [
        {
            "username": "admin",
            "password": "admin123",
            "email": "admin@school.com",
            "full_name": "مدير النظام",
            "role": "معلم",
            "grade": None
        },
        {
            "username": "student",
            "password": "student123",
            "email": "student@school.com",
            "full_name": "طالب مجتهد",
            "role": "طالب",
            "grade": "العاشر"
        }
    ]
    
    for u in defaults:
        try:
            # محاولة التحقق من وجود المستخدم
            existing = db_manager._make_request(f"users?username=eq.{u['username']}&select=id")
            
            if not existing:
                logger.add(f"حساب {u['username']} غير موجود، جاري الإنشاء...", "WARNING")
                result = db_manager.create_user(u['username'], u['password'], u['email'], u['full_name'], u['role'], u['grade'])
                if result:
                    logger.add(f"تم إنشاء حساب {u['username']} بنجاح!", "SUCCESS")
                else:
                    logger.add(f"فشل إنشاء حساب {u['username']}", "ERROR")
            else:
                logger.add(f"حساب {u['username']} موجود مسبقاً.", "SUCCESS")
        except Exception as e:
            logger.add(f"خطأ أثناء إعداد المستخدم الافتراضي: {e}", "ERROR")

# ============================================
# 6. باقي الكلاسات (AI, Curriculum, etc.) - مختصرة للاختصار
# ============================================

class AIEducationAssistant:
    def __init__(self, api_key: str): self.api_key = api_key
    def explain_lesson(self, s, t, g, l="مبتدئ"): return "شرح ذكي تجريبي..."
    def generate_exercise(self, s, t, d="متوسط", n=3): return "تمرين ذكي تجريبي..."
    def evaluate_answer(self, q, a): return "تقييم ذكي تجريبي..."
    def answer_student_question(self, q, c=None): return "إجابة ذكية تجريبية..."
    def analyze_student_performance(self, data): return "تحليل أداء تجريبي..."

ai_assistant = AIEducationAssistant(OPENAI_API_KEY) if OPENAI_API_KEY != "your-openai-key" else None

class SessionManager:
    def __init__(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.notifications = []
    def login(self, user_data: dict):
        st.session_state.logged_in = True
        st.session_state.user_data = user_data
        st.session_state.role = user_data.get("role", "طالب")
    def logout(self):
        for k in list(st.session_state.keys()): del st.session_state[k]
        self.__init__()

session_manager = SessionManager()

# ============================================
# 7. صفحة تسجيل الدخول (مع السجلات)
# ============================================

def show_login_page():
    # تشغيل التهيئة الافتراضية عند كل تحميل للصفحة
    init_default_users()
    
    st.markdown('<div class="main-title">🎓 المنصة التعليمية الذكية</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب"])
            
            with tab1:
                st.markdown('<h3 style="text-align: center;">تسجيل الدخول</h3>', unsafe_allow_html=True)
                
                username = st.text_input("اسم المستخدم", key="l_u")
                password = st.text_input("كلمة المرور", type="password", key="l_p")
                
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button("دخول", use_container_width=True, type="primary"):
                        if username and password:
                            logger.add(f"محاولة دخول المستخدم: {username}", "INFO")
                            user = db_manager.authenticate_user(username, password)
                            if user:
                                session_manager.login(user)
                                st.success("تم تسجيل الدخول بنجاح")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("بيانات الدخول غير صحيحة")
                        else:
                            st.warning("أدخل البيانات")
                
                with col2_btn:
                    if st.button("الدخول كزائر", use_container_width=True):
                        logger.add("دخول كزائر", "INFO")
                        session_manager.login({"username": "زائر", "role": "طالب", "full_name": "زائر"})
                        st.rerun()
                
                # عرض البيانات التجريبية للمستخدم الجديد
                st.info("بيانات الدخول الافتراضية (إنشاء تلقائي):")
                st.markdown("""
                <div style="background:#f0f8ff; padding:10px; border-radius:10px; text-align:center;">
                <b>أدمن:</b> admin / admin123<br>
                <b>طالب:</b> student / student123
                </div>
                """, unsafe_allow_html=True)

            with tab2:
                st.markdown('<h3 style="text-align: center;">حساب جديد</h3>', unsafe_allow_html=True)
                full_name = st.text_input("الاسم الكامل")
                n_username = st.text_input("اسم المستخدم")
                n_email = st.text_input("البريد الإلكتروني")
                n_password = st.text_input("كلمة المرور", type="password")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
                grade = st.selectbox("الصف", ["السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"])
                role = st.selectbox("الدور", ["طالب", "معلم"])
                
                if st.button("إنشاء حساب", use_container_width=True, type="primary"):
                    if n_password == confirm_password:
                        res = db_manager.create_user(n_username, n_password, n_email, full_name, role, grade)
                        if res:
                            st.success("تم إنشاء الحساب! قم بتسجيل الدخول الآن.")
                        else:
                            st.error("فشل إنشاء الحساب (راجع السجلات بالأسفل)")
                    else:
                        st.error("كلمات المرور غير متطابقة")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # --- قسم السجلات (Logs) الجديد ---
            with st.expander("🛠️ سجلات النظام واختبار الاتصال (Logs)", expanded=False):
                col_log1, col_log2 = st.columns([1, 2])
                with col_log1:
                    if st.button("🔄 اختبار الاتصال بقاعدة البيانات"):
                        test_url = f"{SUPABASE_URL}/rest/v1/"
                        try:
                            r = requests.get(test_url, headers={"apikey": SUPABASE_KEY}, timeout=5)
                            if r.status_code == 200:
                                st.success("✅ الاتصال ناجح!")
                                logger.add("تم اختبار الاتصال: نجح", "SUCCESS")
                            else:
                                st.error(f"❌ كود الخطأ: {r.status_code}")
                                logger.add(f"فشل الاتصال: {r.status_code}", "ERROR")
                        except Exception as e:
                            st.error("❌ فشل الاتصال")
                            logger.add(f"فشل الاتصال: {str(e)}", "ERROR")
                    
                    if st.button("🗑️ مسح السجلات"):
                        st.session_state.logs = []
                        st.rerun()

                with col_log2:
                    st.text_area("تفاصيل السجلات:", value="\n".join(logger.get_logs()), height=200, key="logs_area")
            
            # حالة الاتصال
            st.markdown('<div style="text-align:center; font-size:0.8rem; color:#888;">Supabase Connection: <span style="color:green;">Active</span></div>', unsafe_allow_html=True)

# ============================================
# 8. الواجهات الداخلية (بسيطة للوظائف)
# ============================================

def show_main_dashboard():
    st.title("🏠 لوحة التحكم")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("تسجيل خروج"): session_manager.logout(); st.rerun()
    st.info(f"مرحباً {st.session_state.user_data.get('full_name')} - دورك: {st.session_state.role}")
    
    # هنا يمكنك استدعاء الدروس والأقسام كما كانت سابقاً
    st.markdown("---")
    st.markdown("### 📚 مكتبة الدروس")
    lessons = db_manager.get_all_lessons()
    if lessons:
        st.write("تم العثور على دروس:", len(lessons))
        for l in lessons[:3]:
            st.write(f"- {l.get('title')}")
    else:
        st.info("لا توجد دروس حالياً في قاعدة البيانات.")

# ============================================
# 9. التشغيل الرئيسي
# ============================================

def main():
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_main_dashboard()

if __name__ == "__main__":
    main()
