"""
مدير الجلسة والحالة
"""
import streamlit as st
from datetime import datetime
from typing import Dict, List
from .supabase_manager import db_manager

class SessionManager:
    """فئة إدارة الجلسة"""
    
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        """تهيئة حالة الجلسة"""
        default_states = {
            "logged_in": False,
            "user": None,
            "user_data": None,
            "role": None,
            "current_page": "home",
            "current_lesson": None,
            "chat_history": [],
            "notifications": [],
            "theme": "light",
            "language": "ar"
        }
        
        for key, value in default_states.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def login(self, user_data: Dict):
        """تسجيل الدخول"""
        st.session_state.logged_in = True
        st.session_state.user = user_data.get("username")
        st.session_state.user_data = user_data
        st.session_state.role = user_data.get("role", "طالب")
        
        # تحديث آخر تسجيل دخول
        db_manager.update_user(user_data.get("id"), {
            "last_login": datetime.now().isoformat()
        })
    
    def logout(self):
        """تسجيل الخروج"""
        keys_to_keep = ["theme", "language"]
        current_values = {k: st.session_state.get(k) for k in keys_to_keep}
        
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        for k, v in current_values.items():
            st.session_state[k] = v
        
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
        
        # حفظ في قاعدة البيانات
        if st.session_state.user_data:
            db_manager.create_notification(
                st.session_state.user_data.get("id"),
                title,
                message,
                notif_type
            )
    
    def get_unread_notifications(self) -> List[Dict]:
        """الحصول على الإشعارات غير المقروءة"""
        return [n for n in st.session_state.notifications if not n.get("read")]

# تهيئة المدير
session_manager = SessionManager()
