"""
app.py - Streamlit Dashboard - Premium Edition
نظام مراقبة جنوبكو - لوحة التحكم الاحترافية
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# استيراد الوحدات المساعدة
from utils.auth import check_authentication, login_page, logout
from utils.database import Database
from utils.user_management import UserManager

# تحميل المتغيرات البيئية
load_dotenv()

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام مراقبة جنوبكو",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة الكائنات
db = Database()
user_mgr = UserManager()

# CSS مخصص
def load_custom_css():
    st.markdown("""
    <style>
    /* الخلفية الأساسية */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* المحتوى الرئيسي */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }

    /* العناوين */
    h1 {
        color: white !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 30px !important;
    }

    h2, h3 {
        color: white !important;
        font-weight: 700 !important;
        margin-top: 30px !important;
    }

        /* البطاقات الإحصائية */
    /* البطاقات الإحصائية */
    .metric-card {
        background: white;
        padding: 20px 15px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        text-align: center;
        transition: all 0.3s ease;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }

    .metric-value {
        font-size: 2.5em;
        font-weight: 800;
        margin: 10px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        word-break: break-word;
    }

    .metric-label {
        font-size: 0.95em;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
    }

    /* تحسين responsive للبطاقات */
    @media (max-width: 1400px) {
        .metric-value {
            font-size: 2em;
        }
        .metric-label {
            font-size: 0.85em;
        }
    }

    @media (max-width: 1200px) {
        .metric-value {
            font-size: 1.8em;
        }
        .metric-label {
            font-size: 0.8em;
        }
    }

    /* صندوق الفلاتر */
    .stSelectbox, .stTextInput {
        background: white;
        border-radius: 15px;
        padding: 5px;
    }

    /* الجدول */
    .dataframe {
        background: white !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
    }

    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(102,126,234,0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.98) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 5px 0 30px rgba(0,0,0,0.1) !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #333 !important;
    }

    /* صورة البروفايل */
    .profile-avatar-container {
        text-align: center;
        padding: 20px 0;
    }

    .profile-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 4px solid #667eea;
        box-shadow: 0 5px 20px rgba(102,126,234,0.3);
        object-fit: cover;
    }

    .profile-name {
        font-size: 1.3em;
        font-weight: 700;
        color: #333;
        margin: 15px 0 5px 0;
    }

    .profile-role {
        font-size: 0.95em;
        color: #667eea;
        font-weight: 600;
    }

    /* Radio buttons */
    [data-testid="stSidebar"] .stRadio > label {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 12px 20px;
        border-radius: 10px;
        margin: 5px 0;
        transition: all 0.3s ease;
        cursor: pointer;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stRadio > label:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateX(5px);
    }

    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 20px 0;
    }

    /* تنسيق Info boxes */
    .stAlert {
        background: white !important;
        border-radius: 15px !important;
        border-left: 5px solid #667eea !important;
        padding: 15px 20px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)
# دالة عرض صورة البروفايل
def display_avatar(username):
    """عرض صورة البروفايل"""
    avatar_path = user_mgr.get_avatar_path(username)

    if avatar_path and os.path.exists(avatar_path):
        st.image(avatar_path, width=120, use_container_width=False)
    else:
        # صورة افتراضية
        st.markdown(f"""
        <div style="width: 120px; height: 120px; border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex; align-items: center; justify-content: center;
                    margin: 20px auto; font-size: 3em; color: white; font-weight: bold;
                    border: 4px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            {username[0].upper()}
        </div>
        """, unsafe_allow_html=True)

