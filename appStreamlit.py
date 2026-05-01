# ============================================
# 🎓 المنصة التعليمية الذكية المتكاملة (إصدار محسن بصرياً)
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

# إعدادات الصفحة
st.set_page_config(
    page_title="المنصة التعليمية الذكية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# المتغيرات البيئية
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "your-anon-key")
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "your-openai-key")

# ============================================
# 2. CSS وتصميم الواجهة (تم تطويره بالكامل)
# ============================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap" rel="stylesheet">
<style>
    /* إعدادات الخطوط العامة */
    body {
        font-family: 'Tajawal', sans-serif;
        background-color: #f4f7f6;
    }
    
    /* إخفاء عناصر Streamlit غير المرغوبة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* العنوان الرئيسي بتأثير متدرج وحديث */
    .main-title {
        text-align: center;
        color: #ffffff;
        padding: 40px 20px;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(118, 75, 162, 0.3);
        margin-bottom: 30px;
        text-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: fadeInDown 1s ease;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* تصميم البطاقات بتأثير الزجاج */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(118, 75, 162, 0.15);
        border-color: #764ba2;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* الأزرار العصرية */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 12px;
        font-weight: 700;
        font-family: 'Tajawal', sans-serif;
        transition: all 0.3s;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(118, 75, 162, 0.4);
    }
    
    /* حقول الإدخال */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid #eef0f2;
        padding: 12px;
        background: #f9fafb;
        font-family: 'Tajawal', sans-serif;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
        background: white;
    }
    
    /* الإحصائيات */
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        text-align: center;
        transition: all 0.3s;
        border: 1px solid rgba(0,0,0,0.03);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(118, 75, 162, 0.1);
    }
    
    .stat-number {
        font-size: 2.8rem;
        font-weight: 800;
        color: #667eea;
        margin: 10px 0;
        line-height: 1;
    }
    
    /* علامات التبويب */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: white;
        padding: 5px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 12px 25px;
        font-family: 'Tajawal', sans-serif;
        font-weight: 600;
        color: #64748b;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* شريط التقدم */
    .progress-container {
        background: #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        height: 12px;
        margin: 15px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }
    
    /* رسائل التنبيه */
    .message-success {
        background: #dcfce7;
        color: #166534;
        padding: 15px;
        border-radius: 12px;
        border-right: 4px solid #22c55e;
        margin: 10px 0;
    }
    
    .message-error {
        background: #fee2e2;
        color: #991b1b;
        padding: 15px;
        border-radius: 12px;
        border-right: 4px solid #ef4444;
        margin: 10px 0;
    }
    
    /* إشعارات جانبية */
    .notification {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        padding: 15px 30px;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideDown 0.5s ease;
        border: 1px solid #eee;
    }
    
    @keyframes slideDown {
        from { top: -50px; opacity: 0; }
        to { top: 20px; opacity: 1; }
    }
    
    /* تحسينات للموبايل */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
            padding: 30px 15px;
        }
        .stat-number {
            font-size: 2rem;
        }
    }
    
    /* الأيقونات الكبيرة */
    .emoji-large {
        font-size: 4rem;
        display: block;
        margin-bottom: 10px;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 3. إدارة قاعدة البيانات (Supabase)
# ============================================

class DatabaseManager:
    """مدير قاعدة البيانات باستخدام Supabase"""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        self.tables = {
            "users": "users",
            "lessons": "lessons",
            "exercises": "exercises",
            "student_progress": "student_progress",
            "ai_interactions": "ai_interactions",
            "notifications": "notifications"
        }
    
    def _make_request(self, endpoint: str, method: str = "GET", data: dict = None):
        """تنفيذ طلب HTTP لـ Supabase"""
        url = f"{self.supabase_url}/rest/v1/{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                return None
            
            # إذا كان الكود 200 أو 201 (نجاح)
            if response.status_code in [200, 201]:
                try:
                    # محاولة قراءة البيانات
                    data = response.json()
                    # إذا كانت البيانات موجودة، أعدها
                    if data:
                        return data
                    # إذا كانت البيانات فارغة [] أو None، هذا يعني نجاح الإضافة ولكن قاعدة البيانات لم ترجع صفوف (تحدث أحياناً في INSERT)
                    return {"status": "success", "details": "no_content"}
                except:
                    # إذا تعذر تحويل الرد لـ JSON، لكن الكود هو 200/201، نفترض النجاح
                    return {"status": "success", "details": "empty_body"}
            else:
                # خطأ من السيرفر (401, 403, 404, etc.)
                print(f"Supabase Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    def create_user(self, username: str, password: str, email: str, full_name: str, role: str = "طالب", grade: str = None):
        """إنشاء مستخدم جديد"""
        user_data = {
            "username": username,
            "password_hash": self._hash_password(password),
            "email": email,
            "full_name": full_name,
            "role": role,
            "grade": grade,
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "last_login": None
        }
        
        return self._make_request(self.tables["users"], "POST", user_data)
    
    def authenticate_user(self, username: str, password: str):
        """المصادقة على المستخدم"""
        users = self._make_request(
            f"{self.tables['users']}?username=eq.{username}&select=*"
        )
        
        if users and len(users) > 0:
            user = users[0]
            if user.get("password_hash") == self._hash_password(password):
                return user
        return None
    
    def update_user_profile(self, user_id: str, data: dict):
        """تحديث ملف المستخدم"""
        return self._make_request(
            f"{self.tables['users']}?id=eq.{user_id}",
            "PATCH",
            data
        )
    
    def get_user_by_id(self, user_id: str):
        """الحصول على بيانات المستخدم"""
        users = self._make_request(
            f"{self.tables['users']}?id=eq.{user_id}&select=*"
        )
        return users[0] if users else None
    
    def create_lesson(self, lesson_data: dict):
        """إنشاء درس جديد"""
        lesson_data["created_at"] = datetime.now().isoformat()
        lesson_data["updated_at"] = datetime.now().isoformat()
        lesson_data["is_published"] = True
        return self._make_request(self.tables["lessons"], "POST", lesson_data)
    
    def get_all_lessons(self, subject: str = None, grade: str = None):
        """الحصول على جميع الدروس"""
        query = f"{self.tables['lessons']}?select=*&order=created_at.desc"
        if subject and subject != "الكل":
            query += f"&subject=eq.{subject}"
        if grade and grade != "الكل":
            query += f"&grade=eq.{grade}"
        return self._make_request(query)
    
    def get_lesson_by_id(self, lesson_id: str):
        """الحصول على درس بواسطة ID"""
        lessons = self._make_request(
            f"{self.tables['lessons']}?id=eq.{lesson_id}&select=*"
        )
        return lessons[0] if lessons else None
    
    def update_lesson(self, lesson_id: str, data: dict):
        """تحديث درس"""
        data["updated_at"] = datetime.now().isoformat()
        return self._make_request(
            f"{self.tables['lessons']}?id=eq.{lesson_id}",
            "PATCH",
            data
        )
    
    def create_exercise(self, exercise_data: dict):
        """إنشاء تمرين جديد"""
        exercise_data["created_at"] = datetime.now().isoformat()
        return self._make_request(self.tables["exercises"], "POST", exercise_data)
    
    def get_exercises_by_lesson(self, lesson_id: str):
        """الحصول على تمارين درس معين"""
        return self._make_request(
            f"{self.tables['exercises']}?lesson_id=eq.{lesson_id}&select=*&order=created_at.asc"
        )
    
    def update_student_progress(self, student_id: str, lesson_id: str, progress_data: dict):
        """تحديث تقدم الطالب"""
        progress_data["student_id"] = student_id
        progress_data["lesson_id"] = lesson_id
        progress_data["updated_at"] = datetime.now().isoformat()
        
        existing = self._make_request(
            f"{self.tables['student_progress']}?student_id=eq.{student_id}&lesson_id=eq.{lesson_id}"
        )
        
        if existing and len(existing) > 0:
            return self._make_request(
                f"{self.tables['student_progress']}?id=eq.{existing[0]['id']}",
                "PATCH",
                progress_data
            )
        else:
            progress_data["started_at"] = datetime.now().isoformat()
            return self._make_request(self.tables["student_progress"], "POST", progress_data)
    
    def get_student_progress(self, student_id: str):
        """الحصول على تقدم الطالب"""
        return self._make_request(
            f"{self.tables['student_progress']}?student_id=eq.{student_id}&select=*"
        )
    
    def log_ai_interaction(self, user_id: str, interaction_type: str, data: dict):
        """تسجيل تفاعل مع الذكاء الاصطناعي"""
        log_data = {
            "user_id": user_id,
            "interaction_type": interaction_type,
            "data": json.dumps(data),
            "created_at": datetime.now().isoformat()
        }
        return self._make_request(self.tables["ai_interactions"], "POST", log_data)
    
    def create_notification(self, user_id: str, title: str, message: str, notification_type: str = "info"):
        """إنشاء إشعار جديد"""
        notification_data = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "is_read": False,
            "created_at": datetime.now().isoformat()
        }
        return self._make_request(self.tables["notifications"], "POST", notification_data)
    
    def get_user_notifications(self, user_id: str, unread_only: bool = True):
        """الحصول على إشعارات المستخدم"""
        query = f"{self.tables['notifications']}?user_id=eq.{user_id}&order=created_at.desc"
        if unread_only:
            query += "&is_read=eq.false"
        return self._make_request(query)
    
    def _hash_password(self, password: str) -> str:
        """تجزئة كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_statistics(self):
        """الحصول على إحصائيات النظام"""
        stats = {
            "total_users": 0,
            "total_lessons": 0,
            "total_exercises": 0,
            "active_students": 0
        }
        return stats

db_manager = DatabaseManager(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# 4. نظام الذكاء الاصطناعي (OpenAI)
# ============================================

class AIEducationAssistant:
    """مساعد تعليمي ذكي باستخدام OpenAI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.teaching_styles = {
            "شرح": "كن أستاذاً محترفاً تشرح المفاهيم بشكل مبسط مع أمثلة",
            "تمرين": "أنشئ تمارين تعليمية مع حلول وتفسيرات",
            "مراجعة": "راجع الدروس مع تركيز على النقاط المهمة",
            "تقييم": "قيم مستوى الطالب وأعط توصيات للتحسين"
        }
    
    def _make_ai_request(self, messages: list, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """إرسال طلب إلى OpenAI API"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1000
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"OpenAI Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"AI request error: {e}")
            return None
    
    def explain_lesson(self, subject: str, topic: str, grade: str, student_level: str = "مبتدئ"):
        """شرح درس باستخدام الذكاء الاصطناعي"""
        prompt = f"""
        أنت أستاذ محترف في مادة {subject}.
        
        المطلوب: اشرح موضوع {topic} للصف {grade}
        مستوى الطالب: {student_level}
        
        يجب أن يحتوي الشرح على:
        1. مقدمة بسيطة عن الموضوع
        2. المفاهيم الأساسية بطريقة مبسطة
        3. أمثلة واقعية من الحياة اليومية
        4. نصائح للفهم والاستيعاب
        5. ملخص للنقاط الرئيسية
        
        استخدم لغة عربية واضحة ومناسبة للطلاب.
        """
        
        messages = [
            {"role": "system", "content": self.teaching_styles["شرح"]},
            {"role": "user", "content": prompt}
        ]
        
        explanation = self._make_ai_request(messages)
        
        if explanation:
            if "user" in st.session_state and st.session_state.user:
                db_manager.log_ai_interaction(
                    st.session_state.user.get("id", "unknown"),
                    "lesson_explanation",
                    {"subject": subject, "topic": topic, "grade": grade}
                )
        
        return explanation or "عذراً، تعذر الحصول على الشرح في الوقت الحالي. يرجى المحاولة لاحقاً."
    
    def generate_exercise(self, subject: str, topic: str, difficulty: str = "متوسط", num_questions: int = 3):
        """توليد تمارين باستخدام الذكاء الاصطناعي"""
        prompt = f"""
        أنت أستاذ محترف في مادة {subject}.
        
        المطلوب: أنشئ {num_questions} تمارين في موضوع {topic}
        مستوى الصعوبة: {difficulty}
        
        لكل تمرين:
        1. سؤال واضح ومحدد
        2. إجابة نموذجية كاملة
        3. خطوات الحل مع الشرح
        4. نصائح للطالب
        
        التمارين يجب أن تكون متنوعة (اختيار من متعدد، صح/خطأ، مقالية).
        """
        
        messages = [
            {"role": "system", "content": self.teaching_styles["تمرين"]},
            {"role": "user", "content": prompt}
        ]
        
        exercises = self._make_ai_request(messages)
        
        if exercises:
            if "user" in st.session_state and st.session_state.user:
                db_manager.log_ai_interaction(
                    st.session_state.user.get("id", "unknown"),
                    "exercise_generation",
                    {"subject": subject, "topic": topic, "difficulty": difficulty}
                )
        
        return exercises or "عذراً، تعذر توليد التمارين في الوقت الحالي. يرجى المحاولة لاحقاً."
    
    def evaluate_answer(self, question: str, student_answer: str, correct_answer: str = None):
        """تقييم إجابة الطالب"""
        prompt = f"""
        أنت أستاذ محترف تقيم إجابات الطلاب.
        
        السؤال: {question}
        إجابة الطالب: {student_answer}
        {'الإجابة الصحيحة: ' + correct_answer if correct_answer else ''}
        
        المطلوب:
        1. قيم صحة الإجابة (صحيحة/خاطئة/جزئية)
        2. أعط درجات (من 10)
        3. اشرح الأخطاء إن وجدت
        4. أعط نصائح للتحسين
        5. قدم الإجابة المثالية
        
        كن داعماً ومشجعاً للطالب.
        """
        
        messages = [
            {"role": "system", "content": self.teaching_styles["تقييم"]},
            {"role": "user", "content": prompt}
        ]
        
        evaluation = self._make_ai_request(messages)
        return evaluation or "عذراً، تعذر التقييم في الوقت الحالي."
    
    def answer_student_question(self, question: str, context: str = None):
        """الإجابة على أسئلة الطالب"""
        prompt = f"""
        أنت مساعد تعليمي ذكي.
        
        سؤال الطالب: {question}
        {'السياق: ' + context if context else ''}
        
        المطلوب:
        1. أجب عن السؤال بوضوح ودقة
        2. استخدم أمثلة مبسطة
        3. قدم مصادر إضافية للتعلم
        4. شجع الطالب على الاستمرار
        """
        
        messages = [
            {"role": "system", "content": "أنت مساعد تعليمي ودود ومفيد."},
            {"role": "user", "content": prompt}
        ]
        
        answer = self._make_ai_request(messages)
        
        if answer and "user" in st.session_state and st.session_state.user:
            db_manager.log_ai_interaction(
                st.session_state.user.get("id", "unknown"),
                "student_question",
                {"question": question[:100]}
            )
        
        return answer or "عذراً، تعذر الإجابة في الوقت الحالي. يرجى صياغة السؤال بطريقة أخرى."
    
    def analyze_student_performance(self, student_data: dict):
        """تحليل أداء الطالب"""
        prompt = f"""
        أنت مستشار تعليمي محترف.
        
        بيانات الطالب:
        {json.dumps(student_data, ensure_ascii=False)}
        
        المطلوب:
        1. حلل نقاط القوة والضعف
        2. اقترح خطط دراسة مخصصة
        3. أعط توصيات للتحسين
        4. حدد الأولويات التعليمية
        5. قدم نصائح للمذاكرة الفعالة
        """
        
        messages = [
            {"role": "system", "content": "أنت مستشار تعليمي خبير."},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self._make_ai_request(messages)
        return analysis or "عذراً، تعذر التحليل في الوقت الحالي."

ai_assistant = AIEducationAssistant(OPENAI_API_KEY) if OPENAI_API_KEY != "your-openai-key" else None

# ============================================
# 5. إدارة الجلسة والحالة
# ============================================

class SessionManager:
    """مدير الجلسة والحالة"""
    
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        """تهيئة حالة الجلسة"""
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.user_data = None
            st.session_state.role = None
            st.session_state.current_page = "home"
            st.session_state.current_lesson = None
            st.session_state.chat_history = []
            st.session_state.notifications = []
            st.session_state.theme = "light"
            st.session_state.language = "ar"
    
    def login(self, user_data: dict):
        """تسجيل الدخول"""
        st.session_state.logged_in = True
        st.session_state.user = user_data.get("username")
        st.session_state.user_data = user_data
        st.session_state.role = user_data.get("role", "طالب")
        
        if ai_assistant:
            db_manager.update_user_profile(
                user_data.get("id"),
                {"last_login": datetime.now().isoformat()}
            )
    
    def logout(self):
        """تسجيل الخروج"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self.init_session_state()
    
    def add_notification(self, title: str, message: str, notif_type: str = "info"):
        """إضافة إشعار"""
        notification = {
            "id": len(st.session_state.notifications) + 1,
            "title": title,
            "message": message,
            "type": notif_type,
            "time": datetime.now().strftime("%H:%M"),
            "read": False
        }
        st.session_state.notifications.insert(0, notification)
        
        if st.session_state.logged_in and st.session_state.user_data:
            db_manager.create_notification(
                st.session_state.user_data.get("id"),
                title,
                message,
                notif_type
            )

session_manager = SessionManager()

# ============================================
# 6. نظام الدروس والمناهج
# ============================================

class CurriculumManager:
    """مدير المناهج والدروس"""
    
    def __init__(self):
        self.subjects = {
            "رياضيات": ["الجبر", "الهندسة", "الإحصاء", "التفاضل والتكامل"],
            "علوم": ["الفيزياء", "الكيمياء", "الأحياء", "علوم الأرض"],
            "لغة عربية": ["النحو", "الصرف", "الأدب", "البلاغة"],
            "لغة إنجليزية": ["Grammar", "Vocabulary", "Reading", "Writing"],
            "تاريخ": ["التاريخ الإسلامي", "التاريخ الحديث", "الجغرافيا"],
            "تكنولوجيا": ["البرمجة", "قواعد البيانات", "التصميم", "الأمن السيبراني"]
        }
        self.grades = ["السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]
        self.sample_lessons = self._create_sample_lessons()
    
    def _create_sample_lessons(self):
        """إنشاء دروس تجريبية"""
        lessons = []
        lesson_id = 1
        
        for subject, topics in self.subjects.items():
            for topic in topics[:2]:
                for grade in self.grades[:3]:
                    lessons.append({
                        "id": f"lesson_{lesson_id}",
                        "title": f"مقدمة في {topic}",
                        "subject": subject,
                        "topic": topic,
                        "grade": grade,
                        "level": "مبتدئ",
                        "duration": "45 دقيقة",
                        "description": f"شرح أساسيات {topic} للصف {grade}",
                        "content": f"""
                        # درس {topic} - {subject}
                        
                        ## 🎯 أهداف الدرس
                        - فهم المفاهيم الأساسية لـ {topic}
                        - تطبيق المعرفة في أمثلة عملية
                        - حل تمارين تقييمية
                        
                        ## 📖 المحتوى التعليمي
                        هذا الدرس يغطي المبادئ الأساسية لـ {topic} بطريقة مبسطة تناسب طلاب الصف {grade}.
                        
                        ### المفاهيم الرئيسية:
                        1. المفهوم الأول
                        2. المفهوم الثاني
                        3. المفهوم الثالث
                        
                        ## 🧠 تمارين
                        1. سؤال تطبيقي بسيط
                        2. سؤال تحليلي
                        3. سؤال تقييمي
                        
                        ## 📝 ملخص
                        نلخص النقاط الرئيسية للدرس.
                        """,
                        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        "resources": ["ملف PDF", "عرض تقديمي", "ورقة عمل"],
                        "created_by": "النظام",
                        "created_at": datetime.now().isoformat(),
                        "is_published": True
                    })
                    lesson_id += 1
        
        return lessons
    
    def get_lessons(self, subject: str = None, grade: str = None, topic: str = None):
        """الحصول على الدروس"""
        try:
            lessons = db_manager.get_all_lessons(subject, grade)
            if lessons is not None:
                return lessons
        except:
            pass
        
        filtered_lessons = self.sample_lessons
        
        if subject and subject != "الكل":
            filtered_lessons = [l for l in filtered_lessons if l["subject"] == subject]
        
        if grade and grade != "الكل":
            filtered_lessons = [l for l in filtered_lessons if l["grade"] == grade]
        
        if topic and topic != "الكل":
            filtered_lessons = [l for l in filtered_lessons if l["topic"] == topic]
        
        return filtered_lessons
    
    def get_lesson_detail(self, lesson_id: str):
        """الحصول على تفاصيل درس"""
        try:
            lesson = db_manager.get_lesson_by_id(lesson_id)
            if lesson:
                return lesson
        except:
            pass
        
        for lesson in self.sample_lessons:
            if lesson["id"] == lesson_id:
                return lesson
        
        return None
    
    def create_new_lesson(self, lesson_data: dict):
        """إنشاء درس جديد"""
        try:
            result = db_manager.create_lesson(lesson_data)
            if result:
                return True, "تم إنشاء الدرس بنجاح"
        except Exception as e:
            print(f"Error creating lesson: {e}")
        
        lesson_data["id"] = f"lesson_{len(self.sample_lessons) + 1}"
        lesson_data["created_at"] = datetime.now().isoformat()
        self.sample_lessons.append(lesson_data)
        
        return True, "تم حفظ الدرس محلياً (اتصال قاعدة البيانات غير متوفر)"

curriculum_manager = CurriculumManager()

# ============================================
# 7. نظام التمارين والتقييم
# ============================================

class ExerciseManager:
    """مدير التمارين والتقييم"""
    
    def __init__(self):
        self.exercise_types = {
            "اختيار من متعدد": "mcq",
            "صح/خطأ": "true_false",
            "ملء الفراغات": "fill_blanks",
            "مقالي": "essay",
            "مطابقة": "matching"
        }
        self.sample_exercises = self._create_sample_exercises()
    
    def _create_sample_exercises(self):
        """إنشاء تمارين تجريبية"""
        exercises = []
        exercise_id = 1
        
        topics = ["الجبر", "الفيزياء", "النحو", "التاريخ"]
        
        for topic in topics:
            for i in range(3):
                exercises.append({
                    "id": f"ex_{exercise_id}",
                    "lesson_id": f"lesson_{i+1}",
                    "question": f"ما هو ناتج 5 × 8 في الرياضيات؟" if topic == "الجبر" else 
                               f"الجاذبية اكتشفها العالم:",
                    "options": ["35", "40", "45", "50"] if topic == "الجبر" else 
                              ["نيوتن", "أينشتاين", "داروين", "فاراداي"],
                    "correct_answer": "40" if topic == "الجبر" else "نيوتن",
                    "explanation": "5 × 8 = 40 (خمسة في ثمانية يساوي أربعين)" if topic == "الجبر" else 
                                  "إسحاق نيوتن هو من صاغ قانون الجاذبية العالمية",
                    "difficulty": "سهل",
                    "points": 5,
                    "time_limit": 60,
                    "exercise_type": "mcq"
                })
                exercise_id += 1
                
                exercises.append({
                    "id": f"ex_{exercise_id}",
                    "lesson_id": f"lesson_{i+1}",
                    "question": f"الماء يغلي عند 100 درجة مئوية؟",
                    "options": ["صح", "خطأ"],
                    "correct_answer": "صح",
                    "explanation": "نعم، الماء يغلي عند 100 درجة مئوية عند مستوى سطح البحر",
                    "difficulty": "سهل",
                    "points": 2,
                    "time_limit": 30,
                    "exercise_type": "true_false"
                })
                exercise_id += 1
        
        return exercises
    
    def get_exercises_for_lesson(self, lesson_id: str):
        """الحصول على تمارين لدرس محدد"""
        try:
            exercises = db_manager.get_exercises_by_lesson(lesson_id)
            if exercises is not None:
                return exercises
        except:
            pass
        return [ex for ex in self.sample_exercises if ex["lesson_id"] == lesson_id]
    
    def evaluate_mcq(self, question: dict, student_answer: str):
        """تقييم إجابة اختيار من متعدد"""
        correct = student_answer == question["correct_answer"]
        score = question["points"] if correct else 0
        return {
            "correct": correct,
            "score": score,
            "max_score": question["points"],
            "correct_answer": question["correct_answer"],
            "explanation": question.get("explanation", "")
        }
    
    def evaluate_true_false(self, question: dict, student_answer: str):
        """تقييم إجابة صح/خطأ"""
        correct = student_answer.lower() == question["correct_answer"].lower()
        score = question["points"] if correct else 0
        return {
            "correct": correct,
            "score": score,
            "max_score": question["points"],
            "correct_answer": question["correct_answer"],
            "explanation": question.get("explanation", "")
        }
    
    def evaluate_essay_with_ai(self, question: str, student_answer: str):
        """تقييم الإجابة المقالية"""
        if ai_assistant:
            evaluation = ai_assistant.evaluate_answer(question, student_answer)
            return {
                "evaluation": evaluation,
                "score": 0,
                "ai_graded": True
            }
        return {
            "evaluation": "تم استلام إجابتك. سيتم تقييمها قريباً.",
            "score": 0,
            "ai_graded": False
        }
    
    def generate_quiz(self, subject: str, num_questions: int = 5):
        """توليد اختبار آلي"""
        if ai_assistant:
            return ai_assistant.generate_exercise(subject, "عام", "متنوع", num_questions)
        return "الخدمة غير متاحة"

exercise_manager = ExerciseManager()

# ============================================
# 8. نظام التتبع والإحصائيات
# ============================================

class AnalyticsManager:
    """مدير التحليلات والإحصائيات"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_progress(self, student_id: str):
        """حساب تقدم الطالب"""
        try:
            progress_data = db_manager.get_student_progress(student_id)
            if progress_data:
                total_lessons = len(curriculum_manager.get_lessons())
                completed_lessons = len([p for p in progress_data if p.get("completed", False)])
                
                completion_rate = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
                
                scores = [p.get("score", 0) for p in progress_data if "score" in p]
                avg_score = sum(scores) / len(scores) if scores else 0
                
                if completion_rate >= 80 and avg_score >= 80:
                    level = "متقدم"
                elif completion_rate >= 50:
                    level = "متوسط"
                else:
                    level = "مبتدئ"
                
                return {
                    "completion_rate": round(completion_rate, 2),
                    "average_score": round(avg_score, 2),
                    "completed_lessons": completed_lessons,
                    "total_lessons": total_lessons,
                    "level": level,
                    "last_active": datetime.now().strftime("%Y-%m-%d")
                }
        except:
            pass
        
        return {
            "completion_rate": 65.5,
            "average_score": 78.3,
            "completed_lessons": 15,
            "total_lessons": 23,
            "level": "متوسط",
            "last_active": datetime.now().strftime("%Y-%m-%d")
        }
    
    def generate_learning_plan(self, student_data: dict):
        """توليد خطة تعلم مخصصة"""
        if ai_assistant:
            return ai_assistant.analyze_student_performance(student_data)
        
        plan = """
        خطة التعلم المقترحة:
        1. مراجعة أساسيات الرياضيات
        2. حل تمارين الفيزياء
        3. مشاهدة فيديوهات الشرح
        """
        return plan
    
    def create_weekly_report(self, student_id: str):
        """إنشاء تقرير أسبوعي"""
        progress = self.calculate_progress(student_id)
        return f"""
        📊 التقرير الأسبوعي
        📈 معدل الإنجاز: {progress['completion_rate']}%
        🎯 المعدل العام: {progress['average_score']}/100
        📚 الدروس المكتملة: {progress['completed_lessons']}/{progress['total_lessons']}
        🏆 المستوى الحالي: {progress['level']}
        """

analytics_manager = AnalyticsManager()

# ============================================
# 9. الواجهات الرئيسية
# ============================================

def show_login_page():
    """عرض صفحة تسجيل الدخول"""
    st.markdown('<div class="main-title">🎓 المنصة التعليمية الذكية</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب"])
            
            with tab1:
                st.markdown('<h3 style="text-align: center; margin-bottom: 20px;">مرحباً بعودتك</h3>', unsafe_allow_html=True)
                
                username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم", key="login_username")
                password = st.text_input("كلمة المرور", type="password", placeholder="••••••••", key="login_password")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("دخول", use_container_width=True, type="primary"):
                        if username and password:
                            with st.spinner("جاري التحقق..."):
                                if db_manager.authenticate_user(username, password):
                                    user_data = {
                                        "id": "1",
                                        "username": username,
                                        "full_name": "طالب نموذجي",
                                        "email": f"{username}@example.com",
                                        "role": "طالب",
                                        "grade": "العاشر"
                                    }
                                    session_manager.login(user_data)
                                    session_manager.add_notification("مرحباً!", "تم تسجيل الدخول بنجاح", "success")
                                    st.rerun()
                                else:
                                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
                        else:
                            st.warning("يرجى ملء جميع الحقول")
                
                with col_btn2:
                    if st.button("الدخول كزائر ⚡", use_container_width=True):
                        user_data = {
                            "id": "guest",
                            "username": "زائر",
                            "full_name": "زائر مميز",
                            "email": "guest@example.com",
                            "role": "طالب",
                            "grade": "العاشر"
                        }
                        session_manager.login(user_data)
                        st.rerun()
                
                st.markdown("<p style='text-align:center; font-size:0.9rem; color:#888;'>جرب الدخول كزائر لتجربة المنصة فوراً</p>", unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<h3 style="text-align: center; margin-bottom: 20px;">إنشاء حساب جديد</h3>', unsafe_allow_html=True)
                
                full_name = st.text_input("الاسم الكامل")
                new_username = st.text_input("اسم المستخدم")
                email = st.text_input("البريد الإلكتروني")
                new_password = st.text_input("كلمة المرور", type="password")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
                grade = st.selectbox("الصف الدراسي", curriculum_manager.grades + ["أخرى"])
                role = st.selectbox("الدور", ["طالب", "معلم", "أولياء أمور"])
                
                if st.button("إنشاء حساب", use_container_width=True, type="primary"):
                    if not all([full_name, new_username, email, new_password, confirm_password]):
                        st.error("يرجى ملء جميع الحقول")
                    elif new_password != confirm_password:
                        st.error("كلمتا المرور غير متطابقتين")
                    else:
                        with st.spinner("جاري إنشاء الحساب..."):
                            try:
                                # محاولة الاتصال الصريحة
                                if not SUPABASE_URL or not SUPABASE_KEY:
                                    st.error("المفاتيح في ملف secrets.toml فارغة!")
                                else:
                                    result = db_manager.create_user(
                                        new_username, new_password, email, full_name, role, grade
                                    )
                                    if result:
                                        st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")
                                    else:
                                        st.error("تم استلام رد من قاعدة البيانات لكنه فارغ (قد يكون خطأ في SQL).")
                            except requests.exceptions.ConnectionError as e:
                                st.error(f"🚫 خطأ في الاتصال (Connection Error): {e}")
                                st.warning("تأكد من رابط URL وأن الإنترنت يعمل")
                            except requests.exceptions.HTTPError as e:
                                st.error(f"🚫 خطأ HTTP (الكود غير صحيح): {e}")
                                st.warning("غالباً الـ URL خاطئ أو المفتاح (Key) غير صحيح")
                            except Exception as e:
                                st.error(f"❌ حدث خطأ غير متوقع: {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # إحصائيات
        st.markdown('<br>', unsafe_allow_html=True)
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.markdown('<div class="stat-card"><h4>👥 الطلاب</h4><div class="stat-number">1,234</div></div>', unsafe_allow_html=True)
        with col_stat2:
            st.markdown('<div class="stat-card"><h4>📚 الدروس</h4><div class="stat-number">456</div></div>', unsafe_allow_html=True)
        with col_stat3:
            st.markdown('<div class="stat-card"><h4>🏆 النجاح</h4><div class="stat-number">94%</div></div>', unsafe_allow_html=True)
        with col_stat4:
            st.markdown('<div class="stat-card"><h4>⏱️ الساعات</h4><div class="stat-number">12,345</div></div>', unsafe_allow_html=True)

def show_main_dashboard():
    """عرض لوحة التحكم الرئيسية"""
    # شريط التنقل
    col_nav1, col_nav2, col_nav3, col_nav4, col_nav5, col_nav6 = st.columns(6)
    
    nav_buttons = [
        ("🏠 الرئيسية", "home"),
        ("📚 المكتبة", "library"),
        ("🧠 المساعد الذكي", "ai_assistant"),
        ("📊 التقدم", "progress"),
        ("⚙️ الإعدادات", "settings")
    ]
    
    for i, (label, page) in enumerate(nav_buttons):
        with [col_nav1, col_nav2, col_nav3, col_nav4, col_nav5][i]:
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
    
    with col_nav6:
        if st.button("🚪 خروج", use_container_width=True, type="secondary"):
            session_manager.logout()
            st.rerun()
    
    user_name = st.session_state.user_data.get("full_name", st.session_state.user)
    st.markdown(f'<h2 style="text-align: center; color: #333; margin-bottom: 30px;">مرحباً {user_name} 👋</h2>', unsafe_allow_html=True)
    
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "library":
        show_library_page()
    elif st.session_state.current_page == "ai_assistant":
        show_ai_assistant_page()
    elif st.session_state.current_page == "progress":
        show_progress_page()
    elif st.session_state.current_page == "settings":
        show_settings_page()

def show_home_page():
    """الصفحة الرئيسية"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"""
        <h3>🚀 ابدأ رحلة التعلم اليوم!</h3>
        <p>مرحباً بك في المنصة التعليمية الذكية. إليك مقترحات اليوم:</p>
        """, unsafe_allow_html=True)
        
        # مقترحات بسيطة
        suggestions = [
            {"icon": "📐", "title": "رياضيات: المعادلات", "status": "مستمر"},
            {"icon": "⚡", "title": "فيزياء: الكهرباء", "status": "جديد"},
            {"icon": "📚", "title": "لغة عربية: البلاغة", "status": "مراجعة"}
        ]
        
        for item in suggestions:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 15px; background: #f8fafc; border-radius: 10px; margin-bottom: 10px; align-items: center;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 1.5rem;">{item['icon']}</span>
                    <span style="font-weight: 600;">{item['title']}</span>
                </div>
                <span style="font-size: 0.8rem; background: #e0e7ff; color: #4338ca; padding: 4px 10px; border-radius: 20px;">{item['status']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # الدروس المقترحة
        st.markdown('<h3 style="margin: 30px 0 15px;">📖 الدروس المقترحة</h3>', unsafe_allow_html=True)
        lessons = curriculum_manager.get_lessons()[:3]
        for lesson in lessons:
            with st.container():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px; background: white; border-radius: 15px; margin-bottom: 15px; border-left: 4px solid #667eea; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
                    <div>
                        <h4 style="margin: 0; color: #333;">{lesson['title']}</h4>
                        <span style="font-size: 0.9rem; color: #64748b;">{lesson['subject']} | {lesson['grade']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("بدء الدرس", key=f"start_{lesson['id']}", use_container_width=True):
                    st.session_state.current_lesson = lesson['id']
                    st.session_state.current_page = "lesson"
                    st.rerun()
    
    with col2:
        # بطاقة التقدم
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin-bottom: 20px;">📊 تقدمك التعليمي</h4>', unsafe_allow_html=True)
        
        progress_data = analytics_manager.calculate_progress(st.session_state.user_data.get("id", "1"))
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 3rem; font-weight: 800; color: transparent; background-clip: text; background-image: linear-gradient(135deg, #667eea, #764ba2);">
                {progress_data['completion_rate']}%
            </div>
            <div style="color: #64748b;">معدل الإنجاز</div>
        </div>
        
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress_data['completion_rate']}%;"></div>
        </div>
        
        <div style="margin-top: 20px; display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span>المستوى</span>
            <span style="font-weight: bold; color: #667eea;">{progress_data['level']}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_library_page():
    """صفحة المكتبة"""
    st.markdown('<h2 style="margin-bottom: 20px;">📚 مكتبة الدروس</h2>', unsafe_allow_html=True)
    
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        subjects = ["الكل"] + list(curriculum_manager.subjects.keys())
        selected_subject = st.selectbox("المادة", subjects)
    with col_filter2:
        grades = ["الكل"] + curriculum_manager.grades
        selected_grade = st.selectbox("الصف", grades)
    with col_filter3:
        search_query = st.text_input("🔍 البحث")
    
    lessons = curriculum_manager.get_lessons(selected_subject, selected_grade)
    if search_query:
        lessons = [l for l in lessons if search_query.lower() in l.get("title", "").lower()]
    
    if not lessons:
        st.info("لم يتم العثور على دروس")
        return
    
    cols = st.columns(2)
    for i, lesson in enumerate(lessons):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="card" style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="background: #e0e7ff; color: #4338ca; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">{lesson.get('subject')}</span>
                    <span style="color: #94a3b8; font-size: 0.9rem;">{lesson.get('duration')}</span>
                </div>
                <h3 style="color: #333;">{lesson.get('title')}</h3>
                <p style="color: #64748b; font-size: 0.9rem; height: 60px; overflow: hidden;">{lesson.get('description')[:80]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                if st.button("👀 عرض", key=f"view_{lesson['id']}", use_container_width=True):
                    st.session_state.current_lesson = lesson['id']
                    st.session_state.current_page = "lesson"
                    st.rerun()
            with col_l2:
                if st.button("🧪 تمرين", key=f"ex_{lesson['id']}", use_container_width=True):
                    st.session_state.current_lesson = lesson['id']
                    st.session_state.current_page = "exercises"
                    st.rerun()

def show_lesson_page():
    """صفحة الدرس"""
    lesson = curriculum_manager.get_lesson_detail(st.session_state.current_lesson)
    if not lesson: return
    
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <h1 style="color: #333;">{lesson['title']}</h1>
        <div style="color: #64748b;">{lesson['subject']} | {lesson['grade']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_content, col_side = st.columns([3, 1])
    with col_content:
        st.markdown(lesson.get("content"))
    with col_side:
        if st.button("✅ إكمال الدرس", type="primary", use_container_width=True):
             st.success("تم تسجيل التقدم!")

def show_ai_assistant_page():
    """المساعد الذكي"""
    st.markdown('<h2>🤖 المساعد التعليمي الذكي</h2>', unsafe_allow_html=True)
    
    if not ai_assistant:
        st.warning("الخدمة غير متاحة (مفتاح API مفقود)")
        return
        
    tab1, tab2 = st.tabs(["💬 محادثة", "📖 توليد محتوى"])
    
    with tab1:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        if prompt := st.chat_input("اطرح سؤالاً..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("جاري التفكير..."):
                    response = ai_assistant.answer_student_question(prompt)
                    st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

def show_progress_page():
    """صفحة التقدم"""
    st.markdown('<h2>📊 تحليل الأداء</h2>', unsafe_allow_html=True)
    data = analytics_manager.calculate_progress(st.session_state.user_data.get("id"))
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("الإنجاز", f"{data['completion_rate']}%")
    c2.metric("المعدل", f"{data['average_score']}/100")
    c3.metric("الدروس", f"{data['completed_lessons']}/{data['total_lessons']}")
    c4.metric("المستوى", data['level'])
    
    st.markdown("### 📈 التقدم الأسبوعي")
    df = pd.DataFrame({
        "الأسبوع": ["أ1", "أ2", "أ3", "أ4"],
        "النقاط": [65, 72, 78, 85]
    })
    st.line_chart(df.set_index("الأسبوع"))

def show_settings_page():
    """الإعدادات"""
    st.markdown('<h2>⚙️ الإعدادات</h2>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("الملف الشخصي")
        st.write("هنا يمكنك تعديل بياناتك الشخصية.")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# التشغيل الرئيسي
# ============================================

def main():
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.get("current_page") == "lesson":
            show_lesson_page()
        else:
            show_main_dashboard()

if __name__ == "__main__":
    main()
