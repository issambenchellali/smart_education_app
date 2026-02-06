# app.py - الملف الرئيسي
"""
المنصة التعليمية الذكية - النسخة المتطورة
"""

import streamlit as st
import json
import time
from datetime import datetime
import base64

# إعدادات الصفحة
st.set_page_config(
    page_title="المنصة التعليمية الذكية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# أضف في بداية app.py
st.markdown("""
<style>
    /* تصميم العنوان الرئيسي */
    .main-header {
        text-align: center;
        color: #1E88E5;
        padding: 20px;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1E88E5, #4A00E0, #1E88E5);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* بطاقات الدروس */
    .lesson-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .lesson-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .lesson-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #1E88E5, #4A00E0);
    }
    
    /* أزرار مميزة */
    .gradient-btn {
        background: linear-gradient(135deg, #1E88E5, #4A00E0);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
    }
    
    .gradient-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(30, 136, 229, 0.3);
    }
    
    /* شريط التقدم */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        height: 20px;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* تخصيص علامات التبويب */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: 2px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #1E88E5;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E88E5, #4A00E0);
        color: white !important;
    }
    
    /* كروت الإحصائيات */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin: 10px 0;
    }
    
    /* إخفاء عناصر Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تحسينات للهواتف */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .stat-number {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)



def login_page():
    """صفحة تسجيل الدخول المطورة"""
    
    # خلفية جميلة
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
    ">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 10px;">🎓</h1>
        <h2 style="color: white; margin-bottom: 10px;">المنصة التعليمية الذكية</h2>
        <p style="color: white; opacity: 0.9;">منصة تعليمية متكاملة مجانية للجميع</p>
    </div>
    """, unsafe_allow_html=True)
    
    # قسم تسجيل الدخول
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            
            st.markdown("### 🔐 تسجيل الدخول")
            
            # علامات تبويب
            tab_login, tab_register, tab_guest = st.tabs(["تسجيل الدخول", "إنشاء حساب", "الدخول السريع"])
            
            with tab_login:
                username = st.text_input("👤 اسم المستخدم", placeholder="أدخل اسم المستخدم")
                password = st.text_input("🔒 كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
                
                if st.button("🚀 دخول إلى المنصة", type="primary", use_container_width=True):
                    if authenticate(username, password):
                        st.success("تم تسجيل الدخول بنجاح!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة")
            
            with tab_register:
                st.markdown("#### 📝 إنشاء حساب جديد")
                
                with st.form("register_form"):
                    full_name = st.text_input("الاسم الكامل")
                    new_username = st.text_input("اسم المستخدم الجديد")
                    email = st.text_input("البريد الإلكتروني")
                    new_password = st.text_input("كلمة المرور", type="password")
                    confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
                    grade = st.selectbox("الصف الدراسي", ["السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"])
                    
                    if st.form_submit_button("✅ إنشاء حساب", use_container_width=True):
                        st.success("تم إنشاء الحساب بنجاح!")
            
            with tab_guest:
                st.markdown("#### 👀 تجربة المنصة كضيف")
                st.info("يمكنك تجربة جميع الميزات بدون حفظ بياناتك")
                
                if st.button("🎯 بدء التجربة كضيف", use_container_width=True):
                    st.session_state.user = {"name": "ضيف", "role": "طالب", "grade": "العاشر"}
                    st.session_state.logged_in = True
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # حسابات تجريبية
            with st.expander("💡 حسابات تجريبية", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("""
                    **👨‍🎓 طالب:**
                    - المستخدم: `student`
                    - كلمة المرور: `123456`
                    """)
                with col_b:
                    st.markdown("""
                    **👨‍🏫 معلم:**
                    - المستخدم: `teacher`
                    - كلمة المرور: `123456`
                    """)



def get_lessons_database():
    """قاعدة بيانات كاملة للدروس"""
    return {
        "رياضيات": [
            {
                "id": "math_1",
                "title": "مقدمة في الجبر",
                "description": "تعلم أساسيات الجبر والمعادلات البسيطة",
                "level": "مبتدئ",
                "duration": "45 دقيقة",
                "sections": [
                    {"title": "المفاهيم الأساسية", "content": "تعريف المتغيرات والمعادلات"},
                    {"title": "المعادلات البسيطة", "content": "حل المعادلات من الدرجة الأولى"},
                    {"title": "التطبيقات العملية", "content": "تطبيقات الجبر في الحياة اليومية"}
                ],
                "video_url": "https://www.youtube.com/watch?v=NybHckSEQBI",
                "exercises": [
                    {"question": "حل المعادلة: س + 5 = 12", "answer": "س = 7"},
                    {"question": "ما قيمة ص إذا كانت: 3ص = 21", "answer": "ص = 7"}
                ],
                "quiz": [
                    {"question": "ما هو المتغير في المعادلة 2س + 3 = 7؟", "options": ["2", "س", "3", "7"], "correct": 1},
                    {"question": "المعادلة س + 2 = 5 لها حل واحد", "options": ["صح", "خطأ"], "correct": 0}
                ]
            },
            {
                "id": "math_2",
                "title": "الهندسة الأساسية",
                "description": "تعلم الأشكال الهندسية وخصائصها",
                "level": "مبتدئ",
                "duration": "60 دقيقة",
                "sections": [
                    {"title": "الأشكال الثنائية", "content": "المربع، المستطيل، المثلث، الدائرة"},
                    {"title": "المحيط والمساحة", "content": "حساب محيط ومساحة الأشكال المختلفة"}
                ],
                "video_url": "https://www.youtube.com/watch?v=5wDpq7j02mM",
                "exercises": [
                    {"question": "احسب محيط مربع طول ضلعه 5 سم", "answer": "20 سم"},
                    {"question": "ما مساحة مستطيل طوله 6 سم وعرضه 4 سم؟", "answer": "24 سم²"}
                ]
            }
        ],
        "علوم": [
            {
                "id": "science_1",
                "title": "الخلية الحية",
                "description": "تعرف على مكونات الخلية الحيوانية والنباتية",
                "level": "متوسط",
                "duration": "50 دقيقة",
                "sections": [
                    {"title": "مكونات الخلية", "content": "النواة، السيتوبلازم، الغشاء الخلوي"},
                    {"title": "الفرق بين الخلايا", "content": "مقارنة بين الخلية الحيوانية والنباتية"}
                ],
                "video_url": "https://www.youtube.com/watch?v=URUJD5NEXC8",
                "exercises": [
                    {"question": "اذكر ثلاثة مكونات للخلية", "answer": "النواة، السيتوبلازم، الغشاء الخلوي"},
                    {"question": "ما الفرق بين الخلية النباتية والحيوانية؟", "answer": "الخلية النباتية تحتوي على جدار خلوي وبلاستيدات خضراء"}
                ]
            }
        ],
        "لغة عربية": [
            {
                "id": "arabic_1",
                "title": "القواعد النحوية",
                "description": "تعلم أساسيات النحو العربي",
                "level": "مبتدئ",
                "duration": "40 دقيقة",
                "sections": [
                    {"title": "أقسام الكلام", "content": "الاسم، الفعل، الحرف"},
                    {"title": "الإعراب الأساسي", "content": "الرفع، النصب، الجر، الجزم"}
                ],
                "video_url": "https://www.youtube.com/watch?v=5_h5gTgVzQ4",
                "exercises": [
                    {"question": "ما هو الفاعل في الجملة: 'قرأ الولد الكتاب'؟", "answer": "الولد"},
                    {"question": "أعرب كلمة 'الكتاب' في الجملة السابقة", "answer": "مفعول به منصوب"}
                ]
            }
        ]
    }



def interactive_lesson_view(lesson):
    """عرض درس تفاعلي"""
    
    st.title(f"📚 {lesson['title']}")
    
    # معلومات الدرس
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**📖 المادة:**")
            st.info(lesson.get('subject', 'عام'))
        with col2:
            st.markdown("**📊 المستوى:**")
            st.info(lesson.get('level', 'متوسط'))
        with col3:
            st.markdown("**⏱️ المدة:**")
            st.info(lesson.get('duration', '45 دقيقة'))
        with col4:
            progress = st.progress(0)
            st.caption("تقدمك في الدرس")
    
    # أقسام الدرس
    st.markdown("---")
    st.markdown("### 📖 محتوى الدرس")
    
    for i, section in enumerate(lesson.get('sections', []), 1):
        with st.expander(f"القسم {i}: {section['title']}", expanded=(i==1)):
            st.markdown(section['content'])
            
            # تحديث التقدم
            progress.progress(i / len(lesson['sections']))
            
            # أسئلة تفاعلية بعد كل قسم
            if st.button(f"🧠 اختبر فهمك للقسم {i}", key=f"quiz_{i}"):
                with st.container():
                    st.info("**سؤال سريع:** ما هو أهم مفهوم في هذا القسم؟")
                    answer = st.text_input("إجابتك:", key=f"answer_{i}")
                    if st.button("تحقق", key=f"check_{i}"):
                        st.success("جيد! واصل التعلم")
    
    # فيديو الشرح
    if lesson.get('video_url'):
        st.markdown("---")
        st.markdown("### 🎥 فيديو الشرح")
        st.video(lesson['video_url'])
    
    # التمارين
    st.markdown("---")
    st.markdown("### 🧠 تمارين الدرس")
    
    for i, exercise in enumerate(lesson.get('exercises', []), 1):
        with st.container():
            st.markdown(f"**تمرين {i}:** {exercise['question']}")
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                user_answer = st.text_input(f"إجابتك للتمرين {i}:", key=f"ex_{i}")
            with col_b:
                if st.button("📤 تسليم", key=f"submit_{i}"):
                    if user_answer.strip():
                        # مقارنة مبسطة للإجابات
                        if exercise['answer'].lower() in user_answer.lower():
                            st.success("✅ إجابة صحيحة!")
                        else:
                            st.error(f"❌ الإجابة الصحيحة: {exercise['answer']}")
                    else:
                        st.warning("⚠️ اكتب إجابة أولاً")
            
            st.markdown("---")
    
    # اختبار نهائي
    if lesson.get('quiz'):
        st.markdown("---")
        st.markdown("### 📝 اختبار الدرس النهائي")
        
        score = 0
        for i, q in enumerate(lesson['quiz'], 1):
            st.markdown(f"**سؤال {i}:** {q['question']}")
            
            if 'options' in q:
                answer = st.radio(f"اختر الإجابة:", q['options'], key=f"q{i}", label_visibility="collapsed")
            else:
                answer = st.text_input(f"إجابتك:", key=f"q{i}")
            
            if st.button(f"تحقق سؤال {i}", key=f"check_q{i}"):
                # منطق التحقق
                st.info("تم التحقق من إجابتك")
        
        if st.button("📊 عرض النتيجة النهائية", type="primary"):
            st.success(f"🎉 نتيجتك: {score}/{len(lesson['quiz'])}")
            if score == len(lesson['quiz']):
                st.balloons()



def educational_assistant():
    """مساعد تعليمي ذكي"""
    
    st.title("🤖 المساعد التعليمي الذكي")
    
    # تهيئة تاريخ المحادثة
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # عرض تاريخ المحادثة
    st.markdown("---")
    st.markdown("### 💬 محادثتك مع المساعد")
    
    for message in st.session_state.chat_history[-10:]:  # عرض آخر 10 رسائل
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # إدخال المستخدم
    st.markdown("---")
    user_input = st.chat_input("اطرح سؤالك التعليمي هنا...")
    
    if user_input:
        # إضافة سؤال المستخدم
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # محاكاة رد المساعد
        with st.chat_message("assistant"):
            with st.spinner("🤔 المساعد يفكر..."):
                time.sleep(1)  # محاكاة وقت المعالجة
                
                # ردود ذكية مبنية على السؤال
                response = generate_ai_response(user_input)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

def generate_ai_response(question):
    """توليد رد ذكي بناءً على السؤال"""
    
    # قاعدة معرفية للردود
    knowledge_base = {
        "رياضيات": {
            "keywords": ["جبر", "معادلة", "رياضيات", "حساب", "هندسة"],
            "responses": [
                "في الرياضيات، يمكنني مساعدتك في فهم:",
                "- المعادلات الجبرية",
                "- الأشكال الهندسية", 
                "- العمليات الحسابية",
                "أي موضوع محدد تريد المساعدة فيه؟"
            ]
        },
        "علوم": {
            "keywords": ["علوم", "خلية", "كيمياء", "فيزياء", "تجربة"],
            "responses": [
                "العلوم موضوع رائع! يمكنني شرح:",
                "- مكونات الخلية الحية",
                "- التفاعلات الكيميائية",
                "- قوانين الفيزياء",
                "ما هو المجال الذي تريد التعلم عنه؟"
            ]
        },
        "عربي": {
            "keywords": ["عربي", "نحو", "إعراب", "قواعد", "لغة"],
            "responses": [
                "اللغة العربية جميلة ومعقدة! يمكنني مساعدتك في:",
                "- قواعد النحو",
                "- الإعراب",
                "- البلاغة والأدب",
                "ما الذي يصعب عليك في اللغة العربية؟"
            ]
        }
    }
    
    # البحث عن الموضوع المناسب
    question_lower = question.lower()
    
    for subject, data in knowledge_base.items():
        for keyword in data["keywords"]:
            if keyword in question_lower:
                return "\n".join(data["responses"])
    
    # رد عام إذا لم يتم التعرف على الموضوع
    return """
    🤔 يبدو أن سؤالك يحتاج إلى مزيد من التوضيح.
    
    يمكنني مساعدتك في:
    - شرح الدروس في جميع المواد
    - حل التمارين والمسائل
    - مراجعة المفاهيم الأساسية
    - الإجابة على أسئلة الاختبارات
    
    💡 **نصيحة:** حاول أن تكون أكثر تحديداً في سؤالك.
    مثال: "كيف أحل المعادلة س + 2 = 5؟"
    """

def advanced_dashboard():
    """لوحة تحكم متقدمة"""
    
    # شريط جانبي متقدم
    with st.sidebar:
        st.markdown(f"# 👋 {st.session_state.user.get('name', 'مستخدم')}")
        
        # صورة المستخدم
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="
                width: 100px;
                height: 100px;
                background: linear-gradient(135deg, #1E88E5, #4A00E0);
                border-radius: 50%;
                margin: 0 auto 15px auto;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
                color: white;
            ">
                👨‍🎓
            </div>
            <h3 style="text-align: center;">{}</h3>
            <p style="text-align: center; color: #666;">{}</p>
        </div>
        """.format(
            st.session_state.user.get('name', 'مستخدم'),
            st.session_state.user.get('grade', 'طالب')
        ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # القائمة الرئيسية
        menu_items = [
            {"icon": "🏠", "label": "الرئيسية", "key": "home"},
            {"icon": "📚", "label": "الدروس", "key": "lessons"},
            {"icon": "🧠", "label": "التمارين", "key": "exercises"},
            {"icon": "📊", "label": "التقارير", "key": "reports"},
            {"icon": "🤖", "label": "المساعد", "key": "assistant"},
            {"icon": "🏆", "label": "الإنجازات", "key": "achievements"},
            {"icon": "⚙️", "label": "الإعدادات", "key": "settings"},
        ]
        
        selected_menu = st.radio(
            "القائمة الرئيسية",
            [f"{item['icon']} {item['label']}" for item in menu_items],
            label_visibility="collapsed"
        )
        
        # استخراج المفتاح المحدد
        selected_key = None
        for item in menu_items:
            if f"{item['icon']} {item['label']}" == selected_menu:
                selected_key = item['key']
                break
        
        st.markdown("---")
        
        # تقدم سريع
        st.markdown("### 📈 تقدمك السريع")
        st.progress(0.75)
        st.caption("75% من أهداف هذا الشهر")
        
        st.markdown("---")
        
        if st.button("🚪 تسجيل الخروج", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # عرض المحتوى حسب الاختيار
    if selected_key == "home":
        show_home_dashboard()
    elif selected_key == "lessons":
        show_lessons_page()
    elif selected_key == "exercises":
        show_exercises_page()
    elif selected_key == "reports":
        show_reports_page()
    elif selected_key == "assistant":
        educational_assistant()
    elif selected_key == "achievements":
        show_achievements_page()
    elif selected_key == "settings":
        show_settings_page()

def show_home_dashboard():
    """عرض لوحة التحكم الرئيسية"""
    
    st.markdown('<h1 class="main-header">🏠 لوحة التحكم الرئيسية</h1>', unsafe_allow_html=True)
    
    # إحصائيات سريعة
    st.markdown("### 📊 نظرة سريعة على أدائك")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div>📚</div>
            <div class="stat-number">12</div>
            <div>دروس مكتملة</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div>🧠</div>
            <div class="stat-number">47</div>
            <div>تمارين محلولة</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div>⏱️</div>
            <div class="stat-number">24.5</div>
            <div>ساعة تعلم</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div>⭐</div>
            <div class="stat-number">8</div>
            <div>إنجازات</div>
        </div>
        """, unsafe_allow_html=True)
    
    # نشاط اليوم
    st.markdown("---")
    st.markdown("### 📝 نشاط اليوم")
    
    today_activities = [
        {"time": "08:00", "subject": "رياضيات", "activity": "درس الجبر", "duration": "45 د", "status": "✅"},
        {"time": "10:00", "subject": "علوم", "activity": "تجربة الخلايا", "duration": "60 د", "status": "✅"},
        {"time": "14:00", "subject": "عربي", "activity": "مراجعة القواعد", "duration": "30 د", "status": "⏳"},
        {"time": "16:00", "subject": "رياضيات", "activity": "تمارين هندسة", "duration": "45 د", "status": "📅"},
    ]
    
    for activity in today_activities:
        col_a, col_b, col_c, col_d, col_e = st.columns([1, 2, 2, 1, 1])
        
        with col_a:
            st.markdown(f"**{activity['time']}**")
        
        with col_b:
            st.markdown(f"**{activity['subject']}**")
        
        with col_c:
            st.markdown(activity['activity'])
        
        with col_d:
            st.markdown(activity['duration'])
        
        with col_e:
            if activity['status'] == "✅":
                st.success(activity['status'])
            elif activity['status'] == "⏳":
                st.info(activity['status'])
            else:
                st.warning(activity['status'])
    
    # دروس موصى بها
    st.markdown("---")
    st.markdown("### 🎯 دروس موصى بها لك")
    
    lessons = get_lessons_database()
    
    # عرض دروس من مواد مختلفة
    col1, col2 = st.columns(2)
    
    with col1:
        if "رياضيات" in lessons:
            math_lesson = lessons["رياضيات"][0]
            with st.container():
                st.markdown(f"#### 🔢 {math_lesson['title']}")
                st.markdown(math_lesson['description'])
                st.markdown(f"**المستوى:** {math_lesson['level']}")
                if st.button("بدء الدرس", key="math_btn"):
                    interactive_lesson_view(math_lesson)
    
    with col2:
        if "علوم" in lessons:
            science_lesson = lessons["علوم"][0]
            with st.container():
                st.markdown(f"#### 🔬 {science_lesson['title']}")
                st.markdown(science_lesson['description'])
                st.markdown(f"**المستوى:** {science_lesson['level']}")
                if st.button("بدء الدرس", key="science_btn"):
                    interactive_lesson_view(science_lesson)