# صفحة لوحة التحكم الرئيسية
def main_dashboard():
    """لوحة التحكم الرئيسية"""

    # العنوان
    st.title("📊 نظام مراقبة جنوبكو - لوحة التحكم")

    # جلب البيانات
    with st.spinner("🔄 جاري تحميل البيانات..."):
        products_df = db.get_products()
        stats = db.get_statistics()

    # عرض الإحصائيات
    st.subheader("📈 الإحصائيات العامة")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">إجمالي المنتجات</div>
            <div class="metric-value">{stats['total']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">✅ متوفر</div>
            <div class="metric-value" style="color: #10b981;">{stats['available']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🚫 نافد</div>
            <div class="metric-value" style="color: #f59e0b;">{stats['out_of_stock']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">👁️ مخفي</div>
            <div class="metric-value" style="color: #6366f1;">{stats['hidden']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🗑️ محذوف</div>
            <div class="metric-value" style="color: #ef4444;">{stats['deleted']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📁 الأقسام</div>
            <div class="metric-value" style="color: #8b5cf6;">{stats['categories']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # الفلاتر
    st.subheader("🔍 البحث والفلترة")

    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:
        status_filter = st.selectbox(
            "حالة المنتج",
            ["الكل", "متوفر", "نافد", "مخفي", "محذوف"]
        )

    with col2:
        categories = ["الكل"] + db.get_categories()
        category_filter = st.selectbox("القسم", categories)

    with col3:
        search_query = st.text_input("🔎 البحث بالاسم", placeholder="ابحث عن منتج...")

    # تطبيق الفلاتر
    filtered_df = products_df.copy()

    if status_filter != "الكل":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]

    if category_filter != "الكل":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]

    if search_query:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_query, case=False, na=False)]

        # عرض النتائج
        # عرض النتائج
        # عرض النتائج
    # عرض النتائج
    st.subheader(f"📋 المنتجات ({len(filtered_df)} منتج)")

    if not filtered_df.empty:
        # خيارات الترتيب
        col1, col2 = st.columns([3, 1])

        with col1:
            sort_by = st.selectbox(
                "ترتيب حسب",
                ["آخر فحص (الأحدث)", "السعر (الأعلى)", "السعر (الأقل)", "الاسم (أ-ي)", "الاسم (ي-أ)"]
            )

        # تطبيق الترتيب
        if sort_by == "آخر فحص (الأحدث)":
            filtered_df = filtered_df.sort_values('last_checked', ascending=False, na_position='last')
        elif sort_by == "السعر (الأعلى)":
            filtered_df = filtered_df.sort_values('current_price', ascending=False, na_position='last')
        elif sort_by == "السعر (الأقل)":
            filtered_df = filtered_df.sort_values('current_price', ascending=True, na_position='last')
        elif sort_by == "الاسم (أ-ي)":
            filtered_df = filtered_df.sort_values('name', ascending=True)
        elif sort_by == "الاسم (ي-أ)":
            filtered_df = filtered_df.sort_values('name', ascending=False)

        # تنسيق العرض مع الروابط
        display_df = filtered_df[['name', 'current_price', 'category', 'status', 'last_checked', 'url']].copy()

        # تحويل الاسم إلى رابط HTML
        display_df['name'] = display_df.apply(
            lambda row: f'<a href="{row["url"]}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600; display: block; padding: 5px 0;">{row["name"][:80]}{"..." if len(row["name"]) > 80 else ""}</a>',
            axis=1
        )

        # تنسيق السعر
        display_df['current_price'] = display_df['current_price'].apply(
            lambda x: f'<span style="color: #10b981; font-weight: 700; font-size: 1.1em;">{x:.2f} ر.س</span>' if pd.notna(x) else '<span style="color: #999;">غير متاح</span>'
        )

        # تنسيق الحالة
        status_colors = {
            'متوفر': '#10b981',
            'نافد': '#f59e0b',
            'مخفي': '#6366f1',
            'محذوف': '#ef4444'
        }

        display_df['status'] = display_df['status'].apply(
            lambda x: f'<span style="background: {status_colors.get(x, "#999")}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.85em; font-weight: 600; white-space: nowrap;">{x}</span>'
        )

        # تنسيق التاريخ
        display_df['last_checked'] = pd.to_datetime(display_df['last_checked']).dt.strftime('%Y-%m-%d<br>%H:%M')

        # إزالة عمود URL
        display_df = display_df.drop('url', axis=1)

        # تسميات الأعمدة
        display_df.columns = ['اسم المنتج', 'السعر', 'القسم', 'الحالة', 'آخر فحص']

        # عرض الجدول
        st.markdown(
            display_df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # CSS للجدول
        st.markdown("""
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            margin: 20px 0;
        }

        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            padding: 18px 15px;
            text-align: center;
            font-weight: 700;
            font-size: 1.05em;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        td {
            padding: 15px;
            border-bottom: 1px solid #f0f0f0;
            text-align: center;
            vertical-align: middle;
        }

        tr:hover {
            background: #f8f9fb;
            transition: all 0.2s ease;
        }

        tr:last-child td {
            border-bottom: none;
        }

        a:hover {
            color: #764ba2 !important;
            text-decoration: underline !important;
        }

        /* تحسين responsive */
        @media (max-width: 1400px) {
            th, td {
                padding: 12px 8px;
                font-size: 0.95em;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        # إضافة قسم تصدير البيانات (أسفل الجدول)
    user_role = st.session_state.get('user_data', {}).get('role')

    # التحقق من الصلاحيات: متاح للمدير والمدير الأساسي فقط
    if user_role in ['super_admin', 'admin']:
        st.divider()
        st.subheader("📥 تصدير البيانات")

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📊 تجهيز ملف Excel", use_container_width=True):
                with st.spinner("⏳ جاري إنشاء الملف..."):
                    excel_data = db.export_to_excel(filtered_df)
                    if excel_data:
                        st.download_button(
                            label="✅ اضغط هنا للتحميل",
                            data=excel_data,
                            file_name=f"janoubco_inventory_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
        with col2:
            st.info("💡 يمكنك تحميل النتائج المفلترة حالياً كملف Excel متوافق مع كافة الأنظمة.")
# صفحة إدارة المستخدمين
def users_management_page():
    """صفحة إدارة المستخدمين (Super Admin فقط)"""

    user_role = st.session_state.get('user_data', {}).get('role')

    if user_role != 'super_admin':
        st.error("🚫 ليس لديك صلاحية الوصول لهذه الصفحة")
        return

    st.title("👥 إدارة المستخدمين")

    # التبويبات
    tab1, tab2, tab3 = st.tabs(["📋 قائمة المستخدمين", "➕ إضافة مستخدم", "✏️ تعديل مستخدم"])

    # تبويب قائمة المستخدمين
    # تبويب قائمة المستخدمين
    # تبويب قائمة المستخدمين
    with tab1:
        st.subheader("قائمة المستخدمين الحالية")
        users = user_mgr.get_all_users()

        if users:
            for user in users:
                # ✅ 1. احسب المسمى الوظيفي هنا بره الـ f-string عشان تتجنب مشاكل الأقواس
                role_map = {"super_admin": "👑 مدير أساسي", "admin": "🔧 مدير", "viewer": "👀 مشاهد"}
                role_text = role_map.get(user['role'], user['role'])

                # ✅ 2. دلوقتي حط المتغير role_text جوه الـ Markdown بسهولة
                st.markdown(f"""
                <div style="background: white; padding: 20px; border-radius: 15px;
                            margin: 15px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                            display: flex; align-items: center; gap: 20px;">
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 style="margin: 0; color: #333; font-size: 1.3em;">{user['name']}</h3>
                                <p style="margin: 5px 0 0 0; color: #999; font-size: 0.95em;">@{user['username']}</p>
                            </div>
                            <div style="text-align: right;">
                                <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                            color: white; padding: 8px 20px; border-radius: 20px;
                                            font-weight: 600; font-size: 0.9em; display: inline-block;">
                                    {role_text}
                                </span>
                                <p style="margin: 8px 0 0 0; color: #667eea; font-size: 0.9em;">
                                    📧 {user['email'] if user['email'] else 'لا يوجد'}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # زر الحذف
                if user['role'] != 'super_admin':
                    col1, col2, col3 = st.columns([5, 1, 5])
                    with col2:
                        if st.button("🗑️ حذف", key=f"del_{user['username']}", use_container_width=True):
                            success, message = user_mgr.delete_user(user['username'])
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("لا يوجد مستخدمين")

    # تبويب إضافة مستخدم
    with tab2:
        st.subheader("إضافة مستخدم جديد")

        with st.form("add_user_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_username = st.text_input("اسم المستخدم *", placeholder="username")
                new_name = st.text_input("الاسم الكامل *", placeholder="محمد أحمد")
                new_email = st.text_input("البريد الإلكتروني", placeholder="email@example.com")

            with col2:
                new_password = st.text_input("كلمة المرور *", type="password")
                new_password_confirm = st.text_input("تأكيد كلمة المرور *", type="password")
                new_role = st.selectbox(
                    "الدور *",
                    ["admin", "viewer"],
                    format_func=lambda x: {"admin": "🔧 مدير", "viewer": "👀 مشاهد"}[x]
                )

            submitted = st.form_submit_button("➕ إضافة المستخدم", use_container_width=True)

            if submitted:
                if not all([new_username, new_name, new_password]):
                    st.error("❌ يرجى ملء جميع الحقول المطلوبة")
                elif new_password != new_password_confirm:
                    st.error("❌ كلمة المرور غير متطابقة")
                elif len(new_password) < 6:
                    st.error("❌ كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                else:
                    success, message = user_mgr.add_user(
                        new_username, new_password, new_name, new_role, new_email
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")

    # تبويب تعديل مستخدم
    with tab3:
        st.subheader("تعديل بيانات مستخدم")

        users = user_mgr.get_all_users()
        usernames = [u['username'] for u in users]

        selected_user = st.selectbox("اختر المستخدم", usernames)

        if selected_user:
            user_data = next((u for u in users if u['username'] == selected_user), None)

            if user_data:
                with st.form("edit_user_form"):
                    col1, col2 = st.columns(2)

                    with col1:
                        edit_name = st.text_input("الاسم الكامل", value=user_data['name'])
                        edit_email = st.text_input("البريد الإلكتروني", value=user_data['email'])

                    with col2:
                        edit_password = st.text_input("كلمة مرور جديدة (اختياري)", type="password")
                        if user_data['role'] != 'super_admin':
                            edit_role = st.selectbox(
                                "الدور",
                                ["admin", "viewer"],
                                index=0 if user_data['role'] == "admin" else 1,
                                format_func=lambda x: {"admin": "🔧 مدير", "viewer": "👀 مشاهد"}[x]
                            )
                        else:
                            st.info("👑 لا يمكن تغيير دور المدير الأساسي")
                            edit_role = "super_admin"

                    submitted = st.form_submit_button("💾 حفظ التعديلات", use_container_width=True)

                    if submitted:
                        update_data = {
                            'name': edit_name,
                            'email': edit_email,
                            'role': edit_role
                        }

                        if edit_password:
                            if len(edit_password) < 6:
                                st.error("❌ كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                            else:
                                update_data['password'] = edit_password

                        success, message = user_mgr.update_user(
                            selected_user,
                            current_user_role=st.session_state.get('user_data', {}).get('role'),
                            **update_data
                        )

                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")

# صفحة الملف الشخصي
def profile_page():
    """صفحة الملف الشخصي"""

    username = st.session_state.get('username')
    user_data = st.session_state.get('user_data', {})

    st.title("👤 الملف الشخصي")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 📸 صورة الملف الشخصي")

        # عرض الصورة الحالية
        display_avatar(username)

        # رفع صورة جديدة
        uploaded_file = st.file_uploader(
            "تحميل صورة جديدة",
            type=['jpg', 'jpeg', 'png'],
            help="الحد الأقصى: 5MB"
        )

        if uploaded_file:
            if st.button("💾 حفظ الصورة", use_container_width=True):
                success, message = user_mgr.upload_avatar(username, uploaded_file)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    with col2:
        st.markdown("### 📋 معلومات الحساب")

        # جدول المعلومات بتصميم احترافي
        role_text = {
            'super_admin': '👑 مدير أساسي',
            'admin': '🔧 مدير',
            'viewer': '👀 مشاهد'
        }

        st.markdown(f"""
        <div style="background: white; padding: 25px; border-radius: 15px;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.1);">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid #f0f0f0;">
                    <td style="padding: 15px; font-weight: 700; color: #667eea; width: 40%;">
                        📛 الاسم الكامل
                    </td>
                    <td style="padding: 15px; color: #333;">
                        {user_data.get('name', 'غير محدد')}
                    </td>
                </tr>
                <tr style="border-bottom: 2px solid #f0f0f0;">
                    <td style="padding: 15px; font-weight: 700; color: #667eea;">
                        👤 اسم المستخدم
                    </td>
                    <td style="padding: 15px; color: #333;">
                        @{username}
                    </td>
                </tr>
                <tr style="border-bottom: 2px solid #f0f0f0;">
                    <td style="padding: 15px; font-weight: 700; color: #667eea;">
                        🎭 الدور
                    </td>
                    <td style="padding: 15px;">
                        <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                     color: white; padding: 5px 15px; border-radius: 20px;
                                     font-weight: 600;">
                            {role_text.get(user_data.get('role'), 'غير محدد')}
                        </span>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 15px; font-weight: 700; color: #667eea;">
                        📧 البريد الإلكتروني
                    </td>
                    <td style="padding: 15px; color: #333;">
                        {user_data.get('email', 'غير محدد')}
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # تغيير كلمة المرور
        st.markdown("### 🔒 تغيير كلمة المرور")

        with st.form("change_password_form"):
            old_password = st.text_input("كلمة المرور الحالية", type="password")
            new_password = st.text_input("كلمة المرور الجديدة", type="password")
            new_password_confirm = st.text_input("تأكيد كلمة المرور الجديدة", type="password")

            submitted = st.form_submit_button("💾 تغيير كلمة المرور", use_container_width=True)

            if submitted:
                if not all([old_password, new_password, new_password_confirm]):
                    st.error("❌ يرجى ملء جميع الحقول")
                elif new_password != new_password_confirm:
                    st.error("❌ كلمة المرور الجديدة غير متطابقة")
                elif len(new_password) < 6:
                    st.error("❌ كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                else:
                    success, message = user_mgr.change_password(username, old_password, new_password)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

# الدالة الرئيسية
def main():
    """الدالة الرئيسية للتطبيق"""

    # تحميل CSS
    load_custom_css()

    # فحص المصادقة
    if not check_authentication():
        login_page()
        return

    # الشريط الجانبي
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)

        # معلومات المستخدم
        username = st.session_state.get('username')
        user_data = st.session_state.get('user_data', {})

        # صورة البروفايل
        display_avatar(username)

        st.markdown(f"<div class='profile-name'>{user_data.get('name', 'مستخدم')}</div>", unsafe_allow_html=True)

        role_text = {
            'super_admin': '👑 مدير أساسي',
            'admin': '🔧 مدير',
            'viewer': '👀 مشاهد'
        }
        st.markdown(f"<div class='profile-role'>{role_text.get(user_data.get('role'), '👤 مستخدم')}</div>", unsafe_allow_html=True)

        st.divider()

        # القائمة
        st.subheader("📋 القائمة")

        page = st.radio(
            "اختر الصفحة",
            ["📊 لوحة التحكم", "👤 الملف الشخصي"] +
            (["👥 إدارة المستخدمين"] if user_data.get('role') == 'super_admin' else []),
            label_visibility="collapsed"
        )

        st.divider()

        # معلومات النظام
        st.caption(f"🕐 آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # زر تسجيل الخروج
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            logout()
            st.rerun()

    # عرض الصفحة المحددة
    if page == "📊 لوحة التحكم":
        main_dashboard()
    elif page == "👤 الملف الشخصي":
        profile_page()
    elif page == "👥 إدارة المستخدمين":
        users_management_page()

if __name__ == "__main__":
    main()
