"""
utils/auth.py - Premium Authentication System
نظام تسجيل دخول احترافي بتصميم عصري
"""

import streamlit as st
from .user_management import UserManager
import base64

user_mgr = UserManager()

def get_logo_base64():
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "logo.png")
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

if logo_b64:
    st.markdown(f"""
    <div class="login-logo">
        <img src="data:image/png;base64,{logo_b64}"
             style="width: 100px; height: 100px; border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(102,126,234,0.4);">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="login-logo">
        <div class="login-logo-icon">📊</div>
    </div>
    """, unsafe_allow_html=True)

def check_authentication():
    """التحقق من حالة تسجيل الدخول"""
    return st.session_state.get('authenticated', False)

def login_page():
    """صفحة تسجيل الدخول - التصميم الاحترافي"""

    # CSS فخم جداً
    st.markdown("""
    <style>
    /* إخفاء عناصر Streamlit الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* الخلفية المتحركة */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* صندوق تسجيل الدخول */
    .login-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 50px 40px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-top: 10vh;
        animation: slideDown 0.5s ease;
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* الشعار */
    .login-logo {
        text-align: center;
        margin-bottom: 30px;
    }

    .login-logo-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5em;
        box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        animation: pulse 2s ease infinite;
    }

    @keyframes pulse {
        0%, 100% {transform: scale(1);}
        50% {transform: scale(1.05);}
    }

    /* العنوان */
    .login-title {
        text-align: center;
        font-size: 2em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0 10px 0;
        letter-spacing: -1px;
    }

    .login-subtitle {
        text-align: center;
        color: #666;
        font-size: 0.95em;
        margin-bottom: 35px;
        font-weight: 500;
    }

    /* حقول الإدخال */
    .stTextInput > div > div > input {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px 20px;
        font-size: 1em;
        transition: all 0.3s ease;
        background: #f8f9fa;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        background: white;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }

    /* زر تسجيل الدخول */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px;
        font-size: 1.1em;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
        margin-top: 10px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(102,126,234,0.4);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* رسالة الخطأ */
    .login-error {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        font-weight: 600;
        animation: shake 0.5s ease;
    }

    @keyframes shake {
        0%, 100% {transform: translateX(0);}
        25% {transform: translateX(-10px);}
        75% {transform: translateX(10px);}
    }

    /* Footer */
    .login-footer {
        text-align: center;
        margin-top: 30px;
        color: #999;
        font-size: 0.85em;
    }

    /* تخصيص Labels */
    .stTextInput > label {
        color: #333;
        font-weight: 600;
        font-size: 0.95em;
        margin-bottom: 8px;
    }

    /* إخفاء الأيقونة الافتراضية للباسورد */
    [data-testid="stPasswordInput"] button {
        color: #667eea !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # صندوق تسجيل الدخول
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # الشعار
    # الشعار
    st.markdown("""
    <div class="login-logo">
        <img src="https://i.imgur.com/YOUR_LOGO.png"
            style="width: 100px; height: 100px; border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(102,126,234,0.4);"
            onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div class="login-logo-icon" style="display: none;">📊</div>
    </div>
    """, unsafe_allow_html=True)

    # العنوان
    st.markdown('<h1 class="login-title">Janoubco Monitor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">نظام مراقبة متقدم للمنتجات</p>', unsafe_allow_html=True)

    # نموذج تسجيل الدخول
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "اسم المستخدم",
            placeholder="أدخل اسم المستخدم",
            key="username_input"
        )

        password = st.text_input(
            "كلمة المرور",
            type="password",
            placeholder="أدخل كلمة المرور",
            key="password_input"
        )

        submitted = st.form_submit_button("🚀 تسجيل الدخول")

        if submitted:
            if username and password:
                user_data = user_mgr.authenticate(username, password)

                if user_data:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.session_state['user_data'] = user_data
                    st.rerun()
                else:
                    st.markdown(
                        '<div class="login-error">❌ اسم المستخدم أو كلمة المرور غير صحيحة</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div class="login-error">⚠️ يرجى إدخال اسم المستخدم وكلمة المرور</div>',
                    unsafe_allow_html=True
                )

    # Footer
    st.markdown("""
    <div class="login-footer">
        🔒 جميع الحقوق محفوظة © 2024<br>
        <small>Powered by Streamlit</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """تسجيل الخروج"""
    for key in ['authenticated', 'username', 'user_data']:
        if key in st.session_state:
            del st.session_state[key]
