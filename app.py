import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os
import re

# ============================================
# تنظیمات هویتی هتل (بر اساس وب‌سایت)
# ============================================
HOTEL_CONFIG = {
    "name": "بوتیک هتل محلاتی",
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
        "primary": "#8B4513",
        "secondary": "#D2691E",
        "accent": "#FFD700",
        "background": "#FDF5E6",
        "text": "#3E2723"
    },
    "event_categories": ["موسیقی", "شعر", "هنرهای تجسمی", "تاریخ و معماری", "خوشنویسی"]
}

# ============================================
# تنظیمات صفحه
# ============================================
st.set_page_config(
    page_title=f"🏨 {HOTEL_CONFIG['name']} - داشبورد مدیریت",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# اعمال استایل هویتی
st.markdown(f"""
<style>
    .stApp {{
        background-color: {HOTEL_CONFIG['colors']['background']};
        direction: rtl;
        font-family: 'Vazir', sans-serif;
    }}
    .hotel-header {{
        background: linear-gradient(135deg, {HOTEL_CONFIG['colors']['primary']}, {HOTEL_CONFIG['colors']['secondary']});
        padding: 20px 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        border-right: 6px solid {HOTEL_CONFIG['colors']['accent']};
    }}
    .hotel-header h1, .hotel-header h2, .hotel-header p {{
        color: white !important;
        margin: 0;
    }}
    .stMetric {{
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-right: 4px solid {HOTEL_CONFIG['colors']['accent']};
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
        box-shadow: 0 4px 12px rgba(139,69,19,0.3);
    }}
    .info-box {{
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-right: 4px solid {HOTEL_CONFIG['colors']['secondary']};
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin: 10px 0;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# توابع تولید داده‌های نمونه
# ============================================

def generate_realistic_data():
    """تولید داده‌های نمونه بر اساس اطلاعات واقعی هتل"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # اسامی مهمانان
    first_names = ['احمد', 'سارا', 'محمد', 'زهرا', 'علی', 'مریم', 'رضا', 'فاطمه', 
                   'حسین', 'نگار', 'کیان', 'نازنین', 'امیر', 'سپیده', 'مهدی', 'الهه',
                   'پویا', 'شیرین', 'نیما', 'ترانه', 'آرمان', 'سودابه', 'بابک', 'گلناز']
    last_names = ['محلاتی', 'کریمی', 'حسینی', 'رضوی', 'نوری', 'یزدی', 'شیرازی', 
                  'کاشانی', 'اصفهانی', 'تبریزی', 'فردوسی', 'سهرابی', 'مهرآور', 'شفیعی']
    cities = ['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان', 'کرمان']
    art_preferences = ['نقاشی', 'معماری', 'شعر', 'موسیقی', 'تاریخ', 'خوشنویسی', 'مینیاتور']
    channels = ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in']
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # ---- تولید مهمانان ----
    guests = []
    for i in range(250):
        guest = {
            'guest_id': f'G{1000+i}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'phone': f'0912{random.randint(1000000, 9999999)}',
            'city': random.choice(cities),
            'first_visit': random.choice(date_range).strftime('%Y-%m-%d'),
            'total_visits': random.randint(1, 8),
            'art_preference': random.choice(art_preferences),
            'loyalty_score': round(random.uniform(0, 100), 1)
        }
        guests.append(guest)
    guests_df = pd.DataFrame(guests)
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    
    # ---- تولید رزرو با اتاق‌های واقعی ----
    reservations = []
    room_names = [room['name'] for room in HOTEL_CONFIG['rooms']]
    for i in range(500):
        check_in = random.choice(date_range)
        stay_days = random.randint(1, 4)
        check_out = check_in + timedelta(days=stay_days)
        room = random.choice(room_names)
        # قیمت بر اساس اتاق واقعی
        price = next((r['price'] for r in HOTEL_CONFIG['rooms'] if r['name'] == room), 5000000)
        
        reservation = {
            'reservation_id': f'R{10000+i}',
            'guest_id': f'G{random.randint(1000, 1249)}',
            'check_in': check_in.strftime('%Y-%m-%d'),
            'check_out': check_out.strftime('%Y-%m-%d'),
            'room_type': room,
            'price_per_night': price,
            'channel': random.choice(channels),
            'status': random.choices(['completed', 'cancelled', 'no-show'], weights=[0.7, 0.2, 0.1])[0]
        }
        reservations.append(reservation)
    reservations_df = pd.DataFrame(reservations)
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    
    # ---- تولید ایونت‌های فرهنگی ----
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
    
    for i in range(30):
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

# ============================================
# توابع بارگذاری و ذخیره داده
# ============================================

def load_data():
    try:
        guests = pd.read_csv('data/guests.csv', encoding='utf-8-sig')
        reservations = pd.read_csv('data/reservations.csv', encoding='utf-8-sig')
        events = pd.read_csv('data/events.csv', encoding='utf-8-sig')
        reservations['check_in'] = pd.to_datetime(reservations['check_in'])
        reservations['check_out'] = pd.to_datetime(reservations['check_out'])
        events['date'] = pd.to_datetime(events['date'])
        return guests, reservations, events
    except Exception as e:
        return None, None, None

def save_data(guests_df, reservations_df, events_df):
    guests_df.to_csv('data/guests.csv', index=False, encoding='utf-8-sig')
    reservations_df.to_csv('data/reservations.csv', index=False, encoding='utf-8-sig')
    events_df.to_csv('data/events.csv', index=False, encoding='utf-8-sig')

# ============================================
# توابع محاسباتی و تحلیلی
# ============================================

def calculate_kpis(guests_df, reservations_df, events_df):
    """محاسبه شاخص‌های کلیدی با اطلاعات واقعی"""
    total_guests = len(guests_df)
    total_rooms = len(HOTEL_CONFIG['rooms'])
    
    completed = reservations_df[reservations_df['status'] == 'completed']
    cancelled = reservations_df[reservations_df['status'] == 'cancelled']
    
    # نرخ اشغال (تخمینی بر اساس رزروهای تکمیل‌شده در ۳۰ روز اخیر)
    last_30_days = datetime.now() - timedelta(days=30)
    recent_completed = completed[completed['check_in'] >= last_30_days]
    occupancy = (len(recent_completed) / (30 * total_rooms)) * 100 if total_rooms > 0 else 0
    
    # ADR
    adr = completed['price_per_night'].mean() if not completed.empty else 0
    
    # درآمد کل
    revenue = 0
    if not completed.empty:
        completed['nights'] = (completed['check_out'] - completed['check_in']).dt.days
        revenue = (completed['price_per_night'] * completed['nights']).sum()
    
    # محبوب‌ترین اتاق
    if not completed.empty:
        popular_room = completed['room_type'].mode()[0] if not completed['room_type'].empty else 'نامشخص'
    else:
        popular_room = 'نامشخص'
    
    # محبوب‌ترین هنر
    if not guests_df.empty:
        popular_art = guests_df['art_preference'].mode()[0] if not guests_df['art_preference'].empty else 'نامشخص'
    else:
        popular_art = 'نامشخص'
    
    return {
        'total_guests': total_guests,
        'occupancy': occupancy,
        'adr': adr,
        'revenue': revenue,
        'popular_room': popular_room,
        'popular_art': popular_art,
        'cancellation_rate': (len(cancelled) / len(reservations_df) * 100) if len(reservations_df) > 0 else 0
    }

# ============================================
# توابع رسم نمودار با رنگ‌های هتل
# ============================================

def plot_loyalty_segmentation(guests_df):
    if guests_df.empty:
        return px.pie(title='داده‌ای وجود ندارد')
    bins = [0, 30, 50, 70, 100]
    labels = ['کم‌وفادار', 'متوسط', 'وفادار', 'بسیار وفادار']
    guests_df_copy = guests_df.copy()
    guests_df_copy['tier'] = pd.cut(guests_df_copy['loyalty_score'], bins=bins, labels=labels, right=True)
    tier_counts = guests_df_copy['tier'].value_counts().reset_index()
    tier_counts.columns = ['سطح', 'تعداد']
    fig = px.pie(tier_counts, values='تعداد', names='سطح', title='تقسیم‌بندی وفاداری', hole=0.4,
                 color_discrete_sequence=['#FF6B6B', '#FECA57', '#48DBFB', '#0ABDE3'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def plot_geography(guests_df):
    if guests_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    city_counts = guests_df['city'].value_counts().reset_index()
    city_counts.columns = ['شهر', 'تعداد']
    city_counts = city_counts.sort_values('تعداد', ascending=True)
    fig = px.bar(city_counts, x='تعداد', y='شهر', title='توزیع جغرافیایی', 
                 color='تعداد', color_continuous_scale=['#D2691E', '#FFD700'], orientation='h')
    fig.update_layout(height=400)
    return fig

def plot_art_preferences(guests_df):
    if guests_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    counts = guests_df['art_preference'].value_counts().reset_index()
    counts.columns = ['علاقه', 'تعداد']
    fig = px.bar(counts, x='علاقه', y='تعداد', title='علایق هنری مهمانان',
                 color='تعداد', color_continuous_scale=['#8B4513', '#FFD700'])
    fig.update_layout(showlegend=False)
    return fig

def plot_guest_growth(guests_df):
    if guests_df.empty:
        return px.line(title='داده‌ای وجود ندارد')
    guests_df_copy = guests_df.copy()
    guests_df_copy['first_visit'] = pd.to_datetime(guests_df_copy['first_visit'])
    monthly = guests_df_copy.groupby(guests_df_copy['first_visit'].dt.to_period('M')).size().reset_index()
    monthly.columns = ['ماه', 'مهمانان جدید']
    monthly['ماه'] = monthly['ماه'].astype(str)
    fig = px.line(monthly, x='ماه', y='مهمانان جدید', title='روند جذب مهمانان', 
                  markers=True, line_shape='spline')
    fig.update_traces(line=dict(color='#8B4513', width=3), marker=dict(color='#D2691E', size=8))
    return fig

def plot_room_analysis(reservations_df):
    if reservations_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    room_stats = reservations_df[reservations_df['status'] == 'completed'].groupby('room_type').agg({
        'price_per_night': 'mean',
        'reservation_id': 'count'
    }).reset_index()
    room_stats.columns = ['اتاق', 'میانگین قیمت', 'تعداد رزرو']
    fig = px.bar(room_stats, x='اتاق', y='میانگین قیمت', title='میانگین قیمت هر اتاق',
                 color='تعداد رزرو', color_continuous_scale=['#D2691E', '#FFD700'],
                 text='میانگین قیمت')
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(yaxis_title='قیمت (تومان)')
    return fig

def plot_events_dashboard(events_df):
    if events_df.empty:
        return px.bar(title='داده‌ای وجود ندارد'), px.bar(title='داده‌ای وجود ندارد')
    
    events_copy = events_df.copy()
    events_copy['fill_rate'] = (events_copy['registered'] / events_copy['capacity']) * 100
    events_copy = events_copy.sort_values('date')
    
    # نمودار ظرفیت و ثبت‌نام
    fig1 = px.bar(events_copy, x='event_name', y=['capacity', 'registered'],
                  title='وضعیت ثبت‌نام ایونت‌ها', barmode='group',
                  color_discrete_sequence=['#8B4513', '#D2691E'])
    fig1.update_layout(xaxis_title='ایونت', yaxis_title='تعداد')
    
    # نمودار درصد پر شدن
    fig2 = px.bar(events_copy, x='event_name', y='fill_rate',
                  title='درصد پر شدن ظرفیت', color='fill_rate',
                  color_continuous_scale=[[0, 'red'], [0.5, 'yellow'], [1, 'green']])
    fig2.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    fig2.update_layout(xaxis_title='ایونت', yaxis_title='درصد پر شدن')
    return fig1, fig2

def plot_event_revenue(events_df, reservations_df):
    if events_df.empty or reservations_df.empty:
        return px.bar(title='داده‌ای وجود ندارد')
    
    # شبیه‌سازی درآمد ایونت‌ها
    event_rev = events_df.copy()
    event_rev['revenue'] = event_rev['registered'] * (event_rev['price'] / 10000)
    event_rev = event_rev.sort_values('revenue', ascending=True)
    
    fig = px.bar(event_rev, x='revenue', y='event_name', title='درآمد ایونت‌ها (هزار تومان)',
                 color='revenue', color_continuous_scale=['#D2691E', '#FFD700'], orientation='h')
    fig.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
    fig.update_layout(xaxis_title='درآمد (هزار تومان)', yaxis_title='ایونت')
    return fig

# ============================================
# بخش مدیریت اطلاعات
# ============================================

def management_section(guests_df, reservations_df, events_df):
    st.header("📝 پنل مدیریت اطلاعات")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👤 مهمانان", "🏠 رزروها", "🎭 ایونت‌ها", "📊 ثبت‌نام ایونت"])
    
    with tab1:
        st.subheader("👤 مدیریت مهمانان")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(guests_df[['guest_id', 'first_name', 'last_name', 'phone', 'city', 'art_preference', 'loyalty_score']],
                        use_container_width=True, hide_index=True)
        with col2:
            with st.form("add_guest"):
                st.subheader("➕ افزودن مهمان جدید")
                first = st.text_input("نام")
                last = st.text_input("نام خانوادگی")
                phone = st.text_input("شماره تماس")
                city = st.selectbox("شهر", ['تهران', 'شیراز', 'اصفهان', 'مشهد', 'تبریز', 'یزد', 'کاشان', 'کرمان'])
                art = st.selectbox("علاقه هنری", HOTEL_CONFIG['event_categories'])
                if st.form_submit_button("افزودن مهمان"):
                    if first and last and phone:
                        new_id = f"G{len(guests_df) + 1000}"
                        new_guest = pd.DataFrame([{
                            'guest_id': new_id,
                            'first_name': first,
                            'last_name': last,
                            'phone': phone,
                            'city': city,
                            'first_visit': datetime.now().strftime('%Y-%m-%d'),
                            'total_visits': 1,
                            'art_preference': art,
                            'loyalty_score': 50.0
                        }])
                        guests_df_updated = pd.concat([guests_df, new_guest], ignore_index=True)
                        save_data(guests_df_updated, reservations_df, events_df)
                        st.success(f"✅ مهمان {first} {last} افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ نام و شماره تماس الزامی است!")
    
    with tab2:
        st.subheader("🏠 مدیریت رزروها")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(reservations_df[['reservation_id', 'guest_id', 'check_in', 'check_out', 'room_type', 'price_per_night', 'status']],
                        use_container_width=True, hide_index=True)
        with col2:
            with st.form("add_reservation"):
                st.subheader("➕ افزودن رزرو جدید")
                guest_id = st.selectbox("شناسه مهمان", guests_df['guest_id'].tolist())
                check_in = st.date_input("تاریخ ورود")
                check_out = st.date_input("تاریخ خروج")
                room_type = st.selectbox("نوع اتاق", [room['name'] for room in HOTEL_CONFIG['rooms']])
                price = st.number_input("قیمت هر شب (تومان)", min_value=100000, step=100000, value=5000000)
                channel = st.selectbox("کانال رزرو", ['Website', 'Booking.com', 'Instagram', 'Phone', 'Walk-in'])
                if st.form_submit_button("افزودن رزرو"):
                    if guest_id and check_in and check_out:
                        new_id = f"R{len(reservations_df) + 10000}"
                        new_res = pd.DataFrame([{
                            'reservation_id': new_id,
                            'guest_id': guest_id,
                            'check_in': check_in.strftime('%Y-%m-%d'),
                            'check_out': check_out.strftime('%Y-%m-%d'),
                            'room_type': room_type,
                            'price_per_night': price,
                            'channel': channel,
                            'status': 'completed'
                        }])
                        reservations_df_updated = pd.concat([reservations_df, new_res], ignore_index=True)
                        save_data(guests_df, reservations_df_updated, events_df)
                        st.success(f"✅ رزرو {new_id} افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ همه فیلدها را پر کنید!")
    
    with tab3:
        st.subheader("🎭 مدیریت ایونت‌ها")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(events_df[['event_id', 'event_name', 'date', 'capacity', 'registered', 'price', 'category']],
                        use_container_width=True, hide_index=True)
        with col2:
            with st.form("add_event"):
                st.subheader("➕ افزودن ایونت جدید")
                name = st.text_input("نام ایونت")
                date = st.date_input("تاریخ برگزاری")
                capacity = st.number_input("ظرفیت", min_value=1, value=30)
                price = st.number_input("قیمت (تومان)", min_value=0, step=100000, value=1000000)
                category = st.selectbox("دسته‌بندی", HOTEL_CONFIG['event_categories'])
                if st.form_submit_button("افزودن ایونت"):
                    if name and date:
                        new_id = f"E{len(events_df) + 2000}"
                        new_event = pd.DataFrame([{
                            'event_id': new_id,
                            'event_name': name,
                            'date': date.strftime('%Y-%m-%d'),
                            'capacity': capacity,
                            'registered': 0,
                            'price': price,
                            'category': category
                        }])
                        events_df_updated = pd.concat([events_df, new_event], ignore_index=True)
                        save_data(guests_df, reservations_df, events_df_updated)
                        st.success(f"✅ ایونت {name} افزوده شد!")
                        st.rerun()
                    else:
                        st.error("❌ نام و تاریخ ایونت الزامی است!")
    
    with tab4:
        st.subheader("📊 ثبت‌نام مهمانان در ایونت‌ها")
        col1, col2 = st.columns(2)
        with col1:
            selected_event = st.selectbox("ایونت مورد نظر", events_df['event_name'].tolist())
            event_data = events_df[events_df['event_name'] == selected_event]
            if not event_data.empty:
                st.info(f"""
                **📋 اطلاعات ایونت:**
                - تاریخ: {event_data['date'].iloc[0]}
                - ظرفیت: {event_data['capacity'].iloc[0]}
                - ثبت‌نام فعلی: {event_data['registered'].iloc[0]}
                - جای خالی: {event_data['capacity'].iloc[0] - event_data['registered'].iloc[0]}
                """)
        with col2:
            guest_list = guests_df['first_name'] + ' ' + guests_df['last_name'] + ' (' + guests_df['guest_id'] + ')'
            selected_guest = st.selectbox("مهمان", guest_list.tolist())
            if st.button("✅ ثبت‌نام در ایونت", use_container_width=True):
                # بروزرسانی تعداد ثبت‌نام
                event_idx = events_df[events_df['event_name'] == selected_event].index[0]
                events_df.loc[event_idx, 'registered'] += 1
                save_data(guests_df, reservations_df, events_df)
                st.success(f"✅ ثبت‌نام با موفقیت انجام شد!")
                st.balloons()
                st.rerun()
    
    return guests_df, reservations_df, events_df

# ============================================
# بخش تحلیل و گزارش
# ============================================

def analytics_section(guests_df, reservations_df, events_df):
    st.header("📊 تحلیل‌های هوشمند")
    
    # هدر هویتی
    st.markdown(f"""
    <div class="hotel-header">
        <h1>🏛️ {HOTEL_CONFIG['name']}</h1>
        <p style="font-size: 16px; opacity: 0.9;">تحلیل‌های عملیاتی بر اساس هنر، تاریخ و معماری</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIها
    kpis = calculate_kpis(guests_df, reservations_df, events_df)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("👥 مهمانان", kpis['total_guests'])
    with col2:
        st.metric("📈 نرخ اشغال", f"{kpis['occupancy']:.1f}%")
    with col3:
        st.metric("💰 ADR", f"{kpis['adr']/10000:,.0f} هزار تومان")
    with col4:
        st.metric("🏠 اتاق محبوب", kpis['popular_room'][:12] + "..." if len(kpis['popular_room']) > 12 else kpis['popular_room'])
    with col5:
        st.metric("🎨 هنر محبوب", kpis['popular_art'])
    with col6:
        st.metric("❌ نرخ لغو", f"{kpis['cancellation_rate']:.1f}%")
    
    st.markdown("---")
    
    # ردیف اول: تحلیل مهمانان
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
    
    # ردیف دوم: تحلیل اتاق‌ها و ایونت‌ها
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
    # ایجاد داده در صورت نیاز
    if not os.path.exists('data'):
        generate_realistic_data()
    
    # بارگذاری داده
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
        <div style="text-align: center; padding: 15px 0; background: linear-gradient(135deg, #8B4513, #D2691E); 
                    border-radius: 10px; margin-bottom: 20px;">
            <h2 style="color: #FFFFFF; margin: 0;">🏨 بوتیک هتل</h2>
            <h3 style="color: #FFD700; margin: 0;">محلاتی</h3>
            <p style="color: #F5DEB3; font-size: 12px;">شیراز - خیابان محلاتی</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        menu = st.radio("📋 منوی اصلی", ["📊 تحلیل و گزارش", "📝 مدیریت اطلاعات"])
        st.markdown("---")
        
        # اطلاعات سریع
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.caption(f"👥 {len(guests_df)} مهمان")
        st.caption(f"🏠 {len(reservations_df)} رزرو")
        st.caption(f"🎭 {len(events_df)} ایونت")
    
    # نمایش بخش‌ها
    if menu == "📊 تحلیل و گزارش":
        analytics_section(guests_df, reservations_df, events_df)
    else:
        guests_df, reservations_df, events_df = management_section(guests_df, reservations_df, events_df)
    
    # فوتر
    st.markdown("---")
    st.caption("🏛️ بوتیک هتل محلاتی - داشبورد هوشمند مدیریت | توسعه‌یافته با Streamlit")

if __name__ == "__main__":
    main()
