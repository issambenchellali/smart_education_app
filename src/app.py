"""
التطبيق الرئيسي - المنصة التعليمية الذكية
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# استيراد المكونات
from .config import config
from .supabase_manager import db_manager
from .ai_assistant import ai_assistant
from .session_manager import session_manager
from .curriculum_manager import curriculum_manager
from .exercise_manager import exercise_manager
from .analytics_manager import analytics_manager

# ============================================
# إعدادات الصفحة
# ============================================
st.set_page_config(
    page_title="المنصة التعليمية الذكية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS وأنماط التصميم
# ============================================
def load_css():
    """تحميل أنماط CSS"""
    st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1E88E5;
            padding: 20px;
            font-size: 3rem;
            font-weight: bold;
        }
        
        .card {
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E88E5;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# الصفحات
# ============================================
def show_login_page():
    """صفحة تسجيل الدخول"""
    st.markdown('<div class="main-title">🎓 المنصة التعليمية الذكية</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 إنشاء حساب"])
        
        with tab1:
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            
            if st.button("دخول", type="primary", use_container_width=True):
                if username and password:
                    user = db_manager.authenticate_user(username, password)
                    if user:
                        session_manager.login(user)
                        st.rerun()
                    else:
                        st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
                else:
                    st.warning("يرجى ملء جميع الحقول")
        
        with tab2:
            full_name = st.text_input("الاسم الكامل")
            email = st.text_input("البريد الإلكتروني")
            new_username = st.text_input("اسم المستخدم")
            new_password = st.text_input("كلمة المرور", type="password")
            
            if st.button("إنشاء حساب", type="primary", use_container_width=True):
                if all([full_name, email, new_username, new_password]):
                    user_data = {
                        "username": new_username,
                        "password": new_password,  # في الإنتاج استخدم التجزئة
                        "email": email,
                        "full_name": full_name,
                        "role": "طالب",
                        "grade": "العاشر",
                        "is_active": True
                    }
                    
                    result = db_manager.create_user(user_data)
                    if result:
                        st.success("تم إنشاء الحساب بنجاح!")
                    else:
                        st.error("حدث خطأ أثناء إنشاء الحساب")
                else:
                    st.warning("يرجى ملء جميع الحقول")
        
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

def show_dashboard():
    """لوحة التحكم الرئيسية"""
    # شريط التنقل
    col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)
    
    with col_nav1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    
    with col_nav2:
        if st.button("📚 المكتبة", use_container_width=True):
            st.session_state.current_page = "library"
            st.rerun()
    
    with col_nav3:
        if st.button("🤖 المساعد الذكي", use_container_width=True):
            st.session_state.current_page = "ai"
            st.rerun()
    
    with col_nav4:
        if st.button("📊 التقدم", use_container_width=True):
            st.session_state.current_page = "progress"
            st.rerun()
    
    with col_nav5:
        if st.button("🚪 خروج", use_container_width=True):
            session_manager.logout()
            st.rerun()
    
    # عرض الصفحة المحددة
    page = st.session_state.current_page
    
    if page == "home":
        show_home_page()
    elif page == "library":
        show_library_page()
    elif page == "ai":
        show_ai_page()
    elif page == "progress":
        show_progress_page()
    elif page == "lesson":
        show_lesson_page()

def show_home_page():
    """الصفحة الرئيسية"""
    st.markdown(f"## مرحباً {st.session_state.user_data.get('full_name', '')} 👋")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🚀 ابدأ رحلة التعلم اليوم!")
        
        # الدروس المقترحة
        lessons = curriculum_manager.get_lessons()[:3]
        for lesson in lessons:
            with st.expander(f"📖 {lesson['title']}"):
                st.write(f"**المادة:** {lesson['subject']}")
                st.write(f"**الصف:** {lesson['grade']}")
                st.write(lesson['description'][:200] + "...")
                
                if st.button("بدء الدرس", key=f"start_{lesson['id']}"):
                    st.session_state.current_lesson = lesson['id']
                    st.session_state.current_page = "lesson"
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # تقدم الطالب
        progress = analytics_manager.calculate_progress(
            st.session_state.user_data.get("id", "1")
        )
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 تقدمك التعليمي")
        st.metric("معدل الإنجاز", f"{progress['completion_rate']}%")
        st.metric("المعدل العام", f"{progress['average_score']}/100")
        st.metric("المستوى", progress['level'])
        st.markdown('</div>', unsafe_allow_html=True)

def show_library_page():
    """صفحة المكتبة"""
    st.markdown("## 📚 مكتبة الدروس")
    
    # التصفية
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject = st.selectbox("المادة", ["الكل"] + list(config.SUBJECTS.keys()))
    
    with col2:
        grade = st.selectbox("الصف", ["الكل"] + config.GRADES)
    
    with col3:
        search = st.text_input("🔍 البحث")
    
    # عرض الدروس
    filters = {}
    if subject != "الكل":
        filters["subject"] = subject
    if grade != "الكل":
        filters["grade"] = grade
    
    lessons = curriculum_manager.get_lessons(**filters)
    
    if search:
        lessons = [l for l in lessons if search.lower() in l['title'].lower()]
    
    for lesson in lessons:
        with st.container():
            col_lesson1, col_lesson2 = st.columns([3, 1])
            
            with col_lesson1:
                st.markdown(f"### {lesson['title']}")
                st.markdown(f"**{lesson['subject']} | الصف {lesson['grade']}**")
                st.markdown(f"{lesson['description'][:150]}...")
            
            with col_lesson2:
                if st.button("👀 عرض", key=f"view_{lesson['id']}", use_container_width=True):
                    st.session_state.current_lesson = lesson['id']
                    st.session_state.current_page = "lesson"
                    st.rerun()
            
            st.divider()

def show_lesson_page():
    """صفحة الدرس"""
    if not st.session_state.current_lesson:
        st.error("لم يتم تحديد درس")
        return
    
    lesson = curriculum_manager.get_lesson_detail(st.session_state.current_lesson)
    
    if not lesson:
        st.error("الدرس غير موجود")
        return
    
    st.markdown(f"# {lesson['title']}")
    st.markdown(f"**المادة:** {lesson['subject']} | **الصف:** {lesson['grade']}")
    
    tab1, tab2, tab3 = st.tabs(["📖 المحتوى", "🧪 التمارين", "🤖 شرح ذكي"])
    
    with tab1:
        st.markdown(lesson.get("content", "لا يوجد محتوى"))
        
        if st.button("✅ تم إكمال الدرس", type="primary"):
            if st.session_state.user_data:
                db_manager.update_progress(
                    st.session_state.user_data.get("id"),
                    lesson["id"],
                    {"completed": True, "score": 100}
                )
                st.success("تم تسجيل إكمال الدرس!")
    
    with tab2:
        exercises = exercise_manager.get_exercises_for_lesson(lesson['id'])
        
        if not exercises:
            st.info("لا توجد تمارين لهذا الدرس بعد")
        else:
            for i, exercise in enumerate(exercises, 1):
                st.markdown(f"**السؤال {i}:** {exercise['question']}")
                
                if exercise['exercise_type'] == 'mcq':
                    options = exercise.get('options', [])
                    selected = st.radio("اختر الإجابة:", options, key=f"ex_{i}")
                    
                    if st.button("تحقق", key=f"check_{i}"):
                        if selected == exercise['correct_answer']:
                            st.success("✅ إجابة صحيحة!")
                        else:
                            st.error(f"❌ الإجابة الصحيحة: {exercise['correct_answer']}")
                
                st.divider()
    
    with tab3:
        if ai_assistant:
            with st.spinner("جاري تحضير الشرح..."):
                explanation = ai_assistant.explain_lesson(
                    lesson['subject'],
                    lesson['topic'],
                    lesson['grade']
                )
                st.markdown(explanation)
        else:
            st.warning("خدمة الذكاء الاصطناعي غير متاحة حالياً")

def show_ai_page():
    """صفحة المساعد الذكي"""
    st.markdown("## 🤖 المساعد التعليمي الذكي")
    
    if not ai_assistant:
        st.warning("خدمة الذكاء الاصطناعي غير متاحة حالياً")
        return
    
    question = st.text_area("اطرح سؤالك التعليمي:", height=100)
    
    if st.button("🔄 الحصول على إجابة", type="primary"):
        if question:
            with st.spinner("جاري تحضير الإجابة..."):
                answer = ai_assistant.answer_question(question)
                st.markdown("### 💬 الإجابة:")
                st.markdown(answer)
                
                # حفظ في سجل المحادثة
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "time": datetime.now().strftime("%H:%M")
                })
        else:
            st.warning("يرجى كتابة سؤال")
    
    # سجل المحادثة
    if st.session_state.chat_history:
        st.markdown("### 📝 سجل المحادثة")
        for chat in st.session_state.chat_history[-5:]:
            with st.expander(f"سؤال: {chat['question'][:50]}..."):
                st.markdown(f"**الإجابة:** {chat['answer']}")
                st.caption(f"الوقت: {chat['time']}")

def show_progress_page():
    """صفحة التقدم"""
    st.markdown("## 📊 تقدمك التعليمي")
    
    if not st.session_state.user_data:
        return
    
    progress = analytics_manager.calculate_progress(
        st.session_state.user_data.get("id", "1")
    )
    
    # بطاقات الإحصائيات
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("معدل الإنجاز", f"{progress['completion_rate']}%")
    
    with col2:
        st.metric("المعدل العام", f"{progress['average_score']}/100")
    
    with col3:
        st.metric("الدروس المكتملة", f"{progress['completed_lessons']}/{progress['total_lessons']}")
    
    with col4:
        st.metric("المستوى", progress['level'])
    
    # مخطط التقدم
    st.markdown("### 📈 تقدمك عبر الزمن")
    
    # بيانات نموذجية
    chart_data = pd.DataFrame({
        "الأسبوع": ["1", "2", "3", "4"],
        "الدرجات": [65, 72, 78, 85],
        "الإنجاز": [40, 55, 65, 78]
    })
    
    st.line_chart(chart_data.set_index("الأسبوع"))
    
    # خطة التعلم
    st.markdown("### 🗓️ خطة التعلم المقترحة")
    learning_plan = analytics_manager.generate_learning_plan(progress)
    st.markdown(learning_plan)

# ============================================
# التطبيق الرئيسي
# ============================================
def main():
    """الدالة الرئيسية"""
    # تحميل الأنماط
    load_css()
    
    # التحقق من حالة تسجيل الدخول
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_dashboard()
    
    # تذييل الصفحة
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🎓 المنصة التعليمية الذكية المتكاملة - إصدار 1.0</p>
        <p>© 2024 جميع الحقوق محفوظة</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
