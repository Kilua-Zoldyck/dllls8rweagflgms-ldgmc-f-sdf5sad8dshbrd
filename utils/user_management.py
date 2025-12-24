"""
utils/user_management.py - User Management System
"""

import json
import os
import hashlib
from datetime import datetime
import streamlit as st
from PIL import Image
import io

class UserManager:
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self.avatars_dir = 'data/avatars'

        # إنشاء المجلدات إذا لم تكن موجودة
        os.makedirs(os.path.dirname(users_file), exist_ok=True)
        os.makedirs(self.avatars_dir, exist_ok=True)

        # تهيئة ملف المستخدمين
        if not os.path.exists(users_file):
            self._create_default_users()

    def _create_default_users(self):
        """إنشاء المستخدمين الافتراضيين"""
        default_users = {
            "mohamed": {
                "password": self._hash_password("Mohamed@2024"),
                "name": "أستاذ محمد",
                "role": "super_admin",
                "email": "mohamed@janoubco.com",
                "created_at": datetime.now().isoformat(),
                "avatar": None
            },
            "youssef": {
                "password": self._hash_password("Youssef@2024"),
                "name": "م/ يوسف محمود",
                "role": "super_admin",
                "email": "youssef.mahmoudd@gmail.com",
                "created_at": datetime.now().isoformat(),
                "avatar": None
            }
        }
        self._save_users(default_users)

    def _hash_password(self, password):
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self):
        """تحميل المستخدمين من الملف"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def _save_users(self, users):
        """حفظ المستخدمين في الملف"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def authenticate(self, username, password):
        """التحقق من بيانات الدخول"""
        users = self._load_users()

        # البحث case-insensitive
        username_lower = username.lower()

        for stored_username, user_data in users.items():
            if stored_username.lower() == username_lower:
                if user_data['password'] == self._hash_password(password):
                    return {
                        'username': stored_username,
                        'name': user_data['name'],
                        'role': user_data['role'],
                        'email': user_data.get('email', ''),
                        'avatar': user_data.get('avatar')
                    }

        return None

    def add_user(self, username, password, name, role, email=''):
        """إضافة مستخدم جديد"""
        users = self._load_users()

        # التحقق من عدم وجود username مماثل (case-insensitive)
        username_lower = username.lower()
        for existing_username in users.keys():
            if existing_username.lower() == username_lower:
                return False, "اسم المستخدم موجود بالفعل"

        users[username] = {
            "password": self._hash_password(password),
            "name": name,
            "role": role,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "avatar": None
        }

        self._save_users(users)
        return True, "تم إضافة المستخدم بنجاح"

    def update_user(self, username, current_user_role='super_admin', **kwargs):
        """تحديث بيانات المستخدم"""
        users = self._load_users()

        if username not in users:
            return False, "المستخدم غير موجود"

        # منع تعديل Super Admin من Super Admin آخر
        if users[username]['role'] == 'super_admin' and current_user_role == 'super_admin':
            # السماح فقط بتعديل بياناته الشخصية
            allowed_fields = ['name', 'email', 'password', 'avatar']
            for key in list(kwargs.keys()):
                if key not in allowed_fields:
                    return False, "لا يمكن تعديل صلاحيات مدير أساسي آخر"

        for key, value in kwargs.items():
            if key == 'password' and value:
                users[username]['password'] = self._hash_password(value)
            elif key != 'password':
                users[username][key] = value

        self._save_users(users)
        return True, "تم تحديث البيانات بنجاح"

    def delete_user(self, username):
        """حذف مستخدم"""
        users = self._load_users()

        if username not in users:
            return False, "المستخدم غير موجود"

        if users[username]['role'] == 'super_admin':
            return False, "لا يمكن حذف المدير الأساسي"

        # حذف صورة البروفايل إذا كانت موجودة
        if users[username].get('avatar'):
            avatar_path = os.path.join(self.avatars_dir, users[username]['avatar'])
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        del users[username]
        self._save_users(users)
        return True, "تم حذف المستخدم بنجاح"

    def get_all_users(self):
        """جلب جميع المستخدمين"""
        users = self._load_users()
        users_list = []

        for username, data in users.items():
            users_list.append({
                'username': username,
                'name': data['name'],
                'role': data['role'],
                'email': data.get('email', ''),
                'created_at': data.get('created_at', ''),
                'avatar': data.get('avatar')
            })

        return users_list

    def upload_avatar(self, username, uploaded_file):
        """رفع صورة البروفايل"""
        users = self._load_users()

        if username not in users:
            return False, "المستخدم غير موجود"

        try:
            # معالجة الصورة
            image = Image.open(uploaded_file)

            # تحويل إلى RGB إذا كانت PNG
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # تصغير الصورة
            image.thumbnail((300, 300))

            # حفظ الصورة
            filename = f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            filepath = os.path.join(self.avatars_dir, filename)
            image.save(filepath, 'JPEG', quality=85)

            # حذف الصورة القديمة
            old_avatar = users[username].get('avatar')
            if old_avatar:
                old_path = os.path.join(self.avatars_dir, old_avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)

            # تحديث بيانات المستخدم
            users[username]['avatar'] = filename
            self._save_users(users)

            return True, "تم رفع الصورة بنجاح"

        except Exception as e:
            return False, f"خطأ في رفع الصورة: {str(e)}"

    def get_avatar_path(self, username):
        """الحصول على مسار صورة البروفايل"""
        users = self._load_users()

        if username in users and users[username].get('avatar'):
            return os.path.join(self.avatars_dir, users[username]['avatar'])

        return None

    def change_password(self, username, old_password, new_password):
        """تغيير كلمة المرور"""
        users = self._load_users()

        if username not in users:
            return False, "المستخدم غير موجود"

        if users[username]['password'] != self._hash_password(old_password):
            return False, "كلمة المرور القديمة غير صحيحة"

        users[username]['password'] = self._hash_password(new_password)
        self._save_users(users)

        return True, "تم تغيير كلمة المرور بنجاح"
