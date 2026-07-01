import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
import jdatetime
from sklearn.linear_model import LinearRegression
import numpy as np
import requests

# ============================================
# تنظیمات صفحه - فقط یک بار و در ابتدا
# ============================================
st.set_page_config(
    page_title="🏨 بوتیک هتل محلاتی - داشبورد مدیریت",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# تنظیمات هویتی هتل
# ============================================
HOTEL_CONFIG = {
    "name": "بوتیک هتل محلاتی",
    "logo_url": "https://www.hotelmahalati.com/images/logo.png",
    "rooms": [
        {"name": "ترنج", "price": 8500000},
        {"name": "پریدخت", "price": 9112000},
        {"name": "پریچهر", "price": 9112000},
        {"name": "دلکش و دلربا", "price": 9112000},
        {"name": "گلدان و گلرخ", "price": 9112000},
        {"name": "شاهدخت", "price": 13427000},
        {"name": "شازده", "price": 12000000},
        {"name": "شاه نشین", "price": 15000000},
        {"name": "آینه", "price": 14093000},
        {"name": "دنج", "price": 3876000}
    ],
    "colors": {
        "primary": "#0B7A75",
        "secondary": "#14A085",
        "accent": "#F4A460",
        "background": "#F0F7F4",
        "text": "#1A2E2A"
    },
    "event_categories": ["موسیقی", "شعر", "هنرهای تجسمی", "تاریخ و معماری", "خوشنویسی"]
}

# ============================================
# توابع تاریخ و مناسبت‌ها
# ============================================

def get_persian_date():
    """گرفتن تاریخ شمسی، میلادی و قمری"""
    now = datetime.now()
    persian = jdatetime.datetime.fromgregorian(date=now)
    
    days = ['شنبه', 'یک‌شنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']
    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 
              'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    
    return {
        'jalali': f"{days[persian.weekday()]} {persian.day} {months[persian.month-1]} {persian.year}",
        'gregorian': now.strftime("%A, %B %d, %Y"),
        'hijri': get_hijri_date(now),
        'event': get_event_of_day()
    }

def get_hijri_date(date_obj):
    """گرفتن تاریخ قمری با API"""
    try:
        url = f"https://api.aladhan.com/v1/gToH/{date_obj.year}/{date_obj.month}/{date_obj.day}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                hijri = data['data']['hijri']
                return f"{hijri['day']} {hijri['month']['en']} {hijri['year']} هجری قمری"
    except:
        pass
    return "تاریخ قمری در دسترس نیست"

def get_event_of_day():
    """گرفتن مناسبت روز با API"""
    try:
        url = "https://api.parsijoo.ir/events/today"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and 'events' in data:
                events = data['events']
                return " - ".join(events[:2])
    except:
        pass
    return get_fallback_event()

def get_fallback_event():
    """مناسبت‌های ثابت در صورت عدم دسترسی به API"""
    now = datetime.now()
    persian = jdatetime.datetime.fromgregorian(date=now)
    month = persian.month
    day = persian.day
    
    events = {
        (1, 1): "🎉 جشن نوروز",
        (1, 13): "🌿 روز طبیعت",
        (2, 25): "📚 روز فردوسی",
        (3, 1): "🌾 روز خرداد",
        (4, 14): "🌸 تولد امام رضا (ع)",
        (6, 21): "📜 روز شعر و ادب فارسی",
        (7, 7): "🍷 تولد حافظ",
        (10, 15): "📖 روز سعدی"
    }
    
    for (m, d), event in events.items():
        if m == month and d == day:
            return event
    
    if persian.weekday() == 6:
        return "🕌 روز جمعه"
    
    return ""

# ============================================
# توابع کمکی
# ============================================

def to_persian_number(num):
    """تبدیل اعداد انگلیسی به فارسی"""
    if num is None or num == '' or num != num:
        return '۰'
    persian_digits = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
                      '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    try:
        result = ''
        for ch in str(int(num)):
            result += persian_digits.get(ch, ch)
        return result
    except (ValueError, TypeError):
        return str(num)

def to_persian_date(date_obj):
    """تبدیل تاریخ میلادی به شمسی"""
    if date_obj is None or date_obj == '' or date_obj != date_obj:
        return ''
    try:
        if isinstance(date_obj, str):
            date_obj = pd.to_datetime(date_obj)
        persian_date = jdatetime.datetime.fromgregorian(datetime=date_obj)
        return f"{to_persian_number(persian_date.year)}/{to_persian_number(persian_date.month)}/{to_persian_number(persian_date.day)}"
    except:
        return str(date_obj)

def format_price_persian(price):
    """فرمت قیمت به تومان با اعداد فارسی"""
    if price is None or price == '' or price != price:
        return '۰ تومان'
    try:
        price_int = int(float(price))
        return f"{to_persian_number(price_int):,} تومان"
    except (ValueError, TypeError):
        return str(price)

# ============================================
# دریافت تاریخ و نمایش هدر
# ============================================

date_info = get_persian_date()
jalali_date = date_info['jalali']
gregorian_date = date_info['gregorian']
hijri_date = date_info['hijri']
event_of_day = date_info['event']

# اعمال استایل
st.markdown(f"""
<style>
    .stApp {{
        background-color: {HOTEL_CONFIG['colors']['background']};
        direction: rtl;
        font-family: 'Vazir', sans-serif;
    }}
    .custom-header {{
        background: linear-gradient(135deg, {HOTEL_CONFIG['colors']['primary']}, {HOTEL_CONFIG['colors']['secondary']});
        padding: 18px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-right: 6px solid {HOTEL_CONFIG['colors']['accent']};
    }}
    .custom-header .title-section h1 {{
        color: white;
        margin: 0;
        font-size: 26px;
        font-weight: bold;
    }}
    .custom-header .title-section p {{
        color: rgba(255,255,255,0.85);
        margin: 5px 0 0 0;
        font-size: 14px;
    }}
    .custom-header .date-section {{
        text-align: left;
        font-size: 13px;
        color: rgba(255,255,255,0.95);
        line-height: 1.8;
        background: rgba(0,0,0,0.15);
        padding: 8px 15px;
        border-radius: 8px;
        min-width: 200px;
    }}
    .custom-header .date-section .event {{
        color: {HOTEL_CONFIG['colors']['accent']};
        font-weight: bold;
        font-size: 14px;
    }}
    .stMetric {{
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-right: 4px solid {HOTEL_CONFIG['colors']['accent']};
    }}
    .stMetric label {{
        color: {HOTEL_CONFIG['colors']['text']} !important;
        font-weight: bold;
    }}
    .stMetric div {{
        color: {HOTEL_CONFIG['colors']['primary']} !important;
        font-size: 28px !important;
        font-weight: bold;
    }}
    .stButton>button {{
        background: {HOTEL_CONFIG['colors']['secondary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: {HOTEL_CONFIG['colors']['primary']};
        transform: scale(1.03);
        box-shadow: 0 4px 12px rgba(11,122,117,0.3);
    }}
    .prediction-box {{
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #2E7D32;
        margin: 15px 0;
        text-align: center;
    }}
    .prediction-box h3 {{
        color: #1B5E20;
        margin: 0;
    }}
    .prediction-box .number {{
        font-size: 32px;
        font-weight: bold;
        color: #0B7A75;
    }}
    .sidebar-logo {{
        text-align: center;
        padding: 15px 0;
        background: linear-gradient(135deg, {HOTEL_CONFIG['colors']['primary']}, {HOTEL_CONFIG['colors']['secondary']});
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    .sidebar-logo img {{
        height: 70px;
        border-radius: 10px;
        background: white;
        padding: 5px;
    }}
</style>
""", unsafe_allow_html=True)

# نمایش هدر
st.markdown(f"""
<div class="custom-header">
    <div class="title-section">
        <h1>🏛️ داشبورد حرفه‌ای مدیریت بوتیک هتل محلاتی شیراز</h1>
        <p>سیستم مدیریت هوشمند اقامتگاه</p>
    </div>
    <div class="date-section">
        <div>📅 {jalali_date}</div>
        <div style="font-size: 11px; opacity: 0.8;">{gregorian_date}</div>
        <div style="font-size: 11px; opacity: 0.8;">{hijri_date}</div>
        {f'<div class="event">🎉 {event_of_day}</div>' if event_of_day else ''}
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# توابع تولید و بارگذاری داده
# ============================================

def generate_realistic_data():
    """تولید داده‌های نمونه"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    first_names = ['احمد', 'سارا', 'محمد', 'زهرا', 'علی', 'مریم', 'رضا', 'فاطمه', 
                   'حسین', 'نگار', 'کیان', 'نازنین', 'امیر', 'سپیده', 'مهدی', 'الهه']
    last_names = ['محلاتی', 'کریمی', 'حسینی', 'رضوی', 'نوری', 'یزدی', 'شیرازی', 
                  'کاشانی', 'اصفهانی', 'تبریزی', 'فردوسی', 'سهرابی']
    cities = ['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان', 'کرمان']
    art_preferences = ['نقاشی', 'معماری', 'شعر', 'موسیقی', 'تاریخ', 'خوشنویسی', 'مینیاتور']
    channels = ['وب‌سایت', 'بوکینگ', 'اینستاگرام', 'تلفن', 'حضوری']
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # مهمانان
    guests = []
    for i in range(300):
        guest = {
            'guest_id': f'G{1000+i}',
            'نام': random.choice(first_names),
            'نام_خانوادگی': random.choice(last_names),
            'شماره_تماس': f'0912{random.randint(1000000, 9999999)}',
            'شهر': random.choice(cities),
            'تاریخ_اولین_اقامت': random.choice(date_range).strftime('%Y-%m-%d'),
            'تعداد_اقامت': random.randint(1, 10),
            'علاقه_هنری': random.choice(art_preferences),
            'امتیاز_وفاداری': round(random.uniform(0, 100), 1)
        }
        guests.append(guest)
    guests_df = pd.DataFrame(guests)
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    
    # رزروها
    reservations = []
    room_names = [room['name'] for room in HOTEL_CONFIG['rooms']]
    for i in range(800):
        check_in = random.choice(date_range)
        stay_days = random.randint(1, 4)
        check_out = check_in + timedelta(days=stay_days)
        room = random.choice(room_names)
        price = next((r['price'] for r in HOTEL_CONFIG['rooms'] if r['name'] == room), 5000000)
        
        reservation = {
            'شناسه_رزرو': f'R{10000+i}',
            'شناسه_مهمان': f'G{random.randint(1000, 1299)}',
            'تاریخ_ورود': check_in.strftime('%Y-%m-%d'),
            'تاریخ_خروج': check_out.strftime('%Y-%m-%d'),
            'اتاق': room,
            'قیمت_هر_شب': price,
            'کانال': random.choice(channels),
            'وضعیت': random.choices(['تکمیل‌شده', 'لغو‌شده', 'عدم_حضور'], weights=[0.7, 0.2, 0.1])[0]
        }
        reservations.append(reservation)
    reservations_df = pd.DataFrame(reservations)
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    
    # ایونت‌ها
    events = []
    event_templates = [
        ('شب شعر حافظ و سعدی', 'شعر', 35, 18),
        ('کنسرت سه‌تار و نی', 'موسیقی', 45, 22),
        ('نمایشگاه نقاشی قاجار', 'هنرهای تجسمی', 50, 28),
        ('کارگاه خوشنویسی با قلم نی', 'خوشنویسی', 20, 12),
        ('سخنرانی تاریخ زندیه', 'تاریخ و معماری', 40, 18),
        ('شب موسیقی سنتی', 'موسیقی', 50, 25),
        ('تور معماری و کاشی‌کاری', 'تاریخ و معماری', 25, 10),
        ('کارگاه نقاشی روی سفال', 'هنرهای تجسمی', 30, 15)
    ]
    
    for i in range(40):
        event_date = random.choice(date_range)
        template = random.choice(event_templates)
        event = {
            'شناسه_ایونت': f'E{2000+i}',
            'نام_ایونت': template[0],
            'تاریخ': event_date.strftime('%Y-%m-%d'),
            'ظرفیت': template[2] + random.randint(-5, 10),
            'ثبت_نام': template[3] + random.randint(-5, 15),
            'قیمت': random.randint(30, 150) * 10000,
            'دسته_بندی': template[1]
        }
        events.append(event)
    events_df = pd.DataFrame(events)
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')
    
    return guests_df, reservations_df, events_df

def load_data():
    try:
        guests = pd.read_csv('data/guests.csv', encoding='utf-8-sig')
        reservations = pd.read_csv('data/reservations.csv', encoding='utf-8-sig')
        events = pd.read_csv('data/events.csv', encoding='utf-8-sig')
        reservations['تاریخ_ورود'] = pd.to_datetime(reservations['تاریخ_ورود'])
        reservations['تاریخ_خروج'] = pd.to_datetime(reservations['تاریخ_خروج'])
        events['تاریخ'] = pd.to_datetime(events['تاریخ'])
        return guests, reservations, events
    except Exception as e:
        return None, None, None

def save_data(guests_df, reservations_df, events_df):
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')

# ============================================
# توابع پیش‌بینی
# ============================================

def predict_occupancy(reservations_df, days_ahead=30):
    if reservations_df.empty:
        return None
    completed = reservations_df[reservations_df['وضعیت'] == 'تکمیل‌شده'].copy()
    if completed.empty:
        return None
    completed['تاریخ_ورود'] = pd.to_datetime(completed['تاریخ_ورود'])
    daily_occupancy = completed.groupby('تاریخ_ورود').size().reset_index()
    daily_occupancy.columns = ['تاریخ', 'تعداد']
    days = np.array(range(len(daily_occupancy))).reshape(-1, 1)
    y = daily_occupancy['تعداد'].values
    try:
        model = LinearRegression()
        model.fit(days, y)
        last_day = len(daily_occupancy)
        future_days = np.array(range(last_day, last_day + days_ahead)).reshape(-1, 1)
        predictions = model.predict(future_days)
        predictions = np.maximum(predictions, 0)
        predictions = np.minimum(predictions, 10)
        last_date = daily_occupancy['تاریخ'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(days_ahead)]
        avg_prediction = np.mean(predictions)
        avg_adr = completed['قیمت_هر_شب'].mean()
        predicted_revenue = avg_prediction * avg_adr * 30
        return {
            'avg_occupancy': avg_prediction,
            'predicted_revenue': predicted_revenue,
            'trend': 'صعودی' if predictions[-1] > predictions[0] else 'نزولی',
            'future_dates': future_dates,
            'predictions': predictions,
            'daily_occupancy': daily_occupancy
        }
    except:
        return None

def predict_guest_growth(guests_df, months_ahead=3):
    if guests_df.empty:
        return None
    guests_df_copy = guests_df.copy()
    guests_df_copy['تاریخ_اولین_اقامت'] = pd.to_datetime(guests_df_copy['تاریخ_اولین_اقامت'])
    monthly_new = guests_df_copy.groupby(guests_df_copy['تاریخ_اولین_اقامت'].dt.to_period('M')).size().reset_index()
    monthly_new.columns = ['ماه', 'تعداد']
    if len(monthly_new) < 3:
        return None
    X = np.array(range(len(monthly_new))).reshape(-1, 1)
    y = monthly_new['تعداد'].values
    try:
        model = LinearRegression()
        model.fit(X, y)
        last_idx = len(monthly_new)
        future_idx = np.array(range(last_idx, last_idx + months_ahead)).reshape(-1, 1)
        predictions = model.predict(future_idx)
        predictions = np.maximum(predictions, 0)
        return {
            'avg_monthly_growth': np.mean(predictions),
            'total_new_guests': int(np.sum(predictions)),
            'trend': 'صعودی' if predictions[-1] > predictions[0] else 'نزولی'
        }
    except:
        return None

def predict_events_success(events_df):
    if events_df.empty:
        return None
    events_copy = events_df.copy()
    events_copy['درصد_پر_شدن'] = (events_copy['ثبت_نام'] / events_copy['ظرفیت']) * 100
    avg_success = events_copy['درصد_پر_شدن'].mean()
    best_category = events_copy.groupby('دسته_بندی')['درصد_پر_شدن'].mean().idxmax()
    return {
        'avg_success_rate': avg_success,
        'best_category': best_category,
        'recommendation': f'برگزاری ایونت‌های {best_category} با استقبال بیشتری همراه است'
    }

# ============================================
# توابع محاسباتی و نمودارها
# ============================================

def calculate_kpis(guests_df, reservations_df, events_df):
    total_guests = len(guests_df)
    total_rooms = len(HOTEL_CONFIG['rooms'])
    completed = reservations_df[reservations_df['وضعیت'] == 'تکمیل‌شده']
    cancelled = reservations_df[reservations_df['وضعیت'] == 'لغو‌شده']
    last_30_days = datetime.now() - timedelta(days=30)
    recent_completed = completed[completed['تاریخ_ورود'] >= last_30_days]
    occupancy = (len(recent_completed) / (30 * total_rooms)) * 100 if total_rooms > 0 else 0
    adr = completed['قیمت_هر_شب'].mean() if not completed.empty else 0
    revenue = 0
    if not completed.empty:
        completed['شب‌ها'] = (completed['تاریخ_خروج'] - completed['تاریخ_ورود']).dt.days
        revenue = (completed['قیمت_هر_شب'] * completed['شب‌ها']).sum()
    popular_room = completed['اتاق'].mode()[0] if not completed.empty and not completed['اتاق'].empty else 'نامشخص'
    popular_art = guests_df['علاقه_هنری'].mode()[0] if 'علاقه_هنری' in guests_df.columns and not guests_df.empty else 'نامشخص'
    return {
        'total_guests': total_guests,
        'occupancy': occupancy,
        'adr': adr,
        'revenue': revenue,
        'popular_room': popular_room,
        'popular_art': popular_art,
        'cancellation_rate': (len(cancelled) / len(reservations_df) * 100) if len(reservations_df) > 0 else 0
    }

def plot_loyalty_segmentation(guests_df):
    if guests_df.empty:
        return px.pie(title='داده‌ای وجود ندارد')
    bins = [0, 30, 50, 70, 100]
    labels = ['کم‌وفادار', 'متوسط', 'وفادار', 'بسیار وفادار']
    guests_df_copy = guests_df.copy()
    guests_df_copy['سطح'] = pd.cut(guests_df_copy['امتیاز_وفاداری'], bins=bins, labels=labels, right=True)
    tier_counts = guests_df_copy['سطح'].value_counts().reset_index()
    tier_counts.columns = ['سطح', 'تعداد']
    fig = px.pie(tier_counts, values='تعداد', names='سطح', title='تقسیم‌بندی وفاداری', hole=0.4,
                 color_discrete_sequence=['#FF6B6B', '#FECA57', '#48DBFB', '#0ABDE3'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def plot_geography(guests_df):
    if guests_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    city_counts = guests_df['شهر'].value_counts().reset_index()
    city_counts.columns = ['شهر', 'تعداد']
    city_counts = city_counts.sort_values('تعداد', ascending=True)
    fig = px.bar(city_counts, x='تعداد', y='شهر', title='توزیع جغرافیایی', 
                 color='تعداد', color_continuous_scale=[HOTEL_CONFIG['colors']['secondary'], HOTEL_CONFIG['colors']['accent']], 
                 orientation='h')
    fig.update_layout(height=400)
    return fig

def plot_art_preferences(guests_df):
    if guests_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    if 'علاقه_هنری' not in guests_df.columns:
        fig = px.bar(title='داده‌ای برای تحلیل هنری وجود ندارد')
        fig.update_layout(annotations=[{'text': 'ستون علاقه هنری موجود نیست', 'x': 0.5, 'y': 0.5, 'showarrow': False}])
        return fig
    counts = guests_df['علاقه_هنری'].value_counts().reset_index()
    counts.columns = ['علاقه', 'تعداد']
    fig = px.bar(counts, x='علاقه', y='تعداد', title='علایق هنری مهمانان',
                 color='تعداد', color_continuous_scale=[HOTEL_CONFIG['colors']['primary'], HOTEL_CONFIG['colors']['accent']])
    fig.update_layout(showlegend=False)
    return fig

def plot_guest_growth(guests_df):
    if guests_df.empty:
        return px.line(title='داده‌ای وجود ندارد')
    guests_df_copy = guests_df.copy()
    guests_df_copy['تاریخ_اولین_اقامت'] = pd.to_datetime(guests_df_copy['تاریخ_اولین_اقامت'])
    monthly = guests_df_copy.groupby(guests_df_copy['تاریخ_اولین_اقامت'].dt.to_period('M')).size().reset_index()
    monthly.columns = ['ماه', 'مهمانان جدید']
    monthly['ماه'] = monthly['ماه'].astype(str)
    fig = px.line(monthly, x='ماه', y='مهمانان جدید', title='روند جذب مهمانان', 
                  markers=True, line_shape='spline')
    fig.update_traces(line=dict(color=HOTEL_CONFIG['colors']['primary'], width=3), 
                      marker=dict(color=HOTEL_CONFIG['colors']['secondary'], size=8))
    return fig

def plot_room_analysis(reservations_df):
    if reservations_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    room_stats = reservations_df[reservations_df['وضعیت'] == 'تکمیل‌شده'].groupby('اتاق').agg({
        'قیمت_هر_شب': 'mean',
        'شناسه_رزرو': 'count'
    }).reset_index()
    room_stats.columns = ['اتاق', 'میانگین قیمت', 'تعداد رزرو']
    fig = px.bar(room_stats, x='اتاق', y='میانگین قیمت', title='میانگین قیمت هر اتاق',
                 color='تعداد رزرو', color_continuous_scale=[HOTEL_CONFIG['colors']['secondary'], HOTEL_CONFIG['colors']['accent']],
                 text='میانگین قیمت')
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(yaxis_title='قیمت (تومان)')
    return fig

def plot_events_dashboard(events_df):
    if events_df.empty:
        return px.bar(title='داده‌ای وجود ندارد'), px.bar(title='داده‌ای وجود ندارد')
    events_copy = events_df.copy()
    events_copy['درصد_پر شدن'] = (events_copy['ثبت_نام'] / events_copy['ظرفیت']) * 100
    events_copy = events_copy.sort_values('تاریخ')
    fig1 = px.bar(events_copy, x='نام_ایونت', y=['ظرفیت', 'ثبت_نام'],
                  title='وضعیت ثبت‌نام ایونت‌ها', barmode='group',
                  color_discrete_sequence=[HOTEL_CONFIG['colors']['primary'], HOTEL_CONFIG['colors']['secondary']])
    fig1.update_layout(xaxis_title='ایونت', yaxis_title='تعداد')
    fig2 = px.bar(events_copy, x='نام_ایونت', y='درصد_پر شدن',
                  title='درصد پر شدن ظرفیت', color='درصد_پر شدن',
                  color_continuous_scale=[[0, 'red'], [0.5, 'yellow'], [1, 'green']])
    fig2.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    fig2.update_layout(xaxis_title='ایونت', yaxis_title='درصد پر شدن')
    return fig1, fig2

def plot_event_revenue(events_df, reservations_df):
    if events_df.empty or reservations_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    event_rev = events_df.copy()
    event_rev['درآمد'] = event_rev['ثبت_نام'] * (event_rev['قیمت'] / 10000)
    event_rev = event_rev.sort_values('درآمد', ascending=True)
    fig = px.bar(event_rev, x='درآمد', y='نام_ایونت', title='درآمد ایونت‌ها (هزار تومان)',
                 color='درآمد', color_continuous_scale=[HOTEL_CONFIG['colors']['secondary'], HOTEL_CONFIG['colors']['accent']], 
                 orientation='h')
    fig.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
    fig.update_layout(xaxis_title='درآمد (هزار تومان)', yaxis_title='ایونت')
    return fig

def plot_prediction_chart(prediction_data):
    if prediction_data is None:
        return None
    fig = go.Figure()
    historical = prediction_data['daily_occupancy']
    fig.add_trace(go.Scatter(
        x=historical['تاریخ'],
        y=historical['تعداد'],
        mode='lines+markers',
        name='داده‌های تاریخی',
        line=dict(color=HOTEL_CONFIG['colors']['primary'], width=2)
    ))
    future_dates = prediction_data['future_dates']
    predictions = prediction_data['predictions']
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predictions,
        mode='lines+markers',
        name='پیش‌بینی',
        line=dict(color='#FF6B6B', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='پیش‌بینی نرخ اشغال هتل',
        xaxis_title='تاریخ',
        yaxis_title='تعداد رزرو',
        height=400,
        hovermode='x'
    )
    return fig

# ============================================
# بخش مدیریت اطلاعات
# ============================================

def management_section(guests_df, reservations_df, events_df):
    st.header("📝 پنل مدیریت اطلاعات")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 مهمانان", "🏠 رزروها", "🎭 ایونت‌ها", "📊 ثبت‌نام ایونت", "📤 آپلود فایل"])
    
    # تب ۱: مهمانان
    with tab1:
        st.subheader("👤 مدیریت مهمانان")
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ حذف همه مهمانان", type="secondary"):
                guests_df = pd.DataFrame(columns=guests_df.columns)
                save_data(guests_df, reservations_df, events_df)
                st.success("✅ همه مهمانان حذف شدند!")
                st.rerun()
        
        display_guests = guests_df.copy()
        if 'تاریخ_اولین_اقامت' in display_guests.columns:
            display_guests['تاریخ_اولین_اقامت'] = display_guests['تاریخ_اولین_اقامت'].apply(
                lambda x: to_persian_date(x) if pd.notna(x) else ''
            )
        if 'امتیاز_وفاداری' in display_guests.columns:
            display_guests['امتیاز_وفاداری'] = display_guests['امتیاز_وفاداری'].apply(to_persian_number)
        if 'شماره_تماس' in display_guests.columns:
            display_guests['شماره_تماس'] = display_guests['شماره_تماس'].apply(to_persian_number)
        st.dataframe(display_guests, use_container_width=True, hide_index=True)
        
        with st.expander("➕ افزودن مهمان جدید"):
            with st.form("add_guest"):
                col1, col2 = st.columns(2)
                with col1:
                    first = st.text_input("نام")
                    last = st.text_input("نام خانوادگی")
                    phone = st.text_input("شماره تماس")
                with col2:
                    city = st.selectbox("شهر", ['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان', 'کرمان'])
                    art = st.selectbox("علاقه هنری", HOTEL_CONFIG['event_categories'])
                if st.form_submit_button("افزودن مهمان"):
                    if first and last and phone:
                        new_id = f"G{len(guests_df) + 1000}"
                        new_guest = pd.DataFrame([{
                            'guest_id': new_id,
                            'نام': first,
                            'نام_خانوادگی': last,
                            'شماره_تماس': phone,
                            'شهر': city,
                            'تاریخ_اولین_اقامت': datetime.now().strftime('%Y-%m-%d'),
                            'تعداد_اقامت': 1,
                            'علاقه_هنری': art,
                            'امتیاز_وفاداری': 50.0
                        }])
                        guests_df_updated = pd.concat([guests_df, new_guest], ignore_index=True)
                        save_data(guests_df_updated, reservations_df, events_df)
                        st.success(f"✅ مهمان {first} {last} افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ نام و شماره تماس الزامی است!")
    
    # تب ۲: رزروها
    with tab2:
        st.subheader("🏠 مدیریت رزروها")
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ حذف همه رزروها", type="secondary"):
                reservations_df = pd.DataFrame(columns=reservations_df.columns)
                save_data(guests_df, reservations_df, events_df)
                st.success("✅ همه رزروها حذف شدند!")
                st.rerun()
        
        display_res = reservations_df.copy()
        if 'تاریخ_ورود' in display_res.columns:
            display_res['تاریخ_ورود'] = display_res['تاریخ_ورود'].apply(
                lambda x: to_persian_date(x) if pd.notna(x) else ''
            )
        if 'تاریخ_خروج' in display_res.columns:
            display_res['تاریخ_خروج'] = display_res['تاریخ_خروج'].apply(
                lambda x: to_persian_date(x) if pd.notna(x) else ''
            )
        if 'قیمت_هر_شب' in display_res.columns:
            display_res['قیمت_هر_شب'] = display_res['قیمت_هر_شب'].apply(format_price_persian)
        st.dataframe(display_res, use_container_width=True, hide_index=True)
        
        with st.expander("➕ افزودن رزرو جدید"):
            with st.form("add_reservation"):
                col1, col2 = st.columns(2)
                with col1:
                    guest_id = st.selectbox("شناسه مهمان", guests_df['guest_id'].tolist() if not guests_df.empty else [''])
                    check_in = st.date_input("تاریخ ورود")
                    check_out = st.date_input("تاریخ خروج")
                with col2:
                    room_type = st.selectbox("نوع اتاق", [room['name'] for room in HOTEL_CONFIG['rooms']])
                    price = st.number_input("قیمت هر شب (تومان)", min_value=100000, step=100000, value=5000000)
                    channel = st.selectbox("کانال رزرو", ['وب‌سایت', 'بوکینگ', 'اینستاگرام', 'تلفن', 'حضوری'])
                if st.form_submit_button("افزودن رزرو"):
                    if guest_id and check_in and check_out:
                        new_id = f"R{len(reservations_df) + 10000}"
                        new_res = pd.DataFrame([{
                            'شناسه_رزرو': new_id,
                            'شناسه_مهمان': guest_id,
                            'تاریخ_ورود': check_in.strftime('%Y-%m-%d'),
                            'تاریخ_خروج': check_out.strftime('%Y-%m-%d'),
                            'اتاق': room_type,
                            'قیمت_هر_شب': price,
                            'کانال': channel,
                            'وضعیت': 'تکمیل‌شده'
                        }])
                        reservations_df_updated = pd.concat([reservations_df, new_res], ignore_index=True)
                        save_data(guests_df, reservations_df_updated, events_df)
                        st.success(f"✅ رزرو {new_id} افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ همه فیلدها را پر کنید!")
    
    # تب ۳: ایونت‌ها
    with tab3:
        st.subheader("🎭 مدیریت ایونت‌ها")
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ حذف همه ایونت‌ها", type="secondary"):
                events_df = pd.DataFrame(columns=events_df.columns)
                save_data(guests_df, reservations_df, events_df)
                st.success("✅ همه ایونت‌ها حذف شدند!")
                st.rerun()
        
        display_events = events_df.copy()
        if 'تاریخ' in display_events.columns:
            display_events['تاریخ'] = display_events['تاریخ'].apply(
                lambda x: to_persian_date(x) if pd.notna(x) else ''
            )
        if 'قیمت' in display_events.columns:
            display_events['قیمت'] = display_events['قیمت'].apply(format_price_persian)
        if 'ظرفیت' in display_events.columns:
            display_events['ظرفیت'] = display_events['ظرفیت'].apply(to_persian_number)
        if 'ثبت_نام' in display_events.columns:
            display_events['ثبت_نام'] = display_events['ثبت_نام'].apply(to_persian_number)
        st.dataframe(display_events, use_container_width=True, hide_index=True)
        
        with st.expander("➕ افزودن ایونت جدید"):
            with st.form("add_event"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("نام ایونت")
                    date = st.date_input("تاریخ برگزاری")
                with col2:
                    capacity = st.number_input("ظرفیت", min_value=1, value=30)
                    price = st.number_input("قیمت (تومان)", min_value=0, step=100000, value=1000000)
                    category = st.selectbox("دسته‌بندی", HOTEL_CONFIG['event_categories'])
                if st.form_submit_button("افزودن ایونت"):
                    if name and date:
                        new_id = f"E{len(events_df) + 2000}"
                        new_event = pd.DataFrame([{
                            'شناسه_ایونت': new_id,
                            'نام_ایونت': name,
                            'تاریخ': date.strftime('%Y-%m-%d'),
                            'ظرفیت': capacity,
                            'ثبت_نام': 0,
                            'قیمت': price,
                            'دسته_بندی': category
                        }])
                        events_df_updated = pd.concat([events_df, new_event], ignore_index=True)
                        save_data(guests_df, reservations_df, events_df_updated)
                        st.success(f"✅ ایونت {name} افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ نام و تاریخ ایونت الزامی است!")
    
    # تب ۴: ثبت‌نام در ایونت
    with tab4:
        st.subheader("📊 ثبت‌نام مهمانان در ایونت‌ها")
        col1, col2 = st.columns(2)
        with col1:
            if not events_df.empty:
                selected_event = st.selectbox("ایونت مورد نظر", events_df['نام_ایونت'].tolist())
                event_data = events_df[events_df['نام_ایونت'] == selected_event]
                if not event_data.empty:
                    st.info(f"""
                    **📋 اطلاعات ایونت:**
                    - تاریخ: {to_persian_date(event_data['تاریخ'].iloc[0])}
                    - ظرفیت: {to_persian_number(event_data['ظرفیت'].iloc[0])}
                    - ثبت‌نام فعلی: {to_persian_number(event_data['ثبت_نام'].iloc[0])}
                    - جای خالی: {to_persian_number(event_data['ظرفیت'].iloc[0] - event_data['ثبت_نام'].iloc[0])}
                    """)
            else:
                st.warning("هیچ ایونتی برای نمایش وجود ندارد")
        with col2:
            if not guests_df.empty:
                guest_list = guests_df['نام'] + ' ' + guests_df['نام_خانوادگی'] + ' (' + guests_df['guest_id'] + ')'
                selected_guest = st.selectbox("مهمان", guest_list.tolist())
                if st.button("✅ ثبت‌نام در ایونت", use_container_width=True):
                    if not events_df.empty:
                        event_idx = events_df[events_df['نام_ایونت'] == selected_event].index[0]
                        events_df.loc[event_idx, 'ثبت_نام'] += 1
                        save_data(guests_df, reservations_df, events_df)
                        st.success(f"✅ ثبت‌نام با موفقیت انجام شد!")
                        st.balloons()
                        st.rerun()
            else:
                st.warning("هیچ مهمانی برای ثبت‌نام وجود ندارد")
    
    # تب ۵: آپلود فایل
    with tab5:
        st.subheader("📤 آپلود اطلاعات مهمانان از فایل")
        st.info("""
        **راهنمای آپلود فایل:**
        - فایل‌های CSV یا Excel را آپلود کنید
        - ستون‌های مورد نیاز: `نام`, `نام_خانوادگی`, `شماره_تماس`, `شهر`, `علاقه_هنری`
        - فایل شما باید دارای هدر (عنوان ستون‌ها) باشد
        """)
        
        uploaded_file = st.file_uploader(
            "📂 انتخاب فایل (CSV یا Excel)",
            type=['csv', 'xlsx', 'xls']
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    new_guests = pd.read_csv(uploaded_file, encoding='utf-8-sig')
                else:
                    new_guests = pd.read_excel(uploaded_file)
                
                st.subheader("📋 پیش‌نمایش داده‌های آپلود شده")
                st.dataframe(new_guests.head(10), use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**تعداد رکوردها:** {len(new_guests)}")
                with col2:
                    if st.button("✅ افزودن به داده‌های هتل", use_container_width=True):
                        required_cols = ['نام', 'نام_خانوادگی', 'شماره_تماس']
                        missing_cols = [col for col in required_cols if col not in new_guests.columns]
                        
                        if missing_cols:
                            st.error(f"❌ ستون‌های زیر در فایل وجود ندارند: {', '.join(missing_cols)}")
                        else:
                            start_id = len(guests_df) + 1000
                            new_guests['guest_id'] = [f'G{start_id + i}' for i in range(len(new_guests))]
                            
                            if 'شهر' not in new_guests.columns:
                                new_guests['شهر'] = 'شیراز'
                            if 'علاقه_هنری' not in new_guests.columns:
                                new_guests['علاقه_هنری'] = 'هنر'
                            if 'تاریخ_اولین_اقامت' not in new_guests.columns:
                                new_guests['تاریخ_اولین_اقامت'] = datetime.now().strftime('%Y-%m-%d')
                            if 'تعداد_اقامت' not in new_guests.columns:
                                new_guests['تعداد_اقامت'] = 1
                            if 'امتیاز_وفاداری' not in new_guests.columns:
                                new_guests['امتیاز_وفاداری'] = 50.0
                            
                            guests_df_updated = pd.concat([guests_df, new_guests], ignore_index=True)
                            save_data(guests_df_updated, reservations_df, events_df)
                            st.success(f"✅ {len(new_guests)} مهمان با موفقیت به سیستم اضافه شدند!")
                            st.balloons()
                            st.rerun()
            except Exception as e:
                st.error(f"❌ خطا در خواندن فایل: {str(e)}")
    
    return guests_df, reservations_df, events_df

# ============================================
# بخش تحلیل و گزارش
# ============================================

def analytics_section(guests_df, reservations_df, events_df):
    st.header("📊 تحلیل‌های هوشمند و پیش‌بینی‌ها")
    
    kpis = calculate_kpis(guests_df, reservations_df, events_df)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("👥 مهمانان", to_persian_number(kpis['total_guests']))
    with col2:
        st.metric("📈 نرخ اشغال", f"{to_persian_number(f'{kpis['occupancy']:.1f}')}%")
    with col3:
        st.metric("💰 ADR", f"{to_persian_number(f'{kpis['adr']:,.0f}')} تومان")
    with col4:
        st.metric("🏠 اتاق محبوب", kpis['popular_room'])
    with col5:
        st.metric("🎨 هنر محبوب", kpis['popular_art'])
    with col6:
        st.metric("❌ نرخ لغو", f"{to_persian_number(f'{kpis['cancellation_rate']:.1f}')}%")
    
    st.markdown("---")
    
    # پیش‌بینی‌ها
    st.subheader("🔮 پیش‌بینی‌های هوشمند")
    
    occupancy_pred = predict_occupancy(reservations_df, days_ahead=30)
    
    col1, col2, col3 = st.columns(3)
    
    if occupancy_pred:
        with col1:
            st.markdown(f"""
            <div class="prediction-box">
                <h3>📊 پیش‌بینی اشغال</h3>
                <div class="number">{to_persian_number(f'{occupancy_pred["avg_occupancy"]:.1f}')}</div>
                <p>میانگین رزرو در ۳۰ روز آینده</p>
                <p style="color: {'#2E7D32' if occupancy_pred['trend'] == 'صعودی' else '#C62828'}">
                    روند: {occupancy_pred['trend']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="prediction-box" style="background: linear-gradient(135deg, #E3F2FD, #BBDEFB); border-right-color: #1565C0;">
                <h3>💰 پیش‌بینی درآمد</h3>
                <div class="number" style="color: #1565C0;">{to_persian_number(f'{occupancy_pred["predicted_revenue"]/1000000:.1f}')}</div>
                <p>میلیون تومان درآمد تخمینی ماه آینده</p>
            </div>
            """, unsafe_allow_html=True)
    
    guest_pred = predict_guest_growth(guests_df, months_ahead=3)
    if guest_pred:
        with col3:
            st.markdown(f"""
            <div class="prediction-box" style="background: linear-gradient(135deg, #FFF3E0, #FFE0B2); border-right-color: #E65100;">
                <h3>👥 پیش‌بینی رشد</h3>
                <div class="number" style="color: #E65100;">{to_persian_number(guest_pred['total_new_guests'])}</div>
                <p>تخمین مهمانان جدید در ۳ ماه آینده</p>
                <p style="color: {'#2E7D32' if guest_pred['trend'] == 'صعودی' else '#C62828'}">
                    روند: {guest_pred['trend']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    if occupancy_pred:
        st.plotly_chart(plot_prediction_chart(occupancy_pred), use_container_width=True)
    
    event_pred = predict_events_success(events_df)
    if event_pred:
        st.info(f"""
        **🎭 پیش‌بینی ایونت‌ها:**
        - میانگین موفقیت ایونت‌ها: {to_persian_number(f'{event_pred["avg_success_rate"]:.1f}')}%
        - بهترین دسته‌بندی: {event_pred['best_category']}
        - توصیه: {event_pred['recommendation']}
        """)
    
    st.markdown("---")
    
    # نمودارها
    st.subheader("👥 تحلیل مهمانان")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_loyalty_segmentation(guests_df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_geography(guests_df), use_container_width=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(plot_guest_growth(guests_df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_art_preferences(guests_df), use_container_width=True)
    
    st.markdown("---")
    st.subheader("🏠 تحلیل اتاق‌ها")
    st.plotly_chart(plot_room_analysis(reservations_df), use_container_width=True)
    
    st.markdown("---")
    st.subheader("🎭 تحلیل ایونت‌ها")
    col1, col2 = st.columns(2)
    with col1:
        fig1, fig2 = plot_events_dashboard(events_df)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    st.plotly_chart(plot_event_revenue(events_df, reservations_df), use_container_width=True)

# ============================================
# تابع اصلی
# ============================================

def main():
    if not os.path.exists('data'):
        generate_realistic_data()
    
    guests_df, reservations_df, events_df = load_data()
    
    if guests_df is None:
        st.error("❌ خطا در بارگذاری داده‌ها. در حال تولید داده‌های جدید...")
        generate_realistic_data()
        guests_df, reservations_df, events_df = load_data()
        if guests_df is None:
            st.error("❌ خطای جدی در بارگذاری داده. لطفاً پوشه data را بررسی کنید.")
            st.stop()
    
    # سایدبار
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-logo">
            <img src="{HOTEL_CONFIG['logo_url']}" alt="لوگو هتل" onerror="this.style.display='none'">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        menu = st.radio("📋 منوی اصلی", ["📊 تحلیل و گزارش", "📝 مدیریت اطلاعات"])
        st.markdown("---")
        
        st.caption(f"📅 {to_persian_number(datetime.now().strftime('%Y-%m-%d'))}")
        st.caption(f"👥 {to_persian_number(len(guests_df))} مهمان")
        st.caption(f"🏠 {to_persian_number(len(reservations_df))} رزرو")
        st.caption(f"🎭 {to_persian_number(len(events_df))} ایونت")
        
        st.markdown("---")
        st.caption("🔮 با پیش‌بینی‌های هوشمند")
    
    if menu == "📊 تحلیل و گزارش":
        analytics_section(guests_df, reservations_df, events_df)
    else:
        guests_df, reservations_df, events_df = management_section(guests_df, reservations_df, events_df)
    
    st.markdown("---")
    st.caption("🏛️ بوتیک هتل محلاتی - داشبورد حرفه‌ای مدیریت هتل | توسعه‌یافته با Streamlit")

if __name__ == "__main__":
    main()
