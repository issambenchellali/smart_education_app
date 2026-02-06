"""
المنصة التعليمية الذكية - النسخة البسيطة
تعمل بدون أي مكتبات خارجية على Streamlit Cloud
"""

import streamlit as st
import time

# ============================================
# إعدادات الصفحة
# ============================================
st.set_page_config(
    page_title="المنصة التعليمية الذكية",
    page_icon="🎓",
    layout="wide"
)

# ============================================
# CSS مخصص
# ============================================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        padding: 20px;
        font-size: 2.5rem;
        background: linear-gradient(90deg, #1E88E5, #4A00E0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-radius: 15px;
        padding: 25px;
        margin: 25px 0;
        text-align: center;
        border: 2px solid #28a745;
    }
    
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 5px solid #1E88E5;
    }
    
    .login-form {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# تهيئة الجلسة
# ============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# ============================================
# الصفحة الرئيسية (قبل التسجيل)
# ============================================
def home_page():
    """الصفحة الرئيسية"""
    
    # العنوان
    st.markdown('<h1 class="main-title">🎓 المنصة التعليمية الذكية</h1>', unsafe_allow_html=True)
    
    # رسالة نجاح
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ تم تشغيل المنصة بنجاح!")
    st.markdown(f"**الوقت:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # قسم المميزات
    st.markdown("---")
    st.subheader("✨ مميزات المنصة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("### 📚 تعليمي")
            st.markdown("• دروس تفاعلية")
            st.markdown("• شروحات فيديو")
            st.markdown("• كتب ومراجع")
    
    with col2:
        with st.container():
            st.markdown("### 🧠 ذكي")
            st.markdown("• تمارين تفاعلية")
            st.markdown("• تصحيح آلي")
            st.markdown("• تتبع التقدم")
    
    with col3:
        with st.container():
            st.markdown("### 👥 مجتمعي")
            st.markdown("• منتديات نقاش")
            st.markdown("• مسابقات")
            st.markdown("• شهادات")
    
    # تسجيل الدخول
    st.markdown("---")
    st.subheader("🔐 تسجيل الدخول للمنصة")
    
    with st.form("login_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("👤 اسم المستخدم")
            password = st.text_input("🔒 كلمة المرور", type="password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_btn = st.form_submit_button("🚀 دخول", type="primary", use_container_width=True)
            with col_btn2:
                guest_btn = st.form_submit_button("👀 تجربة كضيف", use_container_width=True)
            
            if login_btn:
                if username == "طالب" and password == "123456":
                    st.session_state.logged_in = True
                    st.session_state.user = "أحمد محمد"
                    st.session_state.role = "طالب"
                    st.success("✅ تم تسجيل الدخول بنجاح!")
                    time.sleep(1)
                    st.rerun()
                elif username == "معلم" and password == "123456":
                    st.session_state.logged_in = True
                    st.session_state.user = "د. علي حسين"
                    st.session_state.role = "معلم"
                    st.success("✅ تم تسجيل الدخول بنجاح!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ بيانات الدخول غير صحيحة")
            
            if guest_btn:
                st.session_state.logged_in = True
                st.session_state.user = "ضيف"
                st.session_state.role = "طالب"
                st.info("👋 مرحباً بك كضيف!")
                time.sleep(1)
                st.rerun()
        
        with col2:
            st.markdown("### 💡 حسابات تجريبية")
            st.markdown("""
            **للاختبار السريع:**
            
            **👨‍🎓 طالب:**
            - اسم المستخدم: `طالب`
            - كلمة المرور: `123456`
            
            **👨‍🏫 معلم:**
            - اسم المستخدم: `معلم`
            - كلمة المرور: `123456`
            
            **أو جرب:**
            - دخول كضيف بدون تسجيل
            """)

# ============================================
# لوحة الطالب
# ============================================
def student_dashboard():
    """لوحة تحكم الطالب"""
    
    # الشريط الجانبي
    with st.sidebar:
        st.markdown(f"# 👋 {st.session_state.user.split()[0]}")
        st.markdown(f"**الدور:** {st.session_state.role}")
        
        st.markdown("---")
        
        menu = st.radio(
            "القائمة",
            ["🏠 الرئيسية", "📚 الدروس", "🧠 التمارين", "📊 التقدم", "⚙️ الإعدادات"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
    
    # المحتوى الرئيسي
    if menu == "🏠 الرئيسية":
        student_home()
    elif menu == "📚 الدروس":
        student_lessons()
    elif menu == "🧠 التمارين":
        student_exercises()
    elif menu == "📊 التقدم":
        student_progress()
    elif menu == "⚙️ الإعدادات":
        student_settings()

def student_home():
    """الصفحة الرئيسية للطالب"""
    st.title("🏠 لوحة الطالب")
    
    # إحصائيات
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("الدروس المكتملة", "12", "+3")
    
    with col2:
        st.metric("التمارين المحلولة", "47", "+8")
    
    with col3:
        st.metric("مستوى التقدم", "75%", "+5%")
    
    # دروس اليوم
    st.markdown("---")
    st.subheader("🎯 دروس اليوم")
    
    lessons_today = [
        {"subject": "رياضيات", "title": "الجبر الأساسي", "time": "10:00 صباحاً", "status": "⏳"},
        {"subject": "علوم", "title": "الخلايا الحية", "time": "12:00 ظهراً", "status": "📅"},
        {"subject": "لغة عربية", "title": "القواعد النحوية", "time": "02:00 مساءً", "status": "📅"}
    ]
    
    for lesson in lessons_today:
        with st.container():
            col_a, col_b, col_c = st.columns([1, 3, 1])
            
            with col_a:
                st.markdown(f"**{lesson['subject']}**")
            
            with col_b:
                st.markdown(lesson['title'])
                st.markdown(f"⏰ {lesson['time']}")
            
            with col_c:
                if st.button("بدء", key=lesson['title']):
                    st.success(f"بدأت درس {lesson['title']}")
    
    # نشاط اليوم
    st.markdown("---")
    st.subheader("📝 نشاط اليوم")
    
    activities = [
        "✅ أكملت درس الرياضيات",
        "✅ حللت 5 تمارين",
        "⏳ قراءة درس العلوم",
        "📅 مراجعة اللغة العربية"
    ]
    
    for activity in activities:
        st.markdown(f"- {activity}")

def student_lessons():
    """صفحة الدروس"""
    st.title("📚 مكتبة الدروس")
    
    # فلترة الدروس
    subject = st.selectbox("اختر المادة", ["الكل", "رياضيات", "علوم", "لغة عربية", "فيزياء"])
    
    # عرض الدروس
    st.markdown("---")
    
    lessons_data = [
        {"id": 1, "title": "مقدمة في الجبر", "subject": "رياضيات", "duration": "45 دقيقة"},
        {"id": 2, "title": "الخلايا الحيوانية", "subject": "علوم", "duration": "60 دقيقة"},
        {"id": 3, "title": "القواعد النحوية", "subject": "لغة عربية", "duration": "30 دقيقة"},
        {"id": 4, "title": "قوانين نيوتن", "subject": "فيزياء", "duration": "50 دقيقة"}
    ]
    
    # تطبيق الفلتر
    if subject != "الكل":
        lessons_data = [l for l in lessons_data if l["subject"] == subject]
    
    for lesson in lessons_data:
        with st.expander(f"{lesson['title']} - {lesson['subject']}"):
            st.markdown(f"**المدة:** {lesson['duration']}")
            st.markdown("**الوصف:** درس تفاعلي مع أمثلة تطبيقية")
            
            if st.button(f"بدء دراسة {lesson['title']}", key=f"start_{lesson['id']}"):
                st.success(f"بدأت دراسة {lesson['title']}")
                
            if st.button(f"تمارين {lesson['title']}", key=f"ex_{lesson['id']}"):
                st.info(f"تمارين {lesson['title']} جاهزة")

def student_exercises():
    """صفحة التمارين"""
    st.title("🧠 التمارين الذكية")
    
    # نوع التمرين
    ex_type = st.radio("نوع التمرين", ["اختيار من متعدد", "صح وخطأ", "مقالي"])
    
    st.markdown("---")
    
    if ex_type == "اختيار من متعدد":
        st.markdown("### ما هو ناتج ٨ × ٩؟")
        
        options = ["٧٢", "٦٤", "٨١", "٥٦"]
        selected = st.radio("اختر الإجابة:", options)
        
        if st.button("تحقق من الإجابة"):
            if selected == "٧٢":
                st.success("✅ إجابة صحيحة! أحسنت")
                st.balloons()
            else:
                st.error("❌ إجابة خاطئة، حاول مرة أخرى")
    
    elif ex_type == "صح وخطأ":
        st.markdown("### الشمس تدور حول الأرض")
        
        answer = st.radio("هل هذه العبارة صحيحة؟", ["صح", "خطأ"])
        
        if st.button("تحقق"):
            if answer == "خطأ":
                st.success("✅ صحيح! الأرض هي التي تدور حول الشمس")
            else:
                st.error("❌ خطأ، الأرض تدور حول الشمس")
    
    elif ex_type == "مقالي":
        st.markdown("### ما هي فوائد الدراسة المنتظمة؟")
        
        answer = st.text_area("اكتب إجابتك هنا:", height=150)
        
        if st.button("📤 تسليم الإجابة"):
            if answer:
                st.success("✅ تم تسليم إجابتك بنجاح!")
                st.info("سيقوم المعلم بتصحيحها قريباً")
            else:
                st.warning("⚠️ يرجى كتابة إجابة قبل التسليم")

def student_progress():
    """صفحة التقدم"""
    st.title("📊 تتبع تقدمك")
    
    # مخطط بسيط
    st.subheader("📈 أداؤك في المواد")
    
    # إنشاء مخطط باستخدام HTML/CSS بسيط
    st.markdown("""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 100px; text-align: right; margin-right: 10px;">رياضيات:</div>
            <div style="flex-grow: 1;">
                <div style="background: #1E88E5; height: 20px; width: 85%; border-radius: 10px;"></div>
            </div>
            <div style="width: 50px; text-align: left; margin-left: 10px;">85%</div>
        </div>
        
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 100px; text-align: right; margin-right: 10px;">علوم:</div>
            <div style="flex-grow: 1;">
                <div style="background: #4CAF50; height: 20px; width: 70%; border-radius: 10px;"></div>
            </div>
            <div style="width: 50px; text-align: left; margin-left: 10px;">70%</div>
        </div>
        
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 100px; text-align: right; margin-right: 10px;">لغة عربية:</div>
            <div style="flex-grow: 1;">
                <div style="background: #FF9800; height: 20px; width: 90%; border-radius: 10px;"></div>
            </div>
            <div style="width: 50px; text-align: left; margin-left: 10px;">90%</div>
        </div>
        
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 100px; text-align: right; margin-right: 10px;">فيزياء:</div>
            <div style="flex-grow: 1;">
                <div style="background: #E91E63; height: 20px; width: 65%; border-radius: 10px;"></div>
            </div>
            <div style="width: 50px; text-align: left; margin-left: 10px;">65%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # توصيات
    st.markdown("---")
    st.subheader("💡 توصيات لتحسين أدائك")
    
    recommendations = [
        "🎯 **الرياضيات:** أداء ممتاز! واصل التقدم",
        "🔬 **العلوم:** جيد، ركز على التجارب العملية",
        "📖 **اللغة العربية:** ممتاز! حافظ على هذا المستوى",
        "⚛️ **الفيزياء:** تحتاج مزيداً من التركيز"
    ]
    
    for rec in recommendations:
        st.markdown(f"- {rec}")

def student_settings():
    """صفحة الإعدادات"""
    st.title("⚙️ إعدادات حسابك")
    
    with st.form("settings_form"):
        name = st.text_input("الاسم الكامل", value=st.session_state.user)
        email = st.text_input("البريد الإلكتروني", value="student@example.com")
        
        st.markdown("### 🔔 إعدادات الإشعارات")
        notifications = st.checkbox("تلقي إشعارات الدروس الجديدة", value=True)
        reminders = st.checkbox("تذكير بالمواعيد", value=True)
        
        if st.form_submit_button("💾 حفظ التغييرات"):
            st.success("✅ تم حفظ الإعدادات بنجاح!")
            st.session_state.user = name

# ============================================
# لوحة المعلم
# ============================================
def teacher_dashboard():
    """لوحة تحكم المعلم"""
    with st.sidebar:
        st.markdown(f"# 👨‍🏫 {st.session_state.user}")
        
        menu = st.radio(
            "القائمة",
            ["🏠 الرئيسية", "👨‍🎓 الطلاب", "📊 التقارير", "⚙️ الإعدادات"]
        )
        
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
    
    if menu == "🏠 الرئيسية":
        st.title("👨‍🏫 لوحة المعلم")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("عدد الطلاب", "25")
            st.metric("الدروس المرفوعة", "15")
        with col2:
            st.metric("التمارين المنشأة", "50")
            st.metric("متوسط النجاح", "78%")
    
    elif menu == "👨‍🎓 الطلاب":
        st.title("👨‍🎓 إدارة الطلاب")
        st.info("قائمة الطلاب المسجلين")

# ============================================
# الدالة الرئيسية
# ============================================
def main():
    """الدالة الرئيسية"""
    
    if not st.session_state.logged_in:
        home_page()
    else:
        if st.session_state.role == "طالب":
            student_dashboard()
        elif st.session_state.role == "معلم":
            teacher_dashboard()
        else:
            student_dashboard()  # الافتراضي للضيف

# ============================================
# تشغيل التطبيق
# ============================================
if __name__ == "__main__":
    main()
