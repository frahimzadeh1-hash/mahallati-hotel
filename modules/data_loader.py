import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data
def load_all_data():
    """بارگذاری همه داده‌ها با کش (برای سرعت بیشتر)"""
    try:
        guests = pd.read_csv('data/guests.csv', encoding='utf-8-sig')
        reservations = pd.read_csv('data/reservations.csv', encoding='utf-8-sig')
        events = pd.read_csv('data/events.csv', encoding='utf-8-sig')
        
        # تبدیل ستون‌های تاریخ به datetime
        reservations['check_in'] = pd.to_datetime(reservations['check_in'])
        reservations['check_out'] = pd.to_datetime(reservations['check_out'])
        events['date'] = pd.to_datetime(events['date'])
        
        return guests, reservations, events
    except FileNotFoundError:
        st.error("❌ فایل‌های داده پیدا نشد! لطفاً ابتدا داده‌های نمونه را بسازید.")
        st.info("برای ساخت داده‌های نمونه، فایل utils/helpers.py را اجرا کنید.")
        return None, None, None
    except Exception as e:
        st.error(f"❌ خطا در خواندن داده‌ها: {str(e)}")
        return None, None, None

def calculate_kpis(reservations_df):
    """محاسبه شاخص‌های کلیدی عملکرد (KPI)"""
    if reservations_df.empty:
        return {
            'total_reservations': 0,
            'completion_rate': 0,
            'cancellation_rate': 0,
            'adr': 0,
            'revenue': 0,
            'revpar': 0,
            'total_nights': 0,
            'no_show_rate': 0
        }
    
    total_reservations = len(reservations_df)
    completed = reservations_df[reservations_df['status'] == 'completed']
    cancelled = reservations_df[reservations_df['status'] == 'cancelled']
    no_show = reservations_df[reservations_df['status'] == 'no-show']
    
    # محاسبه شب‌های اقامت
    completed['nights'] = (completed['check_out'] - completed['check_in']).dt.days
    total_nights = completed['nights'].sum() if not completed.empty else 0
    
    # میانگین نرخ روزانه (ADR)
    adr = completed['price_per_night'].mean() if not completed.empty else 0
    
    # درآمد کل
    if not completed.empty:
        completed['total_price'] = completed['price_per_night'] * completed['nights']
        revenue = completed['total_price'].sum()
    else:
        revenue = 0
    
    # RevPAR (با فرض ۲۰ اتاق)
    total_rooms = 20
    days_in_period = 30  # میانگین ماهانه
    revpar = revenue / total_rooms / days_in_period if total_rooms > 0 else 0
    
    kpis = {
        'total_reservations': total_reservations,
        'completion_rate': (len(completed) / total_reservations * 100) if total_reservations > 0 else 0,
        'cancellation_rate': (len(cancelled) / total_reservations * 100) if total_reservations > 0 else 0,
        'no_show_rate': (len(no_show) / total_reservations * 100) if total_reservations > 0 else 0,
        'adr': adr,
        'revenue': revenue,
        'revpar': revpar,
        'total_nights': total_nights
    }
    return kpis

def filter_data_by_date(df, date_column, start_date, end_date):
    """فیلتر کردن داده‌ها بر اساس بازه زمانی"""
    mask = (df[date_column] >= pd.to_datetime(start_date)) & (df[date_column] <= pd.to_datetime(end_date))
    return df[mask]import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data
def load_all_data():
    """بارگذاری همه داده‌ها با کش (برای سرعت بیشتر)"""
    try:
        guests = pd.read_csv('data/guests.csv', encoding='utf-8-sig')
        reservations = pd.read_csv('data/reservations.csv', encoding='utf-8-sig')
        events = pd.read_csv('data/events.csv', encoding='utf-8-sig')
        
        # تبدیل ستون‌های تاریخ به datetime
        reservations['check_in'] = pd.to_datetime(reservations['check_in'])
        reservations['check_out'] = pd.to_datetime(reservations['check_out'])
        events['date'] = pd.to_datetime(events['date'])
        
        return guests, reservations, events
    except FileNotFoundError:
        st.error("❌ فایل‌های داده پیدا نشد! لطفاً ابتدا داده‌های نمونه را بسازید.")
        st.info("برای ساخت داده‌های نمونه، فایل utils/helpers.py را اجرا کنید.")
        return None, None, None
    except Exception as e:
        st.error(f"❌ خطا در خواندن داده‌ها: {str(e)}")
        return None, None, None

def calculate_kpis(reservations_df):
    """محاسبه شاخص‌های کلیدی عملکرد (KPI)"""
    if reservations_df.empty:
        return {
            'total_reservations': 0,
            'completion_rate': 0,
            'cancellation_rate': 0,
            'adr': 0,
            'revenue': 0,
            'revpar': 0,
            'total_nights': 0,
            'no_show_rate': 0
        }
    
    total_reservations = len(reservations_df)
    completed = reservations_df[reservations_df['status'] == 'completed']
    cancelled = reservations_df[reservations_df['status'] == 'cancelled']
    no_show = reservations_df[reservations_df['status'] == 'no-show']
    
    # محاسبه شب‌های اقامت
    completed['nights'] = (completed['check_out'] - completed['check_in']).dt.days
    total_nights = completed['nights'].sum() if not completed.empty else 0
    
    # میانگین نرخ روزانه (ADR)
    adr = completed['price_per_night'].mean() if not completed.empty else 0
    
    # درآمد کل
    if not completed.empty:
        completed['total_price'] = completed['price_per_night'] * completed['nights']
        revenue = completed['total_price'].sum()
    else:
        revenue = 0
    
    # RevPAR (با فرض ۲۰ اتاق)
    total_rooms = 20
    days_in_period = 30  # میانگین ماهانه
    revpar = revenue / total_rooms / days_in_period if total_rooms > 0 else 0
    
    kpis = {
        'total_reservations': total_reservations,
        'completion_rate': (len(completed) / total_reservations * 100) if total_reservations > 0 else 0,
        'cancellation_rate': (len(cancelled) / total_reservations * 100) if total_reservations > 0 else 0,
        'no_show_rate': (len(no_show) / total_reservations * 100) if total_reservations > 0 else 0,
        'adr': adr,
        'revenue': revenue,
        'revpar': revpar,
        'total_nights': total_nights
    }
    return kpis

def filter_data_by_date(df, date_column, start_date, end_date):
    """فیلتر کردن داده‌ها بر اساس بازه زمانی"""
    mask = (df[date_column] >= pd.to_datetime(start_date)) & (df[date_column] <= pd.to_datetime(end_date))
    return df[mask]
