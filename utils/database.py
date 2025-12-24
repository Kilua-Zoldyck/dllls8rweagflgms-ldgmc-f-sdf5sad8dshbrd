"""
utils/database.py - Database Connection & Operations
"""

import os
import psycopg2
import pandas as pd
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection_string = os.getenv('SUPABASE_URL')

    @st.cache_data(ttl=300)
    def get_products(_self):
        """جلب جميع المنتجات من قاعدة البيانات"""
        try:
            conn = psycopg2.connect(_self.connection_string)

            query = """
                SELECT
                    id,
                    product_id,
                    name,
                    url,
                    current_price,
                    old_price,
                    discount_percentage,
                    category,
                    image_url,
                    last_updated,
                    is_deleted,
                    is_out_of_stock,
                    is_hidden,
                    last_deep_check,
                    created_at
                FROM products
                ORDER BY last_updated DESC NULLS LAST
            """

            df = pd.read_sql(query, conn)
            conn.close()

            # تحويل الحالات إلى نص عربي
            def get_status(row):
                if row['is_deleted']:
                    return 'محذوف'
                elif row['is_out_of_stock']:
                    return 'نافد'
                elif row['is_hidden']:
                    return 'مخفي'
                else:
                    return 'متوفر'

            df['status'] = df.apply(get_status, axis=1)

            # تنسيق السعر
            df['price'] = df['current_price'].apply(lambda x: f"{x:.2f} ريال" if pd.notna(x) else "غير متاح")

            # إعادة تسمية الأعمدة
            df['last_checked'] = df['last_updated']

            return df

        except Exception as e:
            st.error(f"❌ خطأ في الاتصال بقاعدة البيانات: {str(e)}")
            return pd.DataFrame()

    def get_statistics(self):
        """حساب الإحصائيات"""
        df = self.get_products()

        if df.empty:
            return {
                'total': 0,
                'available': 0,
                'out_of_stock': 0,
                'hidden': 0,
                'deleted': 0,
                'categories': 0
            }

        stats = {
            'total': len(df),
            'available': len(df[df['status'] == 'متوفر']),
            'out_of_stock': len(df[df['status'] == 'نافد']),
            'hidden': len(df[df['status'] == 'مخفي']),
            'deleted': len(df[df['status'] == 'محذوف']),
            'categories': df['category'].nunique() if 'category' in df.columns else 0
        }

        return stats

    def get_categories(self):
        """جلب قائمة الأقسام"""
        df = self.get_products()
        if df.empty or 'category' not in df.columns:
            return []
        categories = df['category'].dropna().unique().tolist()
        return sorted(categories)

    def export_to_excel(self, df):
        """تصدير البيانات إلى Excel"""
        try:
            from io import BytesIO

            # اختيار الأعمدة المهمة للتصدير
            export_columns = [
                'product_id', 'name', 'current_price', 'old_price',
                'discount_percentage', 'category', 'status',
                'url', 'last_updated'
            ]

            # التأكد من وجود الأعمدة
            available_cols = [col for col in export_columns if col in df.columns]
            export_df = df[available_cols].copy()

            # تنسيق الأسماء بالعربي
            column_names = {
                'product_id': 'رقم المنتج',
                'name': 'اسم المنتج',
                'current_price': 'السعر الحالي',
                'old_price': 'السعر القديم',
                'discount_percentage': 'نسبة الخصم',
                'category': 'القسم',
                'status': 'الحالة',
                'url': 'الرابط',
                'last_updated': 'آخر تحديث'
            }

            export_df = export_df.rename(columns=column_names)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                export_df.to_excel(writer, index=False, sheet_name='Products')

            return output.getvalue()

        except Exception as e:
            st.error(f"❌ خطأ في التصدير: {str(e)}")
            return None
