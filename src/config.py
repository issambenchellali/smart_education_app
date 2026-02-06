"""
ملف إعدادات التطبيق
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """فئة إعدادات التطبيق"""
    
    # Supabase
    SUPABASE_URL = os.getenv("https://tsossglwefidkyvtprls.supabase.co", "")
    SUPABASE_KEY = os.getenv("sb_publishable_sKTHKljlq5MKIbu-kT21aA_1orzuIc8", "")
    SUPABASE_SERVICE_KEY = os.getenv("sb_publishable_sKTHKljlq5MKIbu-kT21aA_1orzuIc8", "")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Application
    APP_NAME = os.getenv("APP_NAME", "المنصة التعليمية الذكية")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))
    
    # Storage
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))
    ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "pdf,doc,docx,ppt,pptx,jpg,jpeg,png,mp4").split(",")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    CSS_DIR = os.path.join(ASSETS_DIR, "css")
    IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
    
    # التعليمات
    SUBJECTS = {
        "رياضيات": ["الجبر", "الهندسة", "الإحصاء", "التفاضل والتكامل"],
        "علوم": ["الفيزياء", "الكيمياء", "الأحياء", "علوم الأرض"],
        "لغة عربية": ["النحو", "الصرف", "الأدب", "البلاغة"],
        "لغة إنجليزية": ["Grammar", "Vocabulary", "Reading", "Writing"],
        "تاريخ": ["التاريخ الإسلامي", "التاريخ الحديث", "الجغرافيا"],
        "تكنولوجيا": ["البرمجة", "قواعد البيانات", "التصميم", "الأمن السيبراني"]
    }
    
    GRADES = ["السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]
    
    # أنماط التعليم
    TEACHING_STYLES = {
        "شرح": "كن أستاذاً محترفاً تشرح المفاهيم بشكل مبسط مع أمثلة",
        "تمرين": "أنشئ تمارين تعليمية مع حلول وتفسيرات",
        "مراجعة": "راجع الدروس مع تركيز على النقاط المهمة",
        "تقييم": "قيم مستوى الطالب وأعط توصيات للتحسين"
    }
    
    # أنواع التمارين
    EXERCISE_TYPES = {
        "اختيار من متعدد": "mcq",
        "صح/خطأ": "true_false",
        "ملء الفراغات": "fill_blanks",
        "مقالي": "essay",
        "مطابقة": "matching"
    }

config = Config()
