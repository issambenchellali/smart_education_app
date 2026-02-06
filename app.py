"""
المنصة التعليمية الذكية - النسخة المؤكدة للعمل
"""

import streamlit as st
import time

# ==============================
# 1. إعدادات الصفحة الأساسية
# ==============================
st.set_page_config(
    page_title="المنصة التعليمية الذكية",
    page_icon="🎓",
    layout="wide"
)

# ==============================
# 2. CSS بسيط
# ==============================
st.markdown("""
<style>
    /* العنوان الرئيسي */
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 2.5rem;
        margin: 20px 0;
    }
    
    /* بطاقات */
    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 3. تهيئة الجلسة
# ==============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# ==============================
# 4. الصفحة الرئيسية
# ==============================
def main_page():
    """الصفحة الرئيسية"""
    
    # العنوان
    st.markdown('<h1 class="main-title">🎓 المنصة التعليمية الذكية</h1>', unsafe_allow_html=True)
    
    # رسالة نجاح
    st.success("✅ تم تشغيل المنصة بنجاح!")
    st.info(f"الوقت: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # قسم تسجيل الدخول
    st.markdown("---")
    st.subheader("🔐 تسجيل الدخول")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        
        if st.button("🚀 دخول", type="primary"):
            if username == "طالب" and password == "123456":
                st.session_state.logged_in = True
                st.session_state.user = "أحمد محمد"
                st.session_state.role = "طالب"
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("بيانات غير صحيحة")
    
    with col2:
        st.info("""
        **💡 حسابات تجريبية:**
        
        **👨‍🎓 طالب:**
        - المستخدم: `طالب`
        - كلمة المرور: `123456`
        
        **👨‍🏫 معلم:**
        - المستخدم: `معلم`
        - كلمة المرور: `123456`
        """)
    
    # مميزات المنصة
    st.markdown("---")
    st.subheader("✨ مميزات المنصة")
    
    features = [
        "📚 دروس تفاعلية في جميع المواد",
        "🧠 تمارين ذكية مع تصحيح آلي",
        "📊 تتبع التقدم الدراسي",
        "👨‍🏫 متابعة من المعلمين",
        "📱 تعمل على جميع الأجهزة"
    ]
    
    for feature in features:
        st.write(f"• {feature}")

# ==============================
# 5. لوحة الطالب
# ==============================
def student_dashboard():
    """لوحة تحكم الطالب"""
    
    with st.sidebar:
        st.title(f"👋 {st.session_state.user}")
        st.write(f"**الدور:** {st.session_state.role}")
        
        menu = st.radio(
            "القائمة",
            ["🏠 الرئيسية", "📚 الدروس", "🧠 التمارين", "📊 تقدمي"]
        )
        
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
    
    if menu == "🏠 الرئيسية":
        st.title("🏠 لوحة الطالب")
        
        # إحصائيات
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("الدروس", "12")
        with col2:
            st.metric("التمارين", "47")
        with col3:
            st.metric("التقدم", "75%")
    
    elif menu == "📚 الدروس":
        st.title("📚 الدروس المتاحة")
        
        lessons = [
            {"title": "مقدمة في الجبر", "subject": "رياضيات"},
            {"title": "قوانين نيوتن", "subject": "فيزياء"},
            {"title": "القواعد النحوية", "subject": "لغة عربية"}
        ]
        
        for lesson in lessons:
            with st.expander(f"{lesson['title']} - {lesson['subject']}"):
                st.write("وصف الدرس هنا...")
                if st.button(f"بدء {lesson['title']}"):
                    st.success(f"بدأت درس {lesson['title']}")
    
    elif menu == "🧠 التمارين":
        st.title("🧠 التمارين التعليمية")
        
        st.write("**ما هو ٧ × ٨؟**")
        answer = st.number_input("الإجابة", min_value=0, max_value=100)
        
        if st.button("تحقق"):
            if answer == 56:
                st.success("✅ إجابة صحيحة!")
            else:
                st.error("❌ حاول مرة أخرى")
    
    elif menu == "📊 تقدمي":
        st.title("📊 تقدمي الدراسي")
        
        st.write("**أداؤك في المواد:**")
        st.write("- رياضيات: 85%")
        st.write("- علوم: 70%")
        st.write("- لغة عربية: 90%")

# ==============================
# 6. الدالة الرئيسية
# ==============================
def main():
    """الدالة الرئيسية"""
    
    if not st.session_state.logged_in:
        main_page()
    else:
        if st.session_state.role == "طالب":
            student_dashboard()
        else:
            st.title("👨‍🏫 لوحة المعلم")
            st.info("لوحة المعلم قيد التطوير")

# ==============================
# 7. تشغيل التطبيق
# ==============================
if __name__ == "__main__":
    main()
