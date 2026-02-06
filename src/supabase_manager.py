"""
مدير قاعدة البيانات باستخدام Supabase
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from supabase import create_client, Client
from .config import config

class SupabaseManager:
    """فئة إدارة قاعدة البيانات"""
    
    def __init__(self):
        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        self.tables = {
            "users": "users",
            "lessons": "lessons",
            "exercises": "exercises",
            "progress": "student_progress",
            "ai_interactions": "ai_interactions",
            "notifications": "notifications",
            "files": "files"
        }
    
    # ===== إدارة المستخدمين =====
    def create_user(self, user_data: Dict) -> Optional[Dict]:
        try:
            user_data["created_at"] = datetime.now().isoformat()
            user_data["updated_at"] = datetime.now().isoformat()
            
            response = self.client.table(self.tables["users"]).insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        try:
            response = self.client.table(self.tables["users"])\
                .select("*")\
                .eq("username", username)\
                .eq("is_active", True)\
                .execute()
            
            if response.data:
                user = response.data[0]
                # التحقق من كلمة المرور (مبسط)
                if user.get("password") == password:  # في الإنتاج استخدم التجزئة
                    # تحديث آخر تسجيل دخول
                    self.update_user(user["id"], {"last_login": datetime.now().isoformat()})
                    return user
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def update_user(self, user_id: str, updates: Dict) -> bool:
        try:
            updates["updated_at"] = datetime.now().isoformat()
            response = self.client.table(self.tables["users"])\
                .update(updates)\
                .eq("id", user_id)\
                .execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    # ===== إدارة الدروس =====
    def create_lesson(self, lesson_data: Dict) -> Optional[Dict]:
        try:
            lesson_data.update({
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "is_published": True
            })
            
            response = self.client.table(self.tables["lessons"]).insert(lesson_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating lesson: {e}")
            return None
    
    def get_lessons(self, filters: Dict = None) -> List[Dict]:
        try:
            query = self.client.table(self.tables["lessons"])\
                .select("*")\
                .eq("is_published", True)\
                .order("created_at", desc=True)
            
            if filters:
                if filters.get("subject"):
                    query = query.eq("subject", filters["subject"])
                if filters.get("grade"):
                    query = query.eq("grade", filters["grade"])
            
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error getting lessons: {e}")
            return []
    
    # ===== إدارة التقدم =====
    def update_progress(self, student_id: str, lesson_id: str, data: Dict) -> Optional[Dict]:
        try:
            data.update({
                "student_id": student_id,
                "lesson_id": lesson_id,
                "updated_at": datetime.now().isoformat()
            })
            
            # التحقق من وجود سجل سابق
            existing = self.client.table(self.tables["progress"])\
                .select("*")\
                .eq("student_id", student_id)\
                .eq("lesson_id", lesson_id)\
                .execute()
            
            if existing.data:
                response = self.client.table(self.tables["progress"])\
                    .update(data)\
                    .eq("id", existing.data[0]["id"])\
                    .execute()
            else:
                data["started_at"] = datetime.now().isoformat()
                response = self.client.table(self.tables["progress"]).insert(data).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating progress: {e}")
            return None
    
    def get_student_progress(self, student_id: str) -> List[Dict]:
        try:
            response = self.client.table(self.tables["progress"])\
                .select("*")\
                .eq("student_id", student_id)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting progress: {e}")
            return []
    
    # ===== إدارة الإشعارات =====
    def create_notification(self, user_id: str, title: str, message: str, type: str = "info") -> Optional[Dict]:
        try:
            notification = {
                "user_id": user_id,
                "title": title,
                "message": message,
                "type": type,
                "is_read": False,
                "created_at": datetime.now().isoformat()
            }
            
            response = self.client.table(self.tables["notifications"]).insert(notification).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None
    
    # ===== إحصائيات النظام =====
    def get_statistics(self) -> Dict:
        try:
            stats = {}
            
            # عدد المستخدمين
            users_resp = self.client.table(self.tables["users"])\
                .select("count")\
                .eq("is_active", True)\
                .execute()
            stats["total_users"] = users_resp.count
            
            # عدد الدروس
            lessons_resp = self.client.table(self.tables["lessons"])\
                .select("count")\
                .eq("is_published", True)\
                .execute()
            stats["total_lessons"] = lessons_resp.count
            
            # عدد التمارين
            exercises_resp = self.client.table(self.tables["exercises"])\
                .select("count")\
                .execute()
            stats["total_exercises"] = exercises_resp.count
            
            return stats
        except:
            return {
                "total_users": 0,
                "total_lessons": 0,
                "total_exercises": 0,
                "active_students": 0
            }

# تهيئة المدير
db_manager = SupabaseManager()
