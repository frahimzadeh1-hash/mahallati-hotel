import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
import re

# ============================================
# تنظیمات هویتی و ظاهری هتل (بر اساس وب‌سایت)
# ============================================
HOTEL_CONFIG = {
    "name": "بوتیک هتل محلاتی",
    "colors": {
        "primary": "#8B4513",     # قهوه‌ای چوبی
        "secondary": "#D2691E",   # نارنجی کاشی‌کاری
        "accent": "#FFD700",      # طلایی گچ‌بری
        "background": "#FDF5E6",  # کرم کهنه‌کار
        "text": "#3E2723"         # قهوه‌ای تیره
    },
    "fonts": {"primary": "Vazir, sans-serif"},
    "rooms": ["اتاق سنتی", "اتاق مدرن", "سوئیت", "اتاق خانوادگی", "کلبه باغ"],
    "event_categories": ["موسیقی", "شعر", "فیلم", "هنرهای تجسمی", "تاریخ و معماری"]
}

# ============================================
# تنظیمات صفحه با هویت بصری هتل
# ============================================
st.set_page_config(
    page_title=f"🏨 {HOTEL_CONFIG['name']} - داشبورد مدیریت",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# اعمال استایل‌های هویتی
st.markdown(f"""
<style>
    .stApp {{
        background-color: {HOTEL_CONFIG['colors']['background']};
        direction: rtl;
    }}
    h1, h2, h3, h4, h5, p, div, span {{
        font-family: {HOTEL_CONFIG['fonts']['primary']};
        color: {HOTEL_CONFIG['colors']['text']};
    }}
    .hotel-header {{
        background: linear-gradient(135deg, {HOTEL_CONFIG['colors']['primary']}, {HOTEL_CONFIG['colors']['secondary']});
        padding: 20px;
        border-radius: 10px;
        color: white !important;
        text-align: center;
        margin-bottom: 30px;
        border-right: 8px solid {HOTEL_CONFIG['colors']['accent']};
    }}
    .hotel-header h1, .hotel-header h2, .hotel-header p {{
        color: white !important;
    }}
    .stMetric {{
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border-right: 4px solid {HOTEL_CONFIG['colors']['accent']};
    }}
    .stButton>button {{
        background: {HOTEL_CONFIG['colors']['secondary']};
        color: white;
        border: none;
        border-radius: 8px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: {HOTEL_CONFIG['colors']['primary']};
        transform: scale(1.02);
    }}
    .insight-box {{
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-right: 4px solid {HOTEL_CONFIG['colors']['secondary']};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 10px 0;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# توابع تولید داده (با افزودن داده‌های هویتی)
# ============================================

def generate_sample_data():
    """تولید داده‌های نمونه با هویت هنری هتل"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # اسامی مرتبط با هنر و تاریخ
    first_names = ['احمد', 'سارا', 'محمد', 'زهرا', 'علی', 'مریم', 'رضا', 'فاطمه', 
                   'حسین', 'نگار', 'کیان', 'نازنین', 'امیر', 'سپیده', 'مهدی', 'الهه']
    last_names = ['محلاتی', 'کریمی', 'حسینی', 'رضوی', 'نوری', 'یزدی', 'شیرازی', 
                  'کاشانی', 'اصفهانی', 'تبریزی', 'فردوسی', 'سهرابی']
    cities = ['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان']
    preferences = ['نقاشی', 'معماری', 'شعر', 'موسیقی', 'تاریخ', 'صنایع‌دستی', 'خوشنویسی']
    channels = ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in']
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # تولید مهمانان با علایق هنری
    guests = []
    for i in range(250):
        guest = {
            'guest_id': f'G{1000+i}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'phone': f'0912{random.randint(1000000, 9999999)}',
            'city': random.choice(cities),
            'first_visit': random.choice(date_range).strftime('%Y-%m-%d'),
            'total_visits': random.randint(1, 10),
            'art_preference': random.choice(preferences),  # کلید جدید
            'loyalty_score': round(random.uniform(0, 100), 1)
        }
        guests.append(guest)
    guests_df = pd.DataFrame(guests)
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    
    # تولید رزرو با انواع اتاق‌ها
    reservations = []
    for i in range(600):
        check_in = random.choice(date_range)
        stay_days = random.randint(1, 5)
        check_out = check_in + timedelta(days=stay_days)
        reservation = {
            'reservation_id': f'R{10000+i}',
            'guest_id': f'G{random.randint(1000, 1249)}',
            'check_in': check_in.strftime('%Y-%m-%d'),
            'check_out': check_out.strftime('%Y-%m-%d'),
            'room_type': random.choice(HOTEL_CONFIG['rooms']),
            'price_per_night': random.randint(150, 600) * 10000,
            'channel': random.choice(channels),
            'status': random.choices(['completed', 'cancelled', 'no-show'], weights=[0.7, 0.2, 0.1])[0]
        }
        reservations.append(reservation)
    reservations_df = pd.DataFrame(reservations)
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    
    # تولید ایونت‌های فرهنگی
    events = []
    event_templates = [
        ('شب شعر حافظ', 'شعر', 30, 15),
        ('کنسرت سه‌تار', 'موسیقی', 40, 20),
        ('نمایشگاه نقاشی قاجار', 'هنرهای تجسمی', 50, 25),
        ('کارگاه خوشنویسی', 'هنرهای تجسمی', 20, 10),
        ('سخنرانی تاریخ زندیه', 'تاریخ و معماری', 35, 15),
        ('شب موسیقی سنتی', 'موسیقی', 45, 20),
        ('تور معماری', 'تاریخ و معماری', 25, 10)
    ]
    
    for i in range(35):
        event_date = random.choice(date_range)
        template = random.choice(event_templates)
        event = {
            'event_id': f'E{2000+i}',
            'event_name': template[0],
            'date': event_date.strftime('%Y-%m-%d'),
            'capacity': template[2] + random.randint(-5, 10),
            'registered': template[3] + random.randint(-5, 15),
            'price': random.randint(30, 150) * 10000,
            'category': template[1]
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
        reservations['check_in'] = pd.to_datetime(reservations['check_in'])
        reservations['check_out'] = pd.to_datetime(reservations['check_out'])
        events['date'] = pd.to_datetime(events['date'])
        return guests, reservations, events
    except:
        return None, None, None

def save_data(guests_df, reservations_df, events_df):
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')

# ============================================
# توابع تحلیلی با رویکرد هنری-تاریخی
# ============================================

def calculate_artistic_kpis(guests_df, reservations_df, events_df):
    """محاسبه شاخص‌های کلیدی با نگاه به هنر و فرهنگ"""
    total_guests = len(guests_df)
    
    # هنر محبوب
    if not guests_df.empty:
        top_art = guests_df['art_preference'].mode()[0] if not guests_df['art_preference'].empty else 'نامشخص'
    else:
        top_art = 'نامشخص'
    
    # ایونت‌های پرمخاطب
    if not events_df.empty:
        popular_event = events_df.loc[events_df['registered'].idxmax()]['event_name'] if not events_df.empty else 'نامشخص'
        avg_fill_rate = (events_df['registered'].sum() / events_df['capacity'].sum()) * 100 if events_df['capacity'].sum() > 0 else 0
    else:
        popular_event = 'نامشخص'
        avg_fill_rate = 0
    
    # بازگشت هنردوستان
    art_lovers = guests_df[guests_df['art_preference'] != 'تاریخ']  # فرضی
    return {
        'total_guests': total_guests,
        'top_art_preference': top_art,
        'popular_event': popular_event,
        'avg_event_fill_rate': avg_fill_rate,
        'art_lovers_return': (art_lovers['total_visits'].mean() if not art_lovers.empty else 0)
    }

def calculate_kpis(reservations_df):
    if reservations_df.empty:
        return {'total': 0, 'completed': 0, 'cancelled': 0, 'revenue': 0, 'adr': 0, 'occupancy': 0}
    completed = reservations_df[reservations_df['status'] == 'completed']
    revenue = (completed['price_per_night'] * (completed['check_out'] - completed['check_in']).dt.days).sum() if not completed.empty else 0
    adr = completed['price_per_night'].mean() if not completed.empty else 0
    return {
        'total': len(reservations_df),
        'completed': len(completed),
        'cancelled': len(reservations_df[reservations_df['status'] == 'cancelled']),
        'revenue': revenue,
        'adr': adr,
        'occupancy': len(completed) / 30 / 20 * 100 if len(completed) > 0 else 0
    }

# ============================================
# توابع رسم نمودار با رنگ‌های هتل
# ============================================

def plot_art_preferences(guests_df):
    if guests_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    counts = guests_df['art_preference'].value_counts().reset_index()
    counts.columns = ['علاقه', 'تعداد']
    fig = px.bar(counts, x='علاقه', y='تعداد', title='علایق هنری مهمانان', 
                 color='تعداد', color_continuous_scale=['#D2691E', '#FFD700'])
    fig.update_layout(showlegend=False)
    return fig

def plot_event_categories(events_df):
    if events_df.empty:
        return px.pie(title='داده‌ای وجود ندارد')
    cat_stats = events_df.groupby('category').agg({'registered': 'sum', 'capacity': 'sum'}).reset_index()
    cat_stats['fill_rate'] = (cat_stats['registered'] / cat_stats['capacity']) * 100
    fig = px.bar(cat_stats, x='category', y='fill_rate', title='استقبال از دسته‌های ایونت',
                 color='fill_rate', color_continuous_scale=['#8B4513', '#FFD700'])
    return fig

# ============================================
# توابع مدیریت (ساده‌شده)
# ============================================

def management_section(guests_df, reservations_df, events_df):
    st.header("📝 پنل مدیریت")
    tab1, tab2, tab3 = st.tabs(["👤 مهمانان", "🏠 رزروها", "🎭 ایونت‌ها"])
    
    with tab1:
        st.subheader("لیست مهمانان")
        st.dataframe(guests_df, use_container_width=True)
        with st.form("add_guest"):
            st.subheader("افزودن مهمان")
            col1, col2 = st.columns(2)
            with col1:
                first = st.text_input("نام")
                last = st.text_input("نام خانوادگی")
                phone = st.text_input("شماره تماس")
            with col2:
                city = st.selectbox("شهر", ['تهران', 'شیراز', 'اصفهان', 'مشهد'])
                art = st.selectbox("علاقه هنری", HOTEL_CONFIG['event_categories'])
            if st.form_submit_button("افزودن"):
                # منطق افزودن
                pass

    with tab2:
        st.subheader("لیست رزروها")
        st.dataframe(reservations_df, use_container_width=True)

    with tab3:
        st.subheader("لیست ایونت‌ها")
        st.dataframe(events_df, use_container_width=True)
    
    return guests_df, reservations_df, events_df

# ============================================
# بخش تحلیل‌های اصلی
# ============================================

def analytics_section(guests_df, reservations_df, events_df):
    st.header("📊 تحلیل‌های هوشمند بر اساس هویت هتل")
    
    # اطلاعات هویتی
    st.markdown(f"""
    <div class="hotel-header">
        <h2>🏛️ {HOTEL_CONFIG['name']}</h2>
        <p>تحلیل‌های بر اساس هنر، تاریخ و معماری</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIهای هنری
    art_kpis = calculate_artistic_kpis(guests_df, reservations_df, events_df)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 کل مهمانان", art_kpis['total_guests'])
    with col2:
        st.metric("🎨 محبوب‌ترین هنر", art_kpis['top_art_preference'])
    with col3:
        st.metric("🎭 ایونت پرمخاطب", art_kpis['popular_event'][:15] + "...")
    with col4:
        st.metric("📈 میانگین پر شدن ایونت‌ها", f"{art_kpis['avg_event_fill_rate']:.1f}%")
    
    st.markdown("---")
    
    # نمودارهای تحلیل هنری
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_art_preferences(guests_df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_event_categories(events_df), use_container_width=True)
    
    # تحلیل اتاق‌ها و درآمد
    st.subheader("🏠 تحلیل اتاق‌ها و درآمد")
    room_stats = reservations_df.groupby('room_type').agg({
        'price_per_night': 'mean',
        'reservation_id': 'count'
    }).reset_index()
    room_stats.columns = ['اتاق', 'میانگین قیمت', 'تعداد رزرو']
    fig = px.bar(room_stats, x='اتاق', y='میانگین قیمت', title='میانگین قیمت هر اتاق',
                 color='تعداد رزرو', color_continuous_scale=['#D2691E', '#FFD700'])
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# تابع اصلی
# ============================================

def main():
    # تولید/بارگذاری داده
    if not os.path.exists('data'):
        generate_sample_data()
    guests_df, reservations_df, events_df = load_data()
    if guests_df is None:
        generate_sample_data()
        guests_df, reservations_df, events_df = load_data()
    
    # سایدبار منو
    with st.sidebar:
        st.image("https://via.placeholder.com/300x80/8B4513/FFFFFF?text=Mahallati+Hotel", use_column_width=True)
        st.markdown("---")
        menu = st.radio("📋 منو", ["📊 تحلیل و گزارش", "📝 مدیریت اطلاعات"])
        st.markdown("---")
        st.caption(f"نسخه ۲.۰ | {datetime.now().strftime('%Y-%m-%d')}")
    
    # نمایش بخش‌ها
    if menu == "📊 تحلیل و گزارش":
        analytics_section(guests_df, reservations_df, events_df)
    else:
        management_section(guests_df, reservations_df, events_df)
    
    st.markdown("---")
    st.caption("🏛️ بوتیک هتل محلاتی - داشبورد هوشمند با نگاه به هنر و تاریخ")

if __name__ == "__main__":
    main()
