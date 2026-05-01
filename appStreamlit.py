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
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Supabase Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def create_user(self, username: str, password: str, email: str, full_name: str
